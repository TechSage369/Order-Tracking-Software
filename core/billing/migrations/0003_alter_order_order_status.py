# Generated by Django 4.1.7 on 2023-03-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_order_is_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('Unpaid', 'Unpaid'), ('Paid', 'Paid')], default='Unpaid', max_length=10),
        ),
    ]
