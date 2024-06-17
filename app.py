from flask import Flask, request, render_template, redirect, flash, session
from models import Usuario, db
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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Has cerrado la sesion", 'success')
    return redirect("/")

@app.route("/") # esto es un decorador
@login_required
def index():
    name = "Gabriel"
    edad = 25

    dinero = 200

    return render_template("index.html", name=name, edad=edad, dinero=dinero)

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
            new_user = Usuario(username=username, password_hash=password_hash, email_user=email)

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

@app.route("/about")
@login_required
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)