# Generated by Django 4.1.7 on 2023-02-24 03:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_preciocliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preciocliente',
            name='CLIENTE',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cliente_precios', to='api.cliente'),
        ),
    ]