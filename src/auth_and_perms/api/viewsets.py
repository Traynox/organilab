from django.contrib.contenttypes.models import ContentType
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from auth_and_perms.api.serializers import RolSerializer, ProfilePermissionRolOrganizationSerializer
from auth_and_perms.models import Rol, ProfilePermission, Profile
from auth_and_perms.templatetags.user_rol_tags import get_related_contenttype_objects
from laboratory.models import OrganizationStructure, Laboratory
from laboratory.utils import get_profile_by_organization


class RolAPI(mixins.ListModelMixin,
             mixins.UpdateModelMixin,
             mixins.CreateModelMixin,
             viewsets.GenericViewSet):

    queryset = Rol.objects.all()
    serializer_class = RolSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        self.request=request
        return super().create(request, *args, **kwargs)


    def perform_create(self, serializer):
        super().perform_create(serializer)
        organizationstructure = OrganizationStructure.objects.filter(pk=self.request.data['rol']).first()
        if organizationstructure:
            serializer.instance.organizationstructure_set.add(organizationstructure)
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)


class UpdateRolOrganizationProfilePermission(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = ProfilePermission.objects.all()
    serializer_class = ProfilePermissionRolOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, pk):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            org = OrganizationStructure.objects.get(pk=pk)
            rols = org.rol.filter(pk__in=serializer.data['rols'])
            if serializer.data['as_conttentype']:
                profiles = get_profile_by_organization(pk)

                for profile in profiles:
                    ppdata={
                        'profile': profile,
                        'content_type': ContentType.objects.filter(
                            app_label=serializer.data['contenttypeobj']['appname'],
                            model= serializer.data['contenttypeobj']['model']
                        ).first()
                    }

                    if 'objectid' in serializer.data['contenttypeobj'] and serializer.data['contenttypeobj']['objectid']:
                        ppdata['object_id']=serializer.data['contenttypeobj']['objectid']
                    else:
                        ppdata['content_type']: ContentType.objects.filter(
                            app_label='auth_and_perms',
                            model='profile'
                        ).first()
                        ppdata['object_id'] = profile.pk
                    profilepermission = ProfilePermission.objects.filter(**ppdata).first()
                    if not profilepermission:
                        profilepermission = ProfilePermission.objects.create(**ppdata)
                    profilepermission.rol.clear()
                    profilepermission.rol.add(*rols)

            if serializer.data['as_user']:
                profile = Profile.objects.get(pk=serializer.data['profile'])

                for relobj in get_related_contenttype_objects(org):
                    """
                    {
                        'str': str(lab),
                        'obj': lab
                    }
                    """
                    if relobj['obj']:
                        query = ProfilePermission.objects.filter(
                            profile=profile,
                            content_type__app_label=relobj['obj']._meta.app_label,
                            content_type__model=relobj['obj']._meta.model_name,
                            object_id=relobj['obj'].pk)
                        if query.exists():
                            for profilepermission in query:
                                profilepermission.rol.clear()
                                profilepermission.rol.add(*rols)
                        else:
                            ppdata = {
                                'profile_id': serializer.data['profile'],
                                'content_type': ContentType.objects.filter(
                                    app_label=relobj['obj']._meta.app_label,
                                    model=relobj['obj']._meta.model_name,

                                ).first(),
                                'object_id': relobj['obj'].pk,
                            }
                            profilepermission = ProfilePermission.objects.create(**ppdata)
                            profilepermission.rol.add(*rols)
                    else:

                        ppdata = {
                            'profile_id': serializer.data['profile'],
                            'content_type': ContentType.objects.filter(
                                app_label=profile._meta.app_label,
                                model=profile._meta.model_name,

                            ).first(),
                            'object_id': profile.pk,
                        }
                        profilepermission, created = ProfilePermission.objects.get_or_create(**ppdata)
                        profilepermission.rol.add(*rols)
            if serializer.data['as_role']:
                profile = Profile.objects.get(pk=serializer.data['profile'])
                ppdata = {
                    'profile_id': serializer.data['profile'],
                    'content_type': ContentType.objects.filter(
                        app_label=serializer.data['contenttypeobj']['appname'],
                        model=serializer.data['contenttypeobj']['model'],
                    ).first()
                }

                if 'objectid' in serializer.data['contenttypeobj'] and serializer.data['contenttypeobj']['objectid']:
                    ppdata['object_id']=serializer.data['contenttypeobj']['objectid']
                else:
                    ppdata = {
                        'profile_id': serializer.data['profile'],
                        'content_type': ContentType.objects.filter(
                            app_label=profile._meta.app_label,
                            model=profile._meta.model_name,

                        ).first(),
                        'object_id': profile.pk,
                    }

                profilepermission = ProfilePermission.objects.filter(**ppdata).first()
                if not profilepermission:
                    profilepermission = ProfilePermission.objects.create(**ppdata)
                profilepermission.rol.clear()
                profilepermission.rol.add(*rols)

            return Response(serializer.data)
        return Response(serializer.errors)





