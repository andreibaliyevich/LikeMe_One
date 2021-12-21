# Generated by Django 3.2.8 on 2021-11-06 09:25

import announcements.utilities
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import easy_thumbnails.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main_app', '0001_initial'),
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=128, verbose_name='Title')),
                ('image', easy_thumbnails.fields.ThumbnailerImageField(upload_to=announcements.utilities.get_announcement_path, verbose_name='Image')),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Date/Time')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='places.place', verbose_name='Place')),
                ('region', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='announcements', to='main_app.region', verbose_name='Region')),
            ],
            options={
                'verbose_name': 'Announcement',
                'verbose_name_plural': 'Announcements',
                'ordering': ['date_time'],
            },
        ),
    ]
