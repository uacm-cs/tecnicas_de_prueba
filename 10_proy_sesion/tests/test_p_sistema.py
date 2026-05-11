import pytest
from appweb.sistema import create_app
from appweb.postgres_db  import pgdb
from appweb.models import AltaProductoPrecioException, AltaProductoException, Producto

#carga los metodos de las vistas

@pytest.fixture(scope="session")
def app_flask():
    # Setup de la aplicación 
    app = create_app()
    
    app.config.update({
        "TESTING": True,
    })

    # Inicialización de la base de datos
    print("...inicializando entorno de TESTING...")
    pgdb.init_app(app)
    pgdb.create_all_tables()
    yield app
    # apartir de aquí se pone el código para liberar los recursos 
    # teardown limpiar/ reinicializar


#@pytest.fixture(scope="session")
# NOTA: Quitar el alcance de la fixture de "sesión" para que cada vez que se ejecute un test
# se cree un nuevo cliente y se limpie la sesión del usuario
@pytest.fixture()
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
    msj_esperado = "Menú"
    assert msj_esperado in data
    assert response.status_code == 200


def test_login_failed(client):
    # Si las credenciales fallaron la página retorna un codigo 401
    usuario = 'usuario1'
    password = 'x'
    response = client.post("/login", data={"usuario":  usuario , "contrasena": password}, follow_redirects=True)
    data = response.get_data().decode('utf-8')
    assert "Credenciales incorrectas" in data
    assert response.status_code == 200


def test_inicio_sin_sesion(client):
    response = client.get("/inicio", data={},  follow_redirects=True)
    data = response.get_data().decode('utf-8')
    msj_esperado = "No se ha iniciado sesión"
    assert msj_esperado in data
    assert response.status_code == 200
        

def test_consulta_producto_sin_sesion(client):
    response = client.get("/consulta_productos", data={},  follow_redirects=True)
    data = response.get_data().decode('utf-8')
    msj_esperado= "No se ha iniciado sesión"
    assert msj_esperado in data
    assert response.status_code == 200


#------------------
# Se define la función iniciar sesión para los tests que requieren autenticación 
#------------------
def iniciar_sesion(client):
    usuario = 'usuario1'
    password = 'u1'
    response = client.post("/login", data={"usuario":  usuario , "contrasena": password}, follow_redirects=True)
    data = response.get_data().decode('utf-8')
    msj_esperado = "Menú"
    assert msj_esperado in data
    assert response.status_code == 200



def test_alta_producto(client):
    # Iniciar sesión 
    iniciar_sesion(client)                
    desc = 'sueter'
    precio = 500
    response = client.post("/alta_producto", data={"descripcion":  desc  , "precio": precio}, follow_redirects=True)
    msj_esperado= "El producto se dio de alta correctamente"
    # Checa si la operación fue exitosa
    data = response.get_data().decode('utf-8')
    assert msj_esperado in data
    assert response.status_code == 200 

def test_alta_producto_precio_incorrecto(client):
    # Iniciar sesión 
    iniciar_sesion(client)     
    desc = 'sueter azul'
    precio = 'x'        
    response = client.post("/alta_producto", data={"descripcion":  desc  , "precio": precio}, follow_redirects=True)
    msj_esperado= "Error: el precio es inválido"
    data = response.get_data().decode('utf-8')
    assert msj_esperado in data
    assert response.status_code == 200 
        
def test_alta_producto_precio_negativo(client):

    # Iniciar sesión 
    iniciar_sesion(client)     
            
    desc = 'sueter azul'
    precio = 0
    response = client.post("/alta_producto", data={"descripcion":  desc  , "precio": precio}, follow_redirects=True)
    msj_esperado= "Error: el precio no puede ser negativo o cero"
    data = response.get_data().decode('utf-8')
    assert msj_esperado in data
    assert response.status_code == 200 


#===========================================================================
# Ejecución de los test.
#===========================================================================
# Desde la terminal,  ejecutar en la carpeta "tests"
#
#
# pytest -v test_p_sistema.py
#
#---------------------------------------------------------------------------
# Para visualizar las impresiones en consola usar el parámetro -s
#---------------------------------------------------------------------------
#
# pytest -vs test_p_sistema.py
#
#---------------------------------------------------------------------------



#===========================================================================
# Ejercicio
#===========================================================================
# De las páginas creadas para la tabla Empleado agregar los tests 
# correspondientes.
#
# 1. Validar el inicio de sesión para todos los métodos web del sistema
# 2. Implemnetar los tests correspondientes para la aplicación web para los usuarios autorizados
#===========================================================================
