# Generated by Django 4.1 on 2022-08-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Err',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1000)),
                ('url', models.CharField(max_length=1000)),
                ('timestamp', models.DecimalField(decimal_places=0, max_digits=15)),
                ('full_ua', models.CharField(max_length=1000)),
                ('browser_name', models.CharField(max_length=1000)),
                ('browse_version', models.CharField(max_length=1000)),
                ('os', models.CharField(max_length=1000)),
                ('type', models.CharField(max_length=1000)),
                ('error_type', models.CharField(max_length=1000)),
                ('kind', models.CharField(max_length=1000)),
                ('message', models.CharField(max_length=1000)),
                ('position', models.CharField(max_length=100)),
                ('stack', models.CharField(max_length=1000)),
                ('selector', models.CharField(max_length=1000)),
            ],
        ),
    ]
