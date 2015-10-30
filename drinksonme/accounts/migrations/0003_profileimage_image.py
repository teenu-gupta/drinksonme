# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import accounts.models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20151027_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileimage',
            name='image',
            field=models.ImageField(null=True, upload_to=accounts.models.profile_image_path, blank=True),
        ),
    ]
