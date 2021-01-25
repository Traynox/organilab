from django.dispatch import receiver
from django.db.models.signals import post_save

from laboratory.models import ShelfObject, Profile
from django.conf import settings
from async_notifications.utils import send_email_from_template
from laboratory.models import BlockedListNotification


@receiver(post_save, sender=ShelfObject)
def notify_shelf_object_reach_limit(sender, **kwargs):
    instance = kwargs.get('instance')

    if instance.quantity < instance.limit_quantity:
        # send email notification
        send_email_to_ptech_limitobjs(instance)


def send_email_to_ptech_limitobjs(shelf_object, enqueued=True):
    labroom = shelf_object.shelf.furniture.labroom
    laboratory = labroom.laboratory_set.first()
    context = {
        'shelf_object': shelf_object,
        'labroom': labroom,
        'laboratory': laboratory
    }
    blocked = BlockedListNotification.objects.filter(
        laboratory=laboratory, object=shelf_object.object)
    blocked_emails = [x for x in blocked.values_list('user__email', flat=True)]
    ptech = Profile.objects.filter(laboratories__in=[laboratory])
    emails = [x for x in ptech.values_list('user__email', flat=True)]
    allowed_emails = [x for x in emails if x not in blocked_emails]
    if not allowed_emails:
        allowed_emails = [settings.DEFAULT_FROM_EMAIL]
    for email in allowed_emails:
        schema = f"http://localhost:8000/lab/{laboratory.pk}/blocknotifications/"
        context['domain'] = f"{schema}{shelf_object.object.pk}/"
        send_email_from_template("Shelf object in limit",
                             email,
                             context=context,
                             enqueued=enqueued,
                             user=None,
                             upfile=None)
