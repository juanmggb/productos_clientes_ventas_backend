# Generated by Django 4.1.7 on 2023-02-24 04:58

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_preciocliente_cliente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('VENDEDOR', models.CharField(max_length=100)),
                ('FECHA', models.DateTimeField(auto_now=True)),
                ('MONTO', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('TIPO_VENTA', models.CharField(choices=[('MOSTRADOR', 'MOSTRADOR'), ('RUTA', 'RUTA')], max_length=100)),
                ('TIPO_PAGO', models.CharField(choices=[('CONTADO', 'CONTADO'), ('CREDITO', 'CREDITO'), ('CORTESIA', 'CORTESIA')], max_length=100)),
                ('STATUS', models.CharField(choices=[('REALIZADO', 'REALIZADO'), ('PENDIENTE', 'PENDIENTE'), ('CANCELADO', 'CANCELADO')], max_length=100)),
                ('OBSERVACIONES', models.CharField(max_length=100)),
                ('CLIENTE', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.cliente')),
            ],
        ),
    ]