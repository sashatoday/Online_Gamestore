# Generated by Django 2.1.3 on 2019-01-22 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0009_auto_20190122_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.PositiveSmallIntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birthDate',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='city',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='country',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('U', 'Unknown')], max_length=1),
        ),
    ]