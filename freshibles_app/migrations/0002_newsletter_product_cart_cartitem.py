# Generated by Django 5.0.4 on 2024-04-19 20:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshibles_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=255)),
                ('product_description', models.TextField()),
                ('product_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_image', models.ImageField(upload_to='products/')),
                ('category', models.CharField(choices=[('Dairy', 'Dairy'), ('Vegetable', 'Vegetable'), ('Fruit', 'Fruit'), ('Bread', 'Bread'), ('Meat', 'Meat')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='freshibles_app.cart')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='freshibles_app.product')),
            ],
        ),
    ]
