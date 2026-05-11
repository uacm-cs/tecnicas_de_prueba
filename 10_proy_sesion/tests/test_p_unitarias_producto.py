import pytest
from appweb.sistema import create_app
from appweb.postgres_db  import pgdb
from appweb.models import AltaProductoPrecioException, AltaProductoException, Producto

app = create_app()
app.config.update({
        "TESTING": True,
    })

    # Inicialización de la base de datos
print("...inicializando entorno de TESTING...")
pgdb.init_app(app)
pgdb.create_all_tables()


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
    desc = 'camisa rosa'
    precio = 900
    # insertar producto
    p = Producto(descripcion=desc, precio=precio)
    id = p.insertar()    

    #-----------------------------
    # Test para probar la actulización de productos
    # modificar producto

    desc_esperada = "camisa rosa mexicano"
    registros_esperados = 1
    p.descripcion = desc_esperada
    registros_mod = p.actualizar()
    
    print(f"\nid modificado: {id}")
    print(f"total modificados: {registros_mod}")

    # verificar que el producto se modificó en la base de datos haciendo una consulta
    prod_modificado = Producto.consultar_id(id)

    assert prod_modificado.id == id
    assert prod_modificado.descripcion == desc_esperada
    assert registros_mod == registros_esperados


#===========================================================================
# Ejecución de los test.
#===========================================================================
# Desde la terminal,  ejecutar en la carpeta "tests"
#
#
# pytest -v test_p_unitarias_producto.py
#
#---------------------------------------------------------------------------
# Para visualizar las impresiones en consola usar el parámetro -s
#---------------------------------------------------------------------------
#
# pytest -vs test_p_unitarias_producto.py
#
#---------------------------------------------------------------------------

