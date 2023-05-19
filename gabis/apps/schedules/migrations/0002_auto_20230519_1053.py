# Generated by Django 3.2.10 on 2023-05-19 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('masters', '0001_initial'),
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestbook',
            name='pin',
            field=models.CharField(blank=True, max_length=64, null=True, verbose_name='PIN of Guest'),
        ),
        migrations.AlterUniqueTogether(
            name='guestbook',
            unique_together={('booking_time_event', 'keuskupan', 'paroki', 'wilayah', 'lingkungan', 'name', 'mobile')},
        ),
    ]
