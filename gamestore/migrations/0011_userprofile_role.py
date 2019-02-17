# Generated by Django 2.1.3 on 2019-01-22 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamestore', '0010_auto_20190122_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('A', 'Admin'), ('D', 'Developer'), ('P', 'Player')], default='P', max_length=1),
        ),
    ]