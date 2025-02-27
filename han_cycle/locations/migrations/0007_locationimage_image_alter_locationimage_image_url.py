# Generated by Django 4.2.14 on 2024-07-29 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("locations", "0006_rename_l_category_location_l_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="locationimage",
            name="image",
            field=models.ImageField(default="", upload_to="locations/"),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="locationimage",
            name="image_url",
            field=models.URLField(blank=True),
        ),
    ]
