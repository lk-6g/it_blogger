# Generated by Django 2.2.5 on 2019-11-07 14:08

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('it_bloggers', '0010_entry_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='text',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
