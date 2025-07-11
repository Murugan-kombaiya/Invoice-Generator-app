# Generated by Django 5.2.3 on 2025-06-21 21:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="invoice",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="invoice",
            name="status",
            field=models.CharField(
                choices=[("Paid", "Paid"), ("Unpaid", "Unpaid")], max_length=20
            ),
        ),
    ]
