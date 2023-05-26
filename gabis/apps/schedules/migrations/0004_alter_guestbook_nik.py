# Generated by Django 3.2.10 on 2023-05-26 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0003_alter_guestbook_nik'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guestbook',
            name='nik',
            field=models.CharField(db_index=True, help_text='KTP/Nomor HP', max_length=255, verbose_name='No Identitas'),
        ),
    ]
