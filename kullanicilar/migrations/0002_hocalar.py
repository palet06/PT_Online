# Generated by Django 2.1.1 on 2018-10-18 19:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kullanicilar', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='hocalar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isim', models.CharField(default='', max_length=51, null=True, verbose_name='İsim')),
                ('soyisim', models.CharField(default='', max_length=51, null=True, verbose_name='Soysim')),
                ('kayit_tarihi', models.DateTimeField(default=django.utils.timezone.now)),
                ('dogum_tarihi', models.DateTimeField(null=True)),
            ],
        ),
    ]
