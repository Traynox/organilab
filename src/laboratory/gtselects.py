from djgentelella.views.select2autocomplete import BaseSelect2View
from djgentelella.groute import register_lookups
from laboratory.models import Object,Rol

@register_lookups(prefix="rol", basename="rolsearch")
class RolGModelLookup(BaseSelect2View):
    model = Rol
    fields = ['name']

@register_lookups(prefix="object", basename="objectsearch")
class ObjectGModelLookup(BaseSelect2View):
    model = Object
    fields = ['code', 'name']

