# Generated by Django 4.2.14 on 2024-07-29 05:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("boards", "0004_alter_post_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="post",
            name="region",
        ),
    ]
