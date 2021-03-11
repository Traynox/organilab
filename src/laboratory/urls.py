'''
Created on 1/8/2016

@author: nashyra
'''

from django.conf.urls import url, include
from django.urls import path
from authentication.users import ChangeUser, password_change
from laboratory import views
from authentication import users
from laboratory.reservation import ShelfObjectReservation
from laboratory.search import SearchObject
from laboratory.sustance.views import create_edit_sustance, sustance_list, SustanceListJson, SubstanceDelete
from laboratory.views import furniture, reports, shelfs, objectfeature
from laboratory.views import labroom, shelfobject, laboratory, solutions, organizations
from laboratory.views.access import access_management, users_management, delete_user
from laboratory.views.laboratory import LaboratoryListView, LaboratoryDeleteView
from laboratory.views.profiles_management import ProfilesListView,ProfileUpdateView
from laboratory.views.objects import ObjectView, block_notifications 
from laboratory.api.views import ApiReservedProductsCRUD, ApiReservationCRUD
from laboratory.views.my_reservations import MyReservationView
from laboratory.validators import validate_duplicate_initial_date
from laboratory.functions import return_laboratory_of_shelf_id
objviews = ObjectView()

urlpatterns = [
    url(r'rp/api/reservedProducts/(?P<pk>\d+)/', ApiReservedProductsCRUD.as_view(), name='api_reservation_detail'),
    url(r'rp/api/reservedProducts$', ApiReservedProductsCRUD.as_view(), name='api_reservation_create'),
    url(r'rp/api/reservedProducts/(?P<pk>\d+)/delete/', ApiReservedProductsCRUD.as_view(), name='api_reservation_delete'),
    url(r'rp/api/reservedProducts/(?P<pk>\d+)/update/', ApiReservedProductsCRUD.as_view(), name='api_reservation_update'),
    url(r'r/api/reservation$', ApiReservationCRUD.as_view(), name='api_individual_reservation_create'),
    url(r"my_reservations$", MyReservationView.as_view(), name="my_reservations"),
    url(r'^(?P<lab_pk>\d+)$', views.lab_index, name='labindex'),
    url(r'^(?P<pk>\d+)/edit$', laboratory.LaboratoryEdit.as_view(), name='laboratory_update'),
    url(r'^select$', laboratory.SelectLaboratoryView.as_view(), name='select_lab'),
    url(r'^create_lab$', laboratory.CreateLaboratoryFormView.as_view(), name='create_lab'),
    # Tour steps
    url(r'^_ajax/get_tour_steps$', views.get_tour_steps, name='get_tour_steps'),
    url(r'^_ajax/get_tour_steps_furniture$', views.get_tour_steps_furniture, name='get_tour_steps_furniture'),
    url(r"reserve_object/(?P<modelpk>\d+)$", ShelfObjectReservation.as_view(), name="object_reservation"),

    url(r"validators", validate_duplicate_initial_date, name="date_validator"),
    url(r"returnLabId", return_laboratory_of_shelf_id, name="get_lab_id"),
]

lab_shelf_urls = [
    url(r"^list$", shelfs.list_shelf, name="list_shelf"),
    url(r"^create$", shelfs.ShelfCreate.as_view(), name="shelf_create"),
    url(r"^delete/(?P<pk>\d+)/(?P<row>\d+)/(?P<col>\d+)$",
        shelfs.ShelfDelete, name="shelf_delete"),
    url(r'^edit/(?P<pk>\d+)/(?P<row>\d+)/(?P<col>\d+)$',
        shelfs.ShelfEdit.as_view(), name="shelf_edit")
]

lab_rooms_urls = [
    url(r'^$', labroom.LaboratoryRoomsList.as_view(), name='rooms_list'),
    url(r'^create$', labroom.LabroomCreate.as_view(), name='rooms_create'),
    url(r'^(?P<pk>\d+)/delete$', labroom.LaboratoryRoomDelete.as_view(),
        name='rooms_delete'),
    url(r'^(?P<pk>\d+)/edit$', labroom.LabroomUpdate.as_view(),
        name='rooms_update'),
]

lab_furniture_urls = [
    url(r'^$', furniture.list_furniture, name='furniture_list'),

    url(r'^create/(?P<labroom>\d+)$', furniture.FurnitureCreateView.as_view(),
        name='furniture_create'),

    url(r'^edit/(?P<pk>\d+)$', furniture.FurnitureUpdateView.as_view(),
        name='furniture_update'),
    url(r'^delete/(?P<pk>\d+)$', furniture.FurnitureDelete.as_view(),
        name='furniture_delete'),
]

shelf_object_urls = [
    url(r"^list$", shelfobject.list_shelfobject,
        name="list_shelfobject"),
    url(r"^create$", shelfobject.ShelfObjectCreate.as_view(),
        name="shelfobject_create"),
    url(r"^delete/(?P<pk>\d+)$",
        shelfobject.ShelfObjectDelete.as_view(), name="shelfobject_delete"),
    url(r"^edit/(?P<pk>\d+)$",
        shelfobject.ShelfObjectEdit.as_view(), name="shelfobject_edit"),
    url(r"q/update/(?P<pk>\d+)$", shelfobject.ShelfObjectSearchUpdate.as_view(),
        name="shelfobject_searchupdate"),
]

