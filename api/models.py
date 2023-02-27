from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Producto(models.Model):

    NOMBRE = models.CharField(max_length=100)

    CANTIDAD = models.IntegerField(validators=[MinValueValidator(0)])

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])

    # RECUERDA NO PONER NADA QUE SE PUEDE VOLVER NULL AQUI
    def __str__(self):
        return f"{self.NOMBRE}, {self.CANTIDAD}, {self.PRECIO}"


class Cliente(models.Model):

    NOMBRE = models.CharField(max_length=100)

    def __str__(self):
        return str(self.NOMBRE)
    
class PrecioCliente(models.Model):

    CLIENTE = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="precios_cliente") 

    PRODUCTO = models.ForeignKey(Producto, on_delete=models.CASCADE)

    PRECIO = models.FloatField(validators=[MinValueValidator(0)])


    def __str__(self):
        return f"{self.CLIENTE.NOMBRE}, {self.PRODUCTO.NOMBRE}, {self.PRECIO}"


class Venta(models.Model):

    VENDEDOR = models.CharField(max_length=100)

    CLIENTE = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)

    FECHA = models.DateTimeField(auto_now=True)

    MONTO = models.FloatField(validators=[MinValueValidator(0)])

    TIPO_VENTA =  models.CharField(max_length=100, choices=(("MOSTRADOR", "MOSTRADOR"), ("RUTA", "RUTA")))

    TIPO_PAGO = models.CharField(max_length=100, choices=(("CONTADO", "CONTADO"), ("CREDITO", "CREDITO"), ("CORTESIA", "CORTESIA")))

    STATUS = models.CharField(max_length=100, choices=(("REALIZADO", "REALIZADO"), ("PENDIENTE", "PENDIENTE"), ("CANCELADO", "CANCELADO")))

    OBSERVACIONES = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.TIPO_VENTA}, {self.MONTO}, {self.TIPO_PAGO}"


class ProductoVenta(models.Model):

    VENTA = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name="productos_venta")
    PRODUCTO = models.ForeignKey(Producto, on_delete=models.CASCADE)
    CANTIDAD_VENTA = models.FloatField(validators=[MinValueValidator(0)])
    PRECIO_VENTA = models.IntegerField(validators=[MinValueValidator(0)])

    def __str__(self):
        return f"{self.VENTA}, {self.PRODUCTO.NOMBRE}"
