# Generated by Django 4.1.5 on 2023-01-09 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_auto_20230109_0846'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuration',
            name='value',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]
