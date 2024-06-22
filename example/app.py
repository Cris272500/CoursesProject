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

# main
if __name__ == '__main__':
    app.run(debug=True)