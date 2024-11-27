"""
Faites l'API avec les "endpoints" suivants :

1. Check Chemins `/utilisateurs`, `/livres`, `/auteurs` : renvoient la liste en JSON des tables complètes
1. Check Chemin `/utilisateur/<utilisateur>` : renvoie le dictionnaire correspondant à l'utilisateur d'id `utilisateur` ou par l'utilisateur de nom `utilisateur` si un seul utilisateur porte ce nom-là. Si plusieurs portent le même nom, une erreur est renvoyée.
1. Check Chemin `/utilisateur/emprunts/<utilisateur>` : renvoie la liste des livres empruntés par l'utilisateur d'id `utilisateur` ou par l'utilisateur de nom `utilisateur` si un seul utilisateur porte ce nom-là.
1. Check Chemin `/livres/siecle/<numero>` : renvoie la liste des livres du siècle marqué.
1. Check Chemin `/livres/ajouter` : en POST ajoute un livre au format identique au fichier JSON (si l'auteur n'existe pas encore il est ajouté)
1. Chemin `/utilisateur/ajouter` : en POST ajoute un utilisateur (format {"nom": nom_user, "email": email_user})
1. Chemin `/utilisateur/<utilisateur>/supprimer` : en DELETE
1. Chemin `/utilisateur/{utilisateur_id}/emprunter/{livre_id}` : en PUT, permet d'emprunter un livre
1. Chemin `/utilisateur/{utilisateur_id}/rendre/{livre_id}` : en PUT, permet de rendre un livre
"""
# Votre code ici...
from flask import Flask, jsonify, request, render_template
import requests
app = Flask(__name__)


@app.route("/", methods=["GET"])
def accueil():
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    return data
    #return render_template('accueil.html.j2')

@app.route("/utilisateurs", methods=["GET"])
def utilisateurs():
    liste_utilisateurs = cur.execute("SELECT * FROM utilisateurs").fetchall()
    return jsonify(liste_utilisateurs)

@app.route("/livres", methods=["GET"])
def livres():
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    liste_livre = cur.execute("SELECT * FROM livres").fetchall()
    return jsonify(liste_livre)

@app.route("/auteurs", methods=["GET"])
def auteurs():
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    liste_auteur = cur.execute("SELECT * FROM auteurs").fetchall()
    return jsonify(liste_auteur)

@app.route("/utilisateur/<utilisateur>", methods=["GET"])
def affiche_utilisateur(utilisateur):
    try:
        utilisateur = int(utilisateur)
    except ValueError:
        utilisateur = str(utilisateur)
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    if type(utilisateur) == str:
        utilisateur = cur.execute("SELECT * FROM utilisateurs WHERE nom = ?", (utilisateur,)).fetchall()
        return jsonify(utilisateur)
    elif type(utilisateur) == int:
        utilisateurs = cur.execute("SELECT * FROM utilisateurs WHERE id = ?", (utilisateur,)).fetchall()
        return jsonify(utilisateurs)
    
@app.route("/utilisateur/emprunt/<utilisateur>", methods=["GET"])
def affiche_emprunt_utilisateur(utilisateur):
    try:
        utilisateur = int(utilisateur)
    except ValueError:
        utilisateur = str(utilisateur)
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    if type(utilisateur) == str:
        cur.execute("SELECT id FROM utilisateurs WHERE nom = ?", (utilisateur,))
        for i in cur.fetchall() :
            livre = cur.execute("SELECT * FROM livres WHERE emprunteur_id = ?", (i[0],)).fetchall()
            return jsonify(livre)
    elif type(utilisateur) == int:
        utilisateurs = cur.execute("SELECT * FROM livres WHERE emprunteur_id = ?", (utilisateur,)).fetchall()
        return jsonify(utilisateurs)

@app.route("/livres/siecle/<numero>", methods=["GET"])
def affiche_siecle(numero):
    try:
        numero = int(numero)
    except ValueError:
        return "Rentrez un nombre"
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    livre=[]
    numero=str(numero).split()
    numero=numero[0][:2]
    for i in cur.execute("SELECT * FROM livres").fetchall():
        date = str(i[4])
        siecle = date.split("/")[2][:2]
        if siecle == numero:
            livre.append(cur.execute("SELECT * FROM livres WHERE date_public = ?", (date,)).fetchall())
    return jsonify(livre)

@app.route("/livres/ajouter", methods=["GET"])
def ajoute_livre():
    return render_template('index.html.j2')

@app.route("/livres/ajouter/affichage", methods=["POST"])
def verif_ajoute_livre():
    reponse = requests.get("http://api:5002")
    data = reponse.json()
    titre = request.form.get('titre')
    pitch = request.form.get('pitch')
    auteur = request.form.get('auteur')
    date = request.form.get('date')
    id_auteur=""
    for i in cur.execute("SELECT * FROM auteurs"):
        if auteur == i[1]:
            id_auteur = cur.execute("SELECT id FROM auteurs WHERE nom_auteur = ?", (auteur,)).fetchall()
        if auteur != i[1]:
            cur.execute("INSERT INTO auteurs (nom_auteur) VALUES (?)", (auteur,))
            conn.commit()
            id_auteur = cur.execute("SELECT id FROM auteurs WHERE nom_auteur = ?", (auteur,)).fetchall()
    for i in id_auteur:
        cur.execute("INSERT INTO livres (titre, pitch, auteur_id, date_public) VALUES (?, ?, ?, ?)", (titre, pitch, i[0], date))
        conn.commit()
    return render_template('ajout_livre.html.j2', titre=titre, pitch=pitch, auteur=auteur, date=date)


if __name__ == '__main__':
    app.run(port = 5000, debug=True)