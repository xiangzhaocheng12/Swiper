# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-28 14:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vip_end',
            field=models.DateTimeField(default='3000-01-01', verbose_name='VIP 截止日期'),
        ),
        migrations.AddField(
            model_name='user',
            name='vip_id',
            field=models.IntegerField(default=1, verbose_name='用户的VIP ID'),
        ),
    ]