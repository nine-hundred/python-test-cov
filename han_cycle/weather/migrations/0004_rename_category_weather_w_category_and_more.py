# Generated by Django 4.2.14 on 2024-07-24 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0001_initial"),
        ("weather", "0003_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="weather",
            old_name="category",
            new_name="W_category",
        ),
        migrations.AlterUniqueTogether(
            name="weather",
            unique_together={
                ("location", "base_date", "base_time", "fcst_date", "W_category")
            },
        ),
    ]
