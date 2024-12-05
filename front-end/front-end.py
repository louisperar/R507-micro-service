from flask import Flask, jsonify, request, render_template
import requests
app = Flask(__name__)


@app.route("/", methods=["GET"])
def accueil():
    return render_template('accueil.html.j2')

@app.route("/utilisateurs", methods=["GET"])
def utilisateurs():
    reponse = requests.get("http://api:5002/utilisateurs")
    data = reponse.json()
    return data

@app.route("/livres", methods=["GET"])
def livres():
    reponse = requests.get("http://api:5002/livres")
    data = reponse.json()
    return data

@app.route("/auteurs", methods=["GET"])
def auteurs():
    reponse = requests.get("http://api:5002/auteurs")
    data = reponse.json()
    return data

@app.route("/utilisateur/<utilisateur>", methods=["GET"])
def affiche_utilisateur(utilisateur):
    try:
        utilisateur = int(utilisateur)
    except ValueError:
        utilisateur = str(utilisateur)
    reponse = requests.get("http://api:5002/utilisateur/"+utilisateur)
    data = reponse.json()
    return data
    
@app.route("/utilisateur/emprunt/<utilisateur>", methods=["GET"])
def affiche_emprunt_utilisateur(utilisateur):
    try:
        utilisateur = int(utilisateur)
    except ValueError:
        utilisateur = str(utilisateur)
    reponse = requests.get("http://api:5002/utilisateur/emprunt/"+utilisateur)
    data = reponse.json()
    return data

@app.route("/livres/siecle/<numero>", methods=["GET"])
def affiche_siecle(numero):
    try:
        numero = int(numero)
    except ValueError:
        return "Rentrez un nombre"
    reponse = requests.get("http://api:5002/livres/siecle/"+numero)
    data = reponse.json()
    return data

@app.route("/livres/ajouter", methods=["GET"])
def ajoute_livre():
    return render_template('index.html.j2')

if __name__ == '__main__':
    app.run(port = 5002, debug=True)