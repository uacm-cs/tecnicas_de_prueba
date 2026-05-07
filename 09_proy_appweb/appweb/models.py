# models.py
from appweb.postgres_db import pgdb
from flask import session

class AltaProductoException(Exception):
    pass
    
class AltaProductoPrecioException(Exception):
    pass
    
    
class DBException(Exception):
    pass


class Producto:

    def __init__(self, descripcion=None, precio=None, id=None):

        #Validaciones al crear el producto

        if isinstance(precio, str):
            try:
                precio = float(precio)
            except:
                raise AltaProductoException("Error: el precio es inválido")
            
        if precio <= 0:            
            raise AltaProductoPrecioException("Error: el precio no puede ser negativo o cero")

        if precio > 999999999:            
            raise AltaProductoPrecioException("Error: el precio es demasiado grande")

        self.id = id
        self.descripcion = descripcion
        self.precio = precio

    #---------------------------
    @property
    def db(self):
        """Accede a la conexión global de la base de datos"""
        global pgdb
        if pgdb is None:
            raise DBException("La conexión a la base de datos no ha sido inicializada")
        return pgdb

    #---------------------------
    def insertar(self):
        """Inserta un nuevo producto en la base de datos"""
        with self.db.get_cursor() as cur:
            # Se recomienda usar %s ; psycopg2 hará la conversión adecuada al tipo de dato utilizado
            cur.execute(
                "INSERT INTO Productos (descripcion, precio) VALUES (%s, %s) RETURNING id",
                (self.descripcion, self.precio)
            )
            self.id = cur.fetchone()[0]
        return self.id
    
    #---------------------------
    def actualizar(self):
        """Actualiza un producto existente en la base de datos"""
        with self.db.get_cursor() as cur:
            # Se recomienda usar %s ; psycopg2 hará la conversión adecuada al tipo de dato utilizado
            cur.execute(
                "UPDATE Productos SET descripcion = %s, precio = %s WHERE id = %s",
                (self.descripcion, self.precio, self.id)
            )
            # total de registros actualizados
            return cur.rowcount
        
    #---------------------------
    @classmethod
    def consultar_todo(cls):
        """Obtiene todos los productos"""
        with pgdb.get_cursor() as cur:
            cur.execute("SELECT id, descripcion, precio FROM Productos ORDER BY id")
            return [Producto(id=row[0], descripcion=row[1], precio=row[2]) for row in cur.fetchall()]
    
    
    @classmethod
    def consultar_id(cls, id):
        """Obtiene un producto por su ID"""
        with pgdb.get_cursor() as cur:
            # (id,) es necesaria para crear una tupla de un solo elemento en Python 
            # para sustituir los marcadores en el query.
            cur.execute("SELECT id, descripcion, precio FROM Productos WHERE id = %s", (id, ))
            row = cur.fetchone()
            if row:
                return Producto(id=row[0], descripcion=row[1], precio=row[2])
            return None

