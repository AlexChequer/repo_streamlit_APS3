from flask import Flask, request
from flask_pymongo import PyMongo, ObjectId
from dotenv import load_dotenv
from bson import ObjectId
from bson.errors import InvalidId
import os

app = Flask(__name__)
load_dotenv('.cred')
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'localhost')
mongo = PyMongo(app)


# USUARIOS 

# Get all usuarios
@app.route('/usuarios', methods=['GET'])
def get_usuarios():

    filtro = {}
    projecao = {"_id" : 0}

    usuario = mongo.db.usuarios.find(filtro, projecao)
    usuarios_list = list(usuario)

    if usuario == None:
        return {"erro": "Nenhum usuário encontrado"}, 404
    
    # Convert ObjectId to string
    for usuario in usuarios_list:
        if '_id' in usuario:
            usuario['_id'] = str(usuario['_id'])

    
    resp = {
        "usuarios": usuarios_list
    }
    
    return resp, 200



# Get one usuario
@app.route('/usuarios/<string:cpf>', methods=['GET'])
def get_usuario(cpf):
    filtro = {"cpf": cpf}
    projecao = {"_id" : 0}

    usuario = mongo.db.usuarios.find_one(filtro, projecao)

    if usuario == None:
        return {"erro": "Usuário não encontrado"}, 404
    
    return {"usuario": usuario}, 200


# Create usuario
@app.route('/usuarios', methods=['POST'])
def post_usuario():

    dados = request.json

    cpf = dados.get('cpf')
    nome = dados.get('nome')
    data_nascimento = dados.get('data_nascimento')

    if cpf == None or nome == None or data_nascimento == None:
        return {"erro": "Todos os campos são obrigatórios"}, 400

    
    # Verifica se o CPF já existe
    usuario_existente = mongo.db.usuarios.find_one({"cpf": cpf})
    if usuario_existente:
        return {"erro": "CPF já cadastrado"}, 400


    usuario_novo = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "emprestimos": []
    }


    x = mongo.db.usuarios.insert_one(usuario_novo)

    if x.inserted_id == None:
        return {"erro": "Erro ao cadastrar usuário"}, 400
    
    usuario_novo_id = str(x.inserted_id)

    return {"Usuario inserido com sucesso! ID": usuario_novo_id}, 201



# Update usuario
@app.route('/usuarios/<string:cpf>', methods=['PUT'])
def put_usuario(cpf):

    dados = request.json

    nome = dados.get('nome')
    cpf_novo = dados.get('cpf')
    data_nascimento = dados.get('data_nascimento')

    usuario_novo = {
        "nome": nome,
        "cpf": cpf_novo,
        "data_nascimento": data_nascimento
    }

    query = {"cpf": cpf}
    novos_valores = {"$set": usuario_novo}

 
    x = mongo.db.usuarios.update_one(query, novos_valores)

    filtro = {"cpf": cpf_novo}
    projecao = {"_id" : 1}

    usuario_id = mongo.db.usuarios.find_one(filtro, projecao)

    
    if x.modified_count == 0:
        return {"erro": "Usuário não encontrado"}, 404

    return {"sucesso": f'Usuario de ID: {usuario_id} com sucesso!'}, 201
  
  
# Delete usuario
@app.route('/usuarios/<string:cpf>', methods=['DELETE'])
def delete_usuario(cpf):
    
        query = {"cpf": cpf}
    
        x = mongo.db.usuarios.delete_one(query)
    
        if x.deleted_count == 0:
            return {"erro": "Usuário não encontrado"}, 404
    
        return {"sucesso": "Usuário deletado com sucesso!"}, 200



#BICICLETA -----------------------------------------------------------------------------------------------------------

