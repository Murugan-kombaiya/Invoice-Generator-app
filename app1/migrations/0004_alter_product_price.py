# Generated by Django 5.1.6 on 2025-07-06 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app1", "0003_product_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="price",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
