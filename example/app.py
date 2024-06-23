from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# RUTA INDEX
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        pass
    else:
        return render_template("register.html")

@app.route("/crear", methods=["POST", "GET"])
def crear():
    if request.method == "POST":
        pass
    else:
        return render_template("create.html")

@app.route("/cursos", methods=['POST', 'GET'])
def cursos():
    if request.method == 'POST':
        pass
    else:
        return render_template("cursos.html")

@app.route("/curso_detalle", methods=['POST', 'GET'])
def curso_detalle():
    if request.method == 'POST':
        pass
    else:
        return render_template("curso_detail.html")
    
# main
if __name__ == '__main__':
    app.run(debug=True)