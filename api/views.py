from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Producto, Cliente, PrecioCliente, Venta, ProductoVenta
from .serializers import ProductoSerializer, ClienteSerializer, PrecioClienteSerializer, VentaSerializer, ProductoVentaSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        

        return token



class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer

# Vistas para productos
@api_view(['GET'])
def producto_list(request):

    queryset = Producto.objects.all()

    serializer = ProductoSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def crear_producto(request):

    serializer = ProductoSerializer(data=request.data)

    if serializer.is_valid():
        producto = serializer.save()

        queryset = Cliente.objects.all()

        clientes_serializer = ClienteSerializer(queryset, many=True)

        for cliente_serializer in clientes_serializer.data:

            precio_cliente = PrecioCliente.objects.create(
                CLIENTE = Cliente.objects.get(pk = cliente_serializer["id"]),
                PRODUCTO = producto,
                PRECIO = producto.PRECIO
            )

            precio_cliente.save()


        return Response(serializer.data)
    

@api_view(['GET'])
def producto_detail(request, pk):

    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ProductoSerializer(producto)
    return Response(serializer.data)

@api_view(['PUT', 'DELETE'])
def modificar_producto(request, pk):

    try:
        producto = Producto.objects.get(pk=pk)
    except Producto.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        serializer = ProductoSerializer(producto, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        producto.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 
    

# Vistas para clientes
@api_view(['GET'])
def cliente_list(request):

    queryset = Cliente.objects.all()
    serializer = ClienteSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def crear_cliente(request):

    data = request.data 

    # Crear cliente
    serializer = ClienteSerializer(data=data)
    if serializer.is_valid():
        cliente = serializer.save()

        # Crear precios
        precios_cliente = data['preciosCliente']
        for precio_cliente in precios_cliente:

            nuevo_precio_cliente = PrecioCliente.objects.create(
                CLIENTE = cliente, 
                PRODUCTO = Producto.objects.get(pk = precio_cliente["productoId"]), 
                PRECIO = precio_cliente['precioCliente']
            )

            nuevo_precio_cliente.save()

        # Por lo tanto, es importante tener en cuenta que, aunque creas los objetos PrecioCliente después de haber validado y serializado el objeto Cliente, estos objetos estarán disponibles en la instancia del objeto Cliente y se incluirán en la respuesta cuando se serialice el objeto Cliente utilizando el serializer ClienteSerializer.
        return Response(serializer.data)
    return Response(serializer.errors)
            
@api_view(['GET'])
def cliente_detail(request, pk):

    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = ClienteSerializer(cliente)
    return Response(serializer.data)
    
@api_view(['PUT', 'DELETE'])
def modificar_cliente(request, pk):

    try: 
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        data = request.data 

        serializer = ClienteSerializer(cliente, data=data)

        if serializer.is_valid():
            serializer.save()

            nuevos_precios_cliente = data["nuevosPreciosCliente"]

            for nuevo_precio_cliente in nuevos_precios_cliente:

                precioCliente = PrecioCliente.objects.get(pk=nuevo_precio_cliente["precioClienteId"])
                precioCliente.PRECIO = nuevo_precio_cliente["nuevoPrecioCliente"]
                precioCliente.save()
            
            return Response(serializer.data)
        return Response(serializer.errors)
    
    elif request.method == 'DELETE':
        cliente.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


# Vistas para ventas
@api_view(['GET'])
def venta_list(request):

    queryset = Venta.objects.all()

    serializer = VentaSerializer(queryset, many=True)

    return Response(serializer.data)

@api_view(['POST'])
def crear_venta(request):

    data = request.data 

    serializer = VentaSerializer(data=data)

    if serializer.is_valid():
        venta = serializer.save()

        productos_venta = data["productosVenta"]

        for producto_venta in productos_venta:

            producto = Producto.objects.get(pk=producto_venta["productoId"])

            nuevo_producto_venta = ProductoVenta.objects.create(
                VENTA = venta,
                PRODUCTO = producto,
                CANTIDAD_VENTA = producto_venta["cantidadVenta"],
                PRECIO_VENTA = producto_venta["precioVenta"],
            )

            if data["STATUS"] == "REALIZADO": 
                producto.CANTIDAD -= nuevo_producto_venta.CANTIDAD_VENTA
                producto.save()

            nuevo_producto_venta.save()


        
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def venta_detail(request, pk):
    
    

    try:
        venta = Venta.objects.get(pk=pk)
        
    except Venta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = VentaSerializer(venta)
    return Response(serializer.data)


@api_view(['PUT', 'DELETE'])
def modificar_venta(request, pk):
    
    try:
        venta = Venta.objects.get(pk=pk)
        
    except Venta.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':

        reporte_cambios = {}

        data = request.data

        status_actual = venta.STATUS
        status_cambios = {"ANTES": status_actual}

        status_nuevo = data["STATUS"]
        
        productos_venta = venta.productos_venta 

        serializer = ProductoVentaSerializer(productos_venta, many=True)
        
        for producto_venta_serializer in serializer.data:

            producto = Producto.objects.get(NOMBRE = producto_venta_serializer["producto_nombre"])
            
            producto_cambios= {"ANTES": producto.CANTIDAD}

            cantidad_venta = producto_venta_serializer["CANTIDAD_VENTA"]

            producto.CANTIDAD = calcular_cantidad(status_actual, status_nuevo, producto.CANTIDAD, cantidad_venta)
            producto.save()
            producto_cambios["DESPUES"] = producto.CANTIDAD

            reporte_cambios[producto.NOMBRE] = producto_cambios

            

        venta.STATUS = status_nuevo
        venta.save()
        status_cambios["DESPUES"] = venta.STATUS
        reporte_cambios["STATUS"] = status_cambios

        return Response(reporte_cambios)

    elif request.method == 'DELETE':
        venta.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


def calcular_cantidad(status_actual, status, cantidad_antes, cantidad_venta):

    if status_actual == "PENDIENTE":
        if status == "REALIZADO":
            return cantidad_antes - cantidad_venta
        else:
            return cantidad_antes
    elif status_actual == "REALIZADO":
        if status in ["PENDIENTE", "CANCELADO"]:
            return cantidad_antes + cantidad_venta
        else: 
            return cantidad_antes
    else:
        return cantidad_antes