@app.route('/bicicletas', methods=['GET'])
def get_bicicletas():

    filtro = {}
    projecao = {"_id" : 0}

    bicicleta = mongo.db.bicicletas.find(filtro, projecao)

    if bicicleta == None:
        return {"erro": "Nenhuma bicicleta encontrado"}, 404
    
    resp = {
        "bicicletas": list(bicicleta)
    }
    
    return resp, 200



# Get one bicicleta
@app.route('/bicicletas/<string:id>', methods=['GET'])
def get_bicicleta_id(id):

    filtro = {"_id": ObjectId(id)}
    projecao = {"_id" : 0}

    bicicleta = mongo.db.bicicletas.find_one(filtro, projecao)

    if bicicleta == None:
        return {"erro": "Bicicleta não encontrada"}, 404
    
    return {"bicicleta": bicicleta}, 200


# Create bicicleta
@app.route('/bicicletas', methods=['POST'])
def post_bicicleta():

    dados = request.json

    marca = dados.get('marca')
    modelo = dados.get('modelo')
    cidade = dados.get('cidade')

    if marca == None or modelo == None or cidade == None:
        return {"erro": "Todos os campos são obrigatórios"}, 400
    



    bicicleta_novo = {
        "marca": marca,
        "modelo": modelo,
        "cidade": cidade,
        "status": "disponivel"
    }


    x = mongo.db.bicicletas.insert_one(bicicleta_novo)

    if x.inserted_id == None:
        return {"erro": "Erro ao cadastrar bicicleta"}, 400
    
    bicicleta_novo_id = str(x.inserted_id)

    return {"Bicicleta inserido com sucesso! ID": bicicleta_novo_id}, 201


# Update bicicleta
@app.route('/bicicletas/<string:id>', methods=['PUT'])
def put_bicicleta(id):

    dados = request.json

    marca = dados.get('marca')
    modelo = dados.get('modelo')
    cidade = dados.get('cidade')
    status = dados.get('status')

    bicicleta_novo = {
        "marca": marca,
        "modelo": modelo,
        "cidade": cidade,
        "status": status
    }

    query = {"_id": ObjectId(id)}
    novos_valores = {"$set": bicicleta_novo}

 
    x = mongo.db.bicicletas.update_one(query, novos_valores)
    
    if x.modified_count == 0:
        return {"erro": "Bicicleta não encontrada"}, 404

    return {"sucesso": "Bicicleta atualizada com sucesso!"}, 201


# Delete bicicleta
@app.route('/bicicletas/<string:id>', methods=['DELETE'])
def delete_bicicleta(id):
    
        query = {"_id": ObjectId(id)}
    
        x = mongo.db.bicicletas.delete_one(query)
    
        if x.deleted_count == 0:
            return {"erro": "Bicicleta não encontrada"}, 404
    
        return {"sucesso": "Bicicleta deletada com sucesso!"}, 200


# EMPRESTIMOS -----------------------------------------------------------------------------------------------------------

# Get all emprestimos
@app.route('/emprestimos', methods=['GET'])
def get_emprestimos():
    usuarios_cursor = mongo.db.usuarios.find({}, {"_id": 1, "emprestimos": 1})
    emprestimos_list = []

    for usuario in usuarios_cursor:
        user_id = usuario['_id']
        emprestimos = usuario.get('emprestimos', [])
        for emprestimo in emprestimos:
            emprestimos_list.append({
                "emprestimo_id": str(emprestimo['emprestimo_id']),
                "user_id": str(user_id),
                "bike_id": str(emprestimo['bike_id'])
            })

    if not emprestimos_list:
        return {"erro": "Nenhum empréstimo encontrado"}, 404

    return {"emprestimos": emprestimos_list}, 200


