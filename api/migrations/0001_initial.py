# Generated by Django 5.1.7 on 2025-04-04 09:39

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_category', models.CharField(choices=[('Veg', 'Veg'), ('Non-Veg', 'Non-Veg')], default='Veg', max_length=100)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, default='Write some Descriptions.', null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('ingredients', models.TextField(blank=True, default='Write some Ingredients.', null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='foods/')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(blank=True, max_length=255, null=True)),
                ('customer_contact', models.CharField(blank=True, max_length=15, null=True)),
                ('total_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('delivery_address', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Preparing', 'Preparing'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('location', models.TextField(blank=True, default='Write Location.', null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True)),
                ('qr_code', models.ImageField(blank=True, null=True, upload_to='qrcodes/')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.food')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='food_items',
            field=models.ManyToManyField(default=None, through='api.OrderItem', to='api.food'),
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Credit Card', 'Credit Card'), ('UPI', 'UPI'), ('Wallet', 'Wallet')], max_length=50)),
                ('is_paid', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='api.order')),
            ],
        ),
        migrations.CreateModel(
            name='Receipt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(blank=True, null=True, upload_to='receipts/')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='receipt', to='api.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='restaurant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.restaurant'),
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, default='Write some descriptions.', null=True)),
                ('is_available', models.BooleanField(default=True)),
                ('foods', models.ManyToManyField(default=None, related_name='menus', to='api.food')),
                ('restaurant', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.restaurant')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('comment', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.restaurant')),
            ],
        ),
    ]
