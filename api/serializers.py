from rest_framework import serializers
from .models import Producto, Cliente, PrecioCliente, ProductoVenta, Venta


class ProductoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Producto
        fields = '__all__'


class PrecioClienteSerializer(serializers.ModelSerializer): 

    producto_nombre = serializers.CharField(source='PRODUCTO.NOMBRE', read_only=True)

    producto_cantidad = serializers.IntegerField(source='PRODUCTO.CANTIDAD', read_only=True)

    class Meta:
        model = PrecioCliente
        fields = "__all__"


class ClienteSerializer(serializers.ModelSerializer):

    precios_cliente = PrecioClienteSerializer(many=True, read_only=True)

    class Meta:
        model = Cliente
        fields = '__all__'
    

class ProductoVentaSerializer(serializers.ModelSerializer):

    producto_nombre = serializers.CharField(source='PRODUCTO.NOMBRE', read_only=True)

    class Meta:

        model = ProductoVenta
        fields = "__all__"

class VentaSerializer(serializers.ModelSerializer):

    productos_venta = ProductoVentaSerializer(many=True, read_only=True)

    cliente_nombre = serializers.CharField(source='CLIENTE.NOMBRE', read_only=True)

    class Meta:

        model = Venta
        fields = "__all__"


