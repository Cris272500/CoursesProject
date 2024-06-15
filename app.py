from flask import Flask, request, render_template, redirect

app = Flask(__name__)

empleados = [ # "CONSULTA A BASE DE DATOS"
    {
        "id": 1,
        "nombre": "Juan Pérez",
        "edad": 28,
        "departamento": "Ventas",
        "salario": 35000,
        "fecha_contratacion": "2019-04-21"
    },
    {
        "id": 2,
        "nombre": "María López",
        "edad": 34,
        "departamento": "Marketing",
        "salario": 42000,
        "fecha_contratacion": "2018-07-14"
    },
    {
        "id": 3,
        "nombre": "Carlos Sánchez",
        "edad": 45,
        "departamento": "Finanzas",
        "salario": 58000,
        "fecha_contratacion": "2012-01-12"
    },
    {
        "id": 4,
        "nombre": "Ana Torres",
        "edad": 30,
        "departamento": "Recursos Humanos",
        "salario": 39000,
        "fecha_contratacion": "2020-09-01"
    },
    {
        "id": 5,
        "nombre": "Luis Gómez",
        "edad": 25,
        "departamento": "IT",
        "salario": 45000,
        "fecha_contratacion": "2021-11-11"
    }
]

@app.route("/") # esto es un decorador
def index():
    name = "Gabriel"
    edad = 25

    dinero = 200

    return render_template("index.html", name=name, edad=edad, dinero=dinero, empleados=empleados)

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

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == '__main__':
    app.run(debug=True)