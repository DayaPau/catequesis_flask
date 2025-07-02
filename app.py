from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, DB_NAME

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/consultas')
def consultas():
    return render_template('consultas.html')

@app.route('/consultas/catequizados')
def listar_catequizados():
    personas = list(db.personas.find({"IdTipoPersona": 19, "Activo": True}))
    return render_template('listar_catequizados.html', personas=personas)

@app.route('/consultas/inscripciones')
def inscripciones():
    inscripciones = list(db.inscripciones.aggregate([
        { "$lookup": {
            "from": "grupos", "localField": "GrupoId", "foreignField": "GrupoId", "as": "grupo" }},
        { "$unwind": "$grupo" },
        { "$lookup": {
            "from": "niveles_catequesis", "localField": "NivelId", "foreignField": "IdNivel", "as": "nivel" }},
        { "$unwind": "$nivel" },
        { "$project": {
            "CatequizandoId": 1, "Estado": 1, "FechaInscripcion": 1,
            "Grupo": "$grupo.NombreGrupo", "Nivel": "$nivel.NombreNivel" }}
    ]))
    return render_template('inscripciones.html', inscripciones=inscripciones)

@app.route('/consultas/certificados')
def certificados():
    certificados = list(db.certificados.aggregate([
        { "$lookup": {
            "from": "personas", "localField": "PersonaId", "foreignField": "PersonaId", "as": "persona" }},
        { "$unwind": "$persona" },
        { "$project": {
            "CertificadoId": 1, "CodigoVerificacion": 1, "FechaEmision": 1,
            "Persona": { "$concat": ["$persona.Nombres", " ", "$persona.Apellidos"] },
            "SacramentoId": 1 }}
    ]))
    return render_template('certificados.html', certificados=certificados)

@app.route('/consultas/sacramentos')
def sacramentos():
    registros = list(db.sacramentos_registrados.aggregate([
        { "$lookup": {
            "from": "parroquias", "localField": "ParroquiaId", "foreignField": "ParroquiaId", "as": "parroquia" }},
        { "$unwind": "$parroquia" },
        { "$project": {
            "RegistroId": 1, "CatequizandoId": 1, "SacramentoId": 1,
            "Parroquia": "$parroquia.Nombre", "Oficiante": 1, "FechaCelebracion": 1 }}
    ]))
    return render_template('sacramentos.html', registros=registros)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    parroquias = list(db.parroquias.find({}, {"_id": 0, "ParroquiaId": 1, "Nombre": 1}))
    
    if request.method == 'POST':
        nueva_persona = {
            "PersonaId": int(request.form.get("PersonaId", 0)),
            "Nombres": request.form.get("Nombres", ""),
            "Apellidos": request.form.get("Apellidos", ""),
            "Cedula": request.form.get("Cedula", ""),
            "FechaNacimiento": request.form.get("FechaNacimiento", ""),
            "Genero": request.form.get("Genero", ""),
            "TelefonoPrincipal": request.form.get("TelefonoPrincipal", ""),
            "ParroquiaId": int(request.form.get("ParroquiaId", 0)),
            "IdTipoPersona": int(request.form.get("IdTipoPersona", 19)),
            "TieneBautismo": request.form.get("TieneBautismo") == "on",
            "Activo": True
        }
        db.personas.insert_one(nueva_persona)
        return redirect(url_for('listar_catequizados'))

    return render_template('registrar_catequizado.html', parroquias=parroquias)

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar(id):
    persona = db.personas.find_one({"_id": ObjectId(id)})
    parroquias = list(db.parroquias.find({}, {"_id": 0, "ParroquiaId": 1, "Nombre": 1}))
    
    if request.method == 'POST':
        db.personas.update_one(
            {"_id": ObjectId(id)},
            {"$set": {
                "Nombres": request.form.get("Nombres", ""),
                "Apellidos": request.form.get("Apellidos", ""),
                "Cedula": request.form.get("Cedula", ""),
                "FechaNacimiento": request.form.get("FechaNacimiento", ""),
                "Genero": request.form.get("Genero", ""),
                "TelefonoPrincipal": request.form.get("TelefonoPrincipal", ""),
                "ParroquiaId": int(request.form.get("ParroquiaId", 0)),
                "TieneBautismo": request.form.get("TieneBautismo") == "on"
            }}
        )
        return redirect(url_for('listar_catequizados'))
    
    return render_template('registrar_catequizado.html', persona=persona, parroquias=parroquias)

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar(id):
    db.personas.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('listar_catequizados'))

if __name__ == '__main__':
    app.run(debug=True)
