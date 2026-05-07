import pytest
from appweb.sistema import create_app
from appweb.postgres_db import pgdb
import re
from appweb.models import AltaProductoPrecioException, AltaProductoException, Producto


# carga los metodos de las vistas


@pytest.fixture(scope="session")
def app_flask():
    # Setup de la aplicación
    app = create_app()

    app.config.update(
        {
            "TESTING": True,
        }
    )

    # Inicialización de la base de datos
    print("...inicializando entorno de TESTING...")
    pgdb.init_app(app)
    # pgdb.create_all_tables()

    yield app
    # apartir de aquí se pone el código para liberar los recursos

    # teardown limpiar/ reinicializar


@pytest.fixture(scope="session")
def client(app_flask):
    print("creando cliente...")
    with app_flask.test_client() as client:
        # Establecer el contexto de aplicación
        with app_flask.app_context():
            yield client


# --------------------------------------------------
# Test de las transacciones de la aplicación
# --------------------------------------------------


def test_login(client):
    usuario = "usuario1"
    password = "u1"
    response = client.post(
        "/login",
        data={"usuario": usuario, "contrasena": password},
        follow_redirects=True,
    )
    data = response.get_data().decode("utf-8")
    print(data)
    assert "<h1>Menú</h1>" in data
    # assert response.status_code == 200


def test_login_failed(client):

    # Si las credenciales fallaron la página retorna un codigo 401
    usuario = "usuario1"
    password = "u"
    response = client.post(
        "/login",
        data={"usuario": usuario, "contrasena": password},
        follow_redirects=True,
    )
    data = response.get_data().decode("utf-8")
    print(data)
    assert "<strong>Error:</strong> Credenciales incorrectas" in data
    # assert response.status_code == 401


def test_consulta_producto(client):
    response = client.post("/consulta_productos", data={}, follow_redirects=True)
    data = response.get_data().decode("utf-8")
    print(data)
    assert "Lista de Datos" in data

    # patron = r"<td>\s*pantalon\s*</td>\s*<td>\s*488\.00\s*</td>"
    # assert re.search(patron, data, re.IGNORECASE)


def test_alta_producto(client):
        desc = 'sueter'
        precio = 500
        response = client.post("/alta_producto", data={"descripcion":  desc  , "precio": precio}, follow_redirects=True)
        msj_esperado= "El producto se dio de alta correctamente"
        # Checa si la operación fue exitosa
        data = response.get_data().decode('utf-8')
        assert msj_esperado in data
        assert response.status_code == 200 

def test_alta_producto_precio_incorrecto(client):
        desc = 'sueter azul'
        precio = 'x'        
        response = client.post("/alta_producto", data={"descripcion":  desc  , "precio": precio}, follow_redirects=True)
        msj_esperado= "Error: el precio es inválido"
        data = response.get_data().decode('utf-8')
        assert msj_esperado in data
        assert response.status_code == 200 
        
def test_alta_producto_precio_negativo(client):
        desc = 'sueter azul'
        precio = 0
        response = client.post("/alta_producto", data={"descripcion":  desc  , "precio": precio}, follow_redirects=True)
        msj_esperado= "Error: el precio no puede ser negativo o cero"
        data = response.get_data().decode('utf-8')
        assert msj_esperado in data
        assert response.status_code == 200 


#---------------------------------------------
# Testing de los métodos del modelo de datos: Clase Producto
#---------------------------------------------

def test_crear_producto():
    desc = 'camisa'
    precio = 900
    p = Producto(descripcion=desc, precio=precio)
    assert  p.descripcion == desc
    assert  p.precio == precio

def test_crear_producto_precio_negativo():
    desc = 'camisa'
    precio = -10
    with pytest.raises(AltaProductoPrecioException) as e:
        p = Producto(descripcion=desc, precio=precio)

def test_insertar_producto():
    desc = 'camisa azul'
    precio = 900
    p = Producto(descripcion=desc, precio=precio)
    id = p.insertar()
    prod_insertado = p.consultar_id(id)
    assert prod_insertado.id == id
    assert prod_insertado.descripcion == desc
    assert prod_insertado.precio == precio


def test_actualizar_producto_desc():
    #-----------------------------
    # Preparación de los datos  para el test
    desc = 'camisa bicolor '
    precio = 900
    # insertar producto
    p = Producto(descripcion=desc, precio=precio)
    id = p.insertar()    

    #-----------------------------
    # Test para probar la actulización de productos
    # modificar producto

    desc_esperada = "camisa  colorida"
    registros_esperados = 1
    p.descripcion = desc_esperada
    registros_mod = p.actualizar()
    
    print(f"\nid modificado: {id}")
    print(f"total modificados: {registros_mod}")

    # verificar que el producto se modificó en la base de datos haciendo una consulta
    prod_modificado = Producto.consultar_id(id)

    assert prod_modificado.id == id
    assert prod_modificado.descripcion == desc_esperada
    assert registros_mod >= registros_esperados


#===========================================================================
# Ejecución de los test.
#===========================================================================
# Desde la terminal,  ejecutar en la carpeta "tests"
#
#
# pytest -v test_sistema.py
#
#---------------------------------------------------------------------------
# Para visualizar las impresiones en consola usar el parámetro -s
#---------------------------------------------------------------------------
#
# pytest -vs test_sistema.py
#
#---------------------------------------------------------------------------



#===========================================================================
# Ejercicio
#===========================================================================
# De las páginas creadas para la tabla Empleado agregar los tests 
# correspondientes.
#
# 1. Modelar la clase Empleados y sus métodos de servio:
#   - Creación de los objetos
#   - Consultar registros
#   - Insertar registro
# 
# 2. Agregar los tests para probar los endpoints (servicios web) para Empleados
# 3. Agregar los tests para probar los métodos de la clase
#===========================================================================


