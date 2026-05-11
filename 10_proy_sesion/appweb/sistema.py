# sistema.py
from flask import Flask
from appweb.postgres_db import pgdb
from appweb.views import registrar_rutas

def create_app():
    app = Flask(__name__)
    registrar_rutas(app)
    return app

app = create_app()
pgdb.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)