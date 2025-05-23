# Generated by Django 5.1.7 on 2025-04-09 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_order_food_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='category',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='food',
            name='is_vegetarian',
            field=models.BooleanField(default=False),
        ),
    ]
