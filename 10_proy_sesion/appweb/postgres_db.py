
from psycopg2.pool import ThreadedConnectionPool, PoolError
from contextlib import contextmanager
import atexit


db_config = { "host" : "localhost",
                "database" : "sistema_abc",
                "user" : "uacm",
                "password" : "uacm1"}


_tabla_productos = "CREATE TABLE Productos (" \
                "id SERIAL PRIMARY KEY,"  \
                "descripcion TEXT,"   \
                "precio NUMERIC(10, 2)" \
                ");"


class PostgresDB:
    def __init__(self):
        self.app = None
        self.pool = None
        self._closed = False 

    def init_app(self, app):
        self.app = app
        self.connect()
        atexit.register(self.close)                

    def connect(self):
        self.pool = ThreadedConnectionPool(minconn=1, maxconn=30, **db_config)

    def create_all_tables(self):
        drop_productos ="DROP TABLE IF EXISTS Productos;"
        with self.get_cursor() as cur: 
            cur.execute(drop_productos)
            cur.execute(_tabla_productos)


# El decorador @contextmanager, se utiliza para crear administradores de contexto (context managers), 
# lo que facilita la gestión de recursos de manera más limpia y eficiente. 
# Se puede definir el comportamiento de entrada y salida del contexto dentro de una función, en lugar de tener que definir una clase con los métodos __enter__ y __exit__
    @contextmanager
    def get_cursor(self):
        if self.pool is None:
            self.connect()
        # Obtiene una conexión del pool
        con = self.pool.getconn()
        cur = con.cursor()
        try:
            # "pausa" y entrega el cursor al bloque with
            yield cur
            # Al salir del with
            # Se ejecuta si no hubo excepciones
            con.commit()
        except Exception:
            con.rollback()  # cancelar los cambios
            raise
        finally:
            cur.close()          # cerrar el cursor
            self.pool.putconn(con)  # devolver conexión al pool

    def close(self):
        if self.pool and not self._closed:
            try:
                self.pool.closeall()
            except PoolError as e:
                # Si ya está cerrado, ignoramos
                if "connection pool is closed" not in str(e):
                    raise
            finally:
                self._closed = True
                self.pool = None

# Instancia a la DB

pgdb = PostgresDB()            
