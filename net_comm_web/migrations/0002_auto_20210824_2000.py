# Generated by Django 3.1.7 on 2021-08-24 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_comm_web', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='f_name',
            field=models.CharField(max_length=50),
        ),
    ]
