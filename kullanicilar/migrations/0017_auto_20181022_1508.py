# Generated by Django 2.1.1 on 2018-10-22 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kullanicilar', '0016_auto_20181022_1502'),
    ]

    operations = [
        migrations.AddField(
            model_name='hocalar',
            name='bolum',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='Bölüm'),
        ),
        migrations.AddField(
            model_name='hocalar',
            name='universite',
            field=models.CharField(default='', max_length=100, null=True, verbose_name='Üniversite'),
        ),
    ]
