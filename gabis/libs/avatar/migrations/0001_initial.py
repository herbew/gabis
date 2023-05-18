# Generated by Django 3.2.10 on 2022-06-11 00:11

import gabis.libs.avatar.models
from django.conf import settings
import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.BooleanField(default=False)),
                ('avatar', models.ImageField(blank=True, max_length=1024, storage=django.core.files.storage.FileSystemStorage(), upload_to=gabis.libs.avatar.models.avatar_file_path)),
                ('date_uploaded', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]