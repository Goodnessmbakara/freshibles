# Generated by Django 5.0.4 on 2024-04-20 00:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freshibles_app', '0002_newsletter_product_cart_cartitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('message_body', models.TextField()),
            ],
        ),
    ]