from flask import Flask, request, render_template, redirect, flash, session, jsonify
from models import Usuario, db, Categoria, categorias_curso, Curso
# con eso importamos la password hasheada
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from flask_session import Session
# clase de Integrity Error
from sqlalchemy.exc import IntegrityError
# importaciones para login
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config.from_object(Config)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db.init_app(app)

#configuraciones para logearse
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# ruta para crear categorias (opcional)
@app.route("/categorias", methods=['POST', 'GET'])
@login_required
def categorias():
    if request.method == "POST":
        nombre = request.form.get("nombre_categoria")
        descripcion = request.form.get("descripcion")

        if not nombre or not descripcion:
            flash("Error, campos vacios", "danger")
            return redirect("/categorias")
        
        try:
            nueva_categoria = Categoria(name=nombre, description=descripcion)
            db.session.add(nueva_categoria)
            db.session.commit() # para guardar y aplicar los cambios
        except IntegrityError:
            db.session.rollback()
            flash("La categoria existe", "danger")
            return redirect("/categorias")
        
        flash("Categoria creada", "success")
        return redirect("/")
            
    else:
        return render_template("categorias.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado la sesion", 'success')
    return redirect("/")

@app.route("/cursos")
@login_required
def cursos():
    # 1. Mostrar los datos con JSON
    cursos = Curso.query.all()
    cursos_data = []

    cursos_data = [curso.serialize() for curso in cursos]
    return jsonify(cursos_data),200

@app.route("/") # esto es un decorador
@login_required
def index():
    return render_template("index.html")

@app.route("/saludo/<nombre>")
def saludo(nombre):
    return f"Hola, {nombre}"
# LOGIN
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Campos vacios", "danger")
            return redirect("/login")
        
        usuario = Usuario.query.filter_by(email_user=email).first()
        
        if usuario is None:
            flash("Usuario no encontrado", 'danger')
            return redirect("/login")

        print(f"U: {usuario.password_hash}")

        if not check_password_hash(usuario.password_hash, password):
            flash("Contraseñas no coinciden", 'warning')
            return redirect("/login")
        
        # si todos los campos y validaciones estan correctos
        login_user(usuario)
        flash("Inicio de sesion exitoso", 'success')
        return redirect("/")
    else:
        return render_template("login.html")
    
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        rol = request.form.get("rol")

        print(f"{username, password}")
        # si los campos estan vacios
        if not username or not password:
            # es danger, porque es para errores
            flash("Campos vacios", "danger")
            return redirect("/register")
        
        # creamos un nuevo usuario
        # crear una password segura
        password_hash = generate_password_hash(password)
            
        try: 
            # si el usuario es nuevo
            new_user = Usuario(username=username, password_hash=password_hash, email_user=email, rol=rol)

            # guardamos a la base de datos con db
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("El usuario ya existe", 'danger')
            return redirect("/register")

        flash("Usuario registrado!", 'success ')
        return redirect("/")

    else:
        return render_template("register.html")

# READ, UPDATE DELETE
@app.route('/users')
def mostrar_usuarios():
    users = Usuario.query.all()
    print(f"Usuarios: {users}")
    return render_template("users.html", users=users)

@app.route('/user/<int:id>')
def mostrar_usuario(id):
    usuario = Usuario.query.get(id)
    return render_template("usuario.html", usuario=usuario)

@app.route('/eliminar', methods=['GET', 'POST'])
def eliminar_usuario():
    if request.method == "POST":
        username = request.form.get("username")
        usuario = Usuario.query.filter_by(username=username).first()

        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            flash("Usuario eliminado", "success")
            return redirect("/")
        else:
            db.session.rollback()
            flash("El usuario no existe", "danger")
            return redirect("/eliminar")
    else:
        return render_template("eliminar_usuario.html")

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

@app.route('/agregar', methods=['POST', 'GET'])
def agregar():
    if request.method == 'POST':
        titulo = request.form.get("titulo")
        contenido = request.form.get("contenido")
        categorias = request.form.getlist("categoria")

        if not titulo or not contenido or not categorias:
            flash("Campos vacios", "danger")
            return redirect("/agregar")
        
        try:
            nuevo_curso = Curso(title=titulo, description=contenido)
            
            for cat in categorias:
                print(f"dato: {cat}")
                categoria_id = Categoria.query.get(int(cat))
                nuevo_curso.categorias.append(categoria_id)
                print(f"Registro : {nuevo_curso.categorias}")
            
            db.session.add(nuevo_curso)
            db.session.commit() # confirmar el registro
        except Exception as e:
            print(f"El error fue: {e}")
            db.session.rollback()
            flash("Hubo un error", "danger")
            return redirect("/agregar")

        #print(f"T: {titulo} Cont: {contenido} Cat: {categorias}")
        
        flash("Curso creado", "success")
        return redirect("/")
    else:
        categorias_list = Categoria.query.all()
        print(f"{categorias_list}")
        return render_template("crear_curso.html", categorias=categorias_list)

if __name__ == '__main__':
    app.run(debug=True)