# Generated by Django 4.2.3 on 2023-08-24 07:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("bio", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="client",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Client_id", models.CharField(default="", max_length=100)),
                ("Secret_key", models.CharField(default="", max_length=100)),
                ("fy_id", models.CharField(default="", max_length=100)),
                ("app_id_type", models.CharField(default="", max_length=100)),
                ("totp_key", models.CharField(default="", max_length=100)),
                ("pin", models.CharField(default="", max_length=100)),
                ("app_id", models.CharField(default="", max_length=100)),
                ("redirect_uri", models.CharField(default="", max_length=100)),
                ("app_type", models.CharField(default="", max_length=100)),
                ("app_id_hash", models.CharField(default="", max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
