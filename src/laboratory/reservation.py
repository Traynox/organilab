# encoding: utf-8

'''
Free as freedom will be 2/9/2016

@author: luisza
'''

from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from laboratory.models import ShelfObject
from djreservation.views import ProductReservationView


@method_decorator(permission_required('laboratory.add_shelfobject'), name='dispatch')
class ShelfObjectReservation(ProductReservationView):
    base_model = ShelfObject
    modelpk = None
    amount_field = 'quantity'
    extra_display_field = ['limit_quantity', 'measurement_unit']

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request, 'reservation'):
            return super(ShelfObjectReservation, self).dispatch(request, *args, **kwargs)
        return redirect(reverse('add_user_reservation'))
