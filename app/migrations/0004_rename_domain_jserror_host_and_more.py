# Generated by Django 4.1 on 2022-08-13 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_website'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jserror',
            old_name='domain',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='performance',
            old_name='domain',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='promiseerror',
            old_name='domain',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='resourceerror',
            old_name='domain',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='website',
            old_name='domain',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='whitescreenerror',
            old_name='domain',
            new_name='host',
        ),
        migrations.RenameField(
            model_name='xhrerror',
            old_name='domain',
            new_name='host',
        ),
    ]
