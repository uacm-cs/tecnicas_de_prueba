from flask import render_template, request, redirect, url_for, session
from flask import flash
from appweb.models import Producto, AltaProductoException, AltaProductoPrecioException


# Datos de usuarios (simulados para el ejemplo)
USUARIOS = {
    'usuario1': 'u1',
    'usuario2': 'u2'
}

def registrar_rutas(app):
    #----------------------------------------
    # Registro de la clave secreta para el uso de sesiones del usuario
    #---------------------------------------- 
    SECRET_KEY='2ca8efd458259a5de5d4c2ce5692475d31401923470d34b1b6b86055453b5488017858b6351e4bd8615e7cf669cdb63e170d792865c04846cb06e6aa48f82b7f'
    app.config['SECRET_KEY'] = SECRET_KEY


    #----------------------------------------
    # Página de registro al sistema
    #----------------------------------------
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/login', methods=['GET', 'POST'])
    def login_home():
        error = None
        if request.method == 'POST':
            username = request.form['usuario']
            password = request.form['contrasena']
            if username in USUARIOS and USUARIOS[username] == password:
                # Registrar el usuario en la sesion actual
                session['usuario'] = username  # Almacenar el usuario en la sesión

                # Iniciar sesión exitosa, redirigir a otra página
                return redirect(url_for('inicio_home'))
            else:
                # Credenciales incorrectas, mostrar mensaje de error
                #return 'Credenciales incorrectas. <a href="/login">Intenta de nuevo</a>'
                msj= 'Credenciales incorrectas'
                flash(msj, 'danger')
                return  render_template('login.html')
        else:
            return render_template('login.html')
        

    @app.route('/logout', methods=['GET', 'POST'])
    def logout():
        session.clear()  # Limpiar la sesión para cerrar sesión
        msj = "Has cerrado la sesión correctamente"
        flash(msj, 'success')
        return redirect( url_for('login_home'))  # Redirige a la página de login



    #----------------------------------------    
    # Página  del menu principal
    #----------------------------------------
    @app.route('/inicio', methods=['GET']) 
    def inicio_home():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login_home'))  # Redirige a la página de login
            
        return render_template('inicio.html')


    #----------------------------------------
    # Página de la consulta de productos
    #----------------------------------------
    @app.route('/consulta_productos', methods=['GET'])
    def consulta_productos():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login_home'))  # Redirige a la página de login
            
        resultados = Producto.consultar_todo()
        print(resultados)
        return render_template("consulta.html", datos=resultados)


    #----------------------------------------
    # Página para dar de alta un producto
    #----------------------------------------
    @app.route('/alta_producto', methods=['GET', 'POST'])
    def alta_producto():
        if 'usuario' not in session:              
            msj = 'No se ha iniciado sesión'
            flash(msj, 'danger')
            return redirect( url_for('login_home'))  # Redirige a la página de login
                
        if request.method == 'POST':
            desc = request.form.get('descripcion')
            precio = request.form.get('precio')
            try:
                nuevo_prod = Producto(descripcion=desc, precio=precio)
                nuevo_prod.insertar()
                msj= "El producto se dio de alta correctamente"
                flash(msj, 'success')
                return  render_template('producto.html')

            except AltaProductoException as e:
                msj = str(e)
                flash(msj, 'danger')                
                return  render_template('producto.html')

            except AltaProductoPrecioException as e:
                msj = str(e)
                flash(msj, 'danger')  
                return  render_template('producto.html')

            except Exception as e:
                msj = str(e)
                flash(msj, 'danger')  
                return  render_template('producto.html')
            
        else:
            return render_template('producto.html')
        
