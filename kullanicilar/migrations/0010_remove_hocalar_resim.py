# Generated by Django 2.1.1 on 2018-10-21 20:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kullanicilar', '0009_hocalar_resim'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hocalar',
            name='resim',
        ),
    ]
