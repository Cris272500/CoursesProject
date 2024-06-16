from flask import Flask, request, render_template, redirect, flash, session
from models import Usuario, db
# con eso importamos la password hasheada
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config
from flask_session import Session

app = Flask(__name__)
app.config.from_object(Config)

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

db.init_app(app)

@app.route("/") # esto es un decorador
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
        name = request.form.get("nombre")
        print(f"Hola {name}")
        return f"Hola {name}"
    else:
        return render_template("index.html")
    
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

        # si el usuario ya existe
        usuario_existente = Usuario.query.filter_by(username=username).first()

        if usuario_existente:
            flash("El usuario ya existe", 'danger')
            return redirect("/register")
        
        # si el usuario es nuevo
        new_user = Usuario(username=username, password_hash=password_hash, email_user=email)

        # guardamos a la base de datos con db
        db.session.add(new_user)
        db.session.commit()

        flash("Usuario registrado!", 'success ')
        return redirect("/")

    else:
        return render_template("register.html")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)