# Generated by Django 2.1.1 on 2018-10-21 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kullanicilar', '0008_auto_20181019_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='hocalar',
            name='resim',
            field=models.CharField(default='/static/img/default.png', max_length=701, null=True, verbose_name='Resim'),
        ),
    ]
