from flask import Flask, render_template, request, redirect, session
from serial_controller import enviar_comando
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = "smartcampus"

USUARIOS = {"admin":"123456","professor":"123456"}

def carregar_salas():
    with open("salas.json","r",encoding="utf-8") as f: return json.load(f)

def salvar_salas(salas):
    with open("salas.json","w",encoding="utf-8") as f: json.dump(salas,f,indent=4)

def carregar_historico():
    with open("historico.json","r",encoding="utf-8") as f: return json.load(f)

def salvar_historico(h):
    with open("historico.json","w",encoding="utf-8") as f: json.dump(h,f,indent=4)

@app.route("/", methods=["GET","POST"])
def login():
    if request.method=="POST":
        if request.form["usuario"] in USUARIOS and USUARIOS[request.form["usuario"]]==request.form["senha"]:
            session["usuario"]=request.form["usuario"]
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "usuario" not in session: return redirect("/")
    return render_template("dashboard.html", salas=carregar_salas())

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    if request.method=="POST":
        salas=carregar_salas()
        salas.append({"nome":request.form["nome"],"capacidade":request.form["capacidade"],"local":request.form["local"],"status":"Livre"})
        salvar_salas(salas)
        return redirect("/dashboard")
    return render_template("cadastro.html")

@app.route("/alterar/<int:id>/<status>")
def alterar(id,status):
    salas=carregar_salas()
    salas[id]["status"]=status
    salvar_salas(salas)
    h=carregar_historico()
    h.append({"data":datetime.now().strftime("%d/%m/%Y %H:%M"),"sala":salas[id]["nome"],"acao":status})
    salvar_historico(h)
    if status=="Livre": enviar_comando("L")
    elif status=="Reservada": enviar_comando("R")
    elif status=="Ocupada": enviar_comando("O")
    return redirect("/dashboard")

@app.route("/historico")
def historico():
    return render_template("historico.html", historico=carregar_historico())

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=False)