# Get one emprestimo
@app.route('/emprestimos/<string:emprestimo_id>', methods=['GET'])
def get_emprestimo_id(emprestimo_id):
    usuario_especifico = mongo.db.usuarios.find({}, {"_id": 1, "emprestimos": 1})
    emprestimos_list = []

    for usuario in usuario_especifico:
        user_id = usuario['_id']
        emprestimos = usuario.get('emprestimos', [])
        for emprestimo in emprestimos:
            if emprestimo['emprestimo_id'] == ObjectId(emprestimo_id):
                emprestimos_list.append({ {
                    "emprestimo_id": str(emprestimo['emprestimo_id']),
                    "user_id": str(user_id),
                    "bike_id": str(emprestimo['bike_id'])
                }})

    if not emprestimos_list:
        return {"erro": "Empréstimo não encontrado"}, 404

    return {"emprestimos": emprestimos_list}, 200


# Post emprestimo
@app.route('/emprestimos/usuarios/<string:id_usuario>/bicicletas/<string:bike_id>', methods=['POST'])
def post_emprestimo(id_usuario, bike_id):
    # Validar id_usuario
    try:
        usuario_object_id = ObjectId(id_usuario)

    except InvalidId:
        return {"erro": "ID de usuário inválido"}, 400

    # Validar bike_id
    try:
        bicicleta_object_id = ObjectId(bike_id)
    except InvalidId:
        return {"erro": "ID de bicicleta inválido"}, 400

    # Checar se usuario existe
    user = mongo.db.usuarios.find_one({"_id": usuario_object_id})
    if not user:
        return {"erro": "Usuário não encontrado"}, 404

    # Checar se bicicleta existe
    bike = mongo.db.bicicletas.find_one({"_id": bicicleta_object_id})
    if not bike:
        return {"erro": "Bicicleta não encontrada"}, 404

    # Checar se bicicleta está disponível
    if bike.get('status') != "disponivel":
        return {"erro": "Bicicleta não está disponível"}, 400

    # Gerar emprestimo ID
    emprestimo_id = ObjectId()
    emprestimo_id_str = str(emprestimo_id)

    data = request.json
    data_emprestimo = data.get('data_emprestimo')

    # Entrada de emprestimo
    emprestimo_entry = {
        "emprestimo_id": emprestimo_id_str,
        "bike_id": str(bicicleta_object_id),
        "data_emprestimo": data_emprestimo
    }

    # Atualiza usuario com novo emprestimo
    update_result = mongo.db.usuarios.update_one(
        {"_id": usuario_object_id},
        {"$push": {"emprestimos": emprestimo_entry}}
    )

    if update_result.modified_count == 0:
        return {"erro": "Erro ao registrar empréstimo no usuário"}, 400

    # Atualiza status da bicicleta para em uso
    mongo.db.bicicletas.update_one({"_id": bicicleta_object_id}, {"$set": {"status": "em uso"}})

    return {"sucesso": f"Empréstimo registrado com sucesso! ID: {emprestimo_id_str}"}, 201


# Deletar emprestimo
@app.route('/emprestimos/<string:emprestimo_id>', methods=['DELETE'])
def delete_emprestimo(emprestimo_id):
    
    # Encontrar usuario do emprestimo
    user = mongo.db.usuarios.find_one({
        "emprestimos.emprestimo_id": emprestimo_id
    }, {"_id": 1, "emprestimos.$": 1})

    if not user:
        return {"erro": "Empréstimo não encontrado"}, 404

    emprestimo = user['emprestimos'][0]
    bike_id = emprestimo['bike_id']

    # Remover emprestimo do array do usuario
    update_result = mongo.db.usuarios.update_one(
        {"_id": user['_id']},
        {"$pull": {"emprestimos": {"emprestimo_id": emprestimo_id}}}
    )

    if update_result.modified_count == 0:
        return {"erro": "Erro ao deletar empréstimo do usuário"}, 400

    # Mudar status da bicicleta de volta pra disponivel
    mongo.db.bicicletas.update_one({"_id": bike_id}, {"$set": {"status": "disponivel"}})

    return {"sucesso": "Empréstimo deletado e bicicleta devolvida com sucesso!"}, 200


if __name__ == '__main__':
    app.run(debug=True)
