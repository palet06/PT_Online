# Generated by Django 2.1.1 on 2018-10-22 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kullanicilar', '0013_hocalar_cinsiyet'),
    ]

    operations = [
        migrations.CreateModel(
            name='okul',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('okul', models.CharField(max_length=100)),
                ('bolum', models.CharField(max_length=100)),
            ],
        ),
    ]
