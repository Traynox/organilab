# Generated by Django 2.2.20 on 2021-05-31 12:50

from django.db import migrations


def update_template(apps, schema_editor):
    model = apps.get_model('async_notifications', 'TemplateContext')
    template = model.objects.filter(code='Shelf object in limit').first()
    if template is not None:
        template.context_dic = {
            "Lista de objectos que se encuentra en el limite del laboratorio {{ laboratory.name }}": [
                ["shelf_object", "Object in limit"], ["laboratory", "Laboratory where is the object"]]}
        template.save()


class Migration(migrations.Migration):

    dependencies = [
        ('laboratory', '0042_change_email_template_message'),
    ]

    operations = [
        migrations.RunPython(update_template),
    ]
