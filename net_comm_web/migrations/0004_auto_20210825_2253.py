# Generated by Django 3.1.7 on 2021-08-25 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('net_comm_web', '0003_auto_20210824_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='f_name',
            field=models.CharField(max_length=254),
        ),
    ]
