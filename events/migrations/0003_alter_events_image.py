# Generated by Django 4.0.3 on 2022-05-23 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_alter_events_options_alter_events_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='image',
            field=models.ImageField(null=True, upload_to='images'),
        ),
    ]