lab_reports_urls = [
    # PDF reports
    url(r'^laboratory$', reports.report_labroom_building,
        name='report_building'),
    url(r'^furniture$', reports.report_furniture,
        name='reports_furniture'),
    url(r'^objects$', reports.report_objects, name='reports_objects'),
    url(r'^shelf_objects$', reports.report_shelf_objects,
        name='reports_shelf_objects'),
    url(r'^limited_shelf_objects$', reports.report_limited_shelf_objects,
        name='reports_limited_shelf_objects'),
    url(r'^reactive_precursor_objects$', reports.report_reactive_precursor_objects,
        name='reports_reactive_precursor_objects'),
    # HTML reports
    url(r'^list/laboratory$', labroom.LaboratoryRoomReportView.as_view(),
        name='reports_laboratory'),
    url(r'^list/furniture$$', furniture.FurnitureReportView.as_view(),
        name='reports_furniture_detail'),
    url(r'^list/objects$', reports.ObjectList.as_view(),
        name='reports_objects_list'),
    url(r'^list/limited_shelf_objects$', reports.LimitedShelfObjectList.as_view(),
        name='reports_limited_shelf_objects_list'),
    url(r'^list/reactive_precursor_objects$', reports.ReactivePrecursorObjectList.as_view(),
        name='reactive_precursor_object_list'),
    url('^objectchanges$', reports.LogObjectView.as_view(), name='object_change_logs'),
    url('^organizationreactivepresence/$', reports.OrganizationReactivePresenceList.as_view(), name='organizationreactivepresence'),

]

lab_reports_organization_urls = [
    url(r'^organization$', reports.report_organization_building,
        name='reports_organization_building'),
    url(r'^list$', organizations.OrganizationReportView.as_view(),
        name='reports_organization'),
]

lab_features_urls = [
    url(r'^create$', objectfeature.FeatureCreateView.as_view(),
        name='object_feature_create'),
    url(r'^edit/(?P<pk>\d+)$', objectfeature.FeatureUpdateView.as_view(),
        name='object_feature_update'),
    url(r'^delete/(?P<pk>\d+)$', objectfeature.FeatureDeleteView.as_view(),
        name='object_feature_delete'),
]

solutions_urls = [
    url(r'^calculator$', solutions.SolutionCalculatorView.as_view(),
        name='solution_calculator'),
    url(r'^$', solutions.SolutionListView.as_view(), name='solution_list'),
    url(r'^(?P<pk>\d+)$', solutions.SolutionDetailView.as_view(),
        name='solution_detail')
]


reports_all_lab=[
    url(r'^reports/hcode$', laboratory.HCodeReports.as_view(), name='h_code_reports'),
    url(r'^reports/download/hcode$', reports.report_h_code, name='download_h_code_reports'),
]

sustance_urls = [
    url('sustance/edit/(?P<pk>\d+)?/(?P<lab_pk>\d+)?$', create_edit_sustance, name='sustance_manage'),
    url('sustance/add/(?P<lab_pk>\d+)?$', create_edit_sustance, name='sustance_add'),
    url('sustance/delete/(?P<pk>\d+)?$', SubstanceDelete.as_view(), name='sustance_delete'),
    url('sustance/(?P<lab_pk>\d+)?$', sustance_list, name='sustance_list'),
    url('sustance/json/(?P<lab_pk>\d+)?$', SustanceListJson.as_view(), name='sustance_list_json'),
]

organization_urls = [
    url('access_list$', access_management, name="access_list"),
    url('access_list/(?P<pk>\d+)/users$', users_management, name="users_management"),
    url('access_list/(?P<pk>\d+)/users/(?P<user_pk>\d+)?$', delete_user, name="delete_user"),
    url('access_list/(?P<pk>\d+)/users/add$', users.AddUser.as_view(), name="add_user"),
    url('profile/(?P<pk>\d+)/info$', ChangeUser.as_view(), name='profile'),
    url('profile/(?P<pk>\d+)/password$', password_change, name='password_change'),
]

lab_profiles_urls = [
    url(r"list$", ProfilesListView.as_view(), name="lab_profiles"),
    url(r"list/(?P<pk>\d+)?$", ProfileUpdateView.as_view(), name="update_lab_profile"),
] 

'''MULTILAB'''
urlpatterns += sustance_urls + organization_urls + [
    url(r'mylabs$', LaboratoryListView.as_view(), name="mylabs"),
    url(r'^lab/(?P<pk>\d+)/delete', LaboratoryDeleteView.as_view(), name="laboratory_delete"),
    url(r"^lab/(?P<lab_pk>\d+)?/search$", SearchObject.as_view(), name="search"),
    url(r'^lab/(?P<lab_pk>\d+)/rooms/', include(lab_rooms_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/furniture/', include(lab_furniture_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/objects/', include(objviews.get_urls())),
    url(r'^lab/(?P<lab_pk>\d+)/reports/', include(lab_reports_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/shelfobject/', include(shelf_object_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/shelf/', include(lab_shelf_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/features/', include(lab_features_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/solutions/', include(solutions_urls)),
    url(r'^lab/(?P<lab_pk>\d+)/organizations/reports/',
        include(lab_reports_organization_urls)),
    url(r'^lab/(?P<lab_pk>\d+)?/profiles/',include(lab_profiles_urls)),
    path(
        'lab/<int:lab_pk>/blocknotifications/<int:obj_pk>/', 
        block_notifications, name="block_notification") 
] +reports_all_lab
