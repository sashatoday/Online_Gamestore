# Generated by Django 2.0.8 on 2019-02-19 02:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0022_auto_20190214_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('U', 'Unknown'), ('M', 'Male'), ('F', 'Female')], default='U', max_length=1),
        ),
    ]
