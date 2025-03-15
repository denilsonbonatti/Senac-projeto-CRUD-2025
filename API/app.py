from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS


app = Flask(__name__)

CORS(app)

# Configuração do banco de dados MySQL
app.config['MYSQL_HOST'] = '40.78.42.232'
app.config['MYSQL_USER'] = 'App'
app.config['MYSQL_PASSWORD'] = 'Senha123'
app.config['MYSQL_DB'] = 'EMPRESA'

mysql = MySQL(app)

# Rota para consultar todos os registros
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome, cargo, email FROM adm_users")
        dados = cur.fetchall()
        cur.close()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para consultar um usuário pelo ID
@app.route('/usuarios/<int:id>', methods=['GET'])
def obter_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, nome, cargo, email FROM adm_users WHERE id = %s", (id,))
        dado = cur.fetchone()
        cur.close()
        
        if dado:
            # Verificação adicional para garantir que 'dado' é uma tupla
            if isinstance(dado, tuple):
                # Converta a tupla para um dicionário para facilitar o retorno em JSON
                usuario = {
                    'id': dado[0],
                    'nome': dado[1],
                    'cargo': dado[2],
                    'email': dado[3]
                }
                return jsonify(usuario), 200
            else:
                return jsonify({'mensagem': 'Erro inesperado: dado não é uma tupla'}), 500
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500


# Rota para verificar se um usuário existe pelo e-mail e senha
@app.route('/usuarios/login', methods=['POST'])
def verificar_usuario():
    dados = request.json
    email = dados.get('email')
    senha = dados.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Email e senha são obrigatórios'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id FROM adm_users WHERE email = %s AND senha = %s", (email, senha))
        usuario = cur.fetchone()
        cur.close()
        
        if usuario:
            return jsonify({'mensagem': 'Login bem-sucedido'})
        else:
            return jsonify({'mensagem': 'Usuário ou senha inválidos'}), 401
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para incluir um novo usuário
@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    dados = request.json
    nome = dados.get('nome')
    cargo = dados.get('cargo')
    email = dados.get('email')
    senha = dados.get('senha')

    if not nome or not cargo or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO adm_users (nome, cargo, email, senha) VALUES (%s, %s, %s, %s)",
                    (nome, cargo, email, senha))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para atualizar um usuário existente
@app.route('/usuarios/<int:id>', methods=['PUT'])
def atualizar_usuario(id):
    dados = request.json
    nome = dados.get('nome')
    cargo = dados.get('cargo')
    email = dados.get('email')
    senha = dados.get('senha')

    if not nome or not cargo or not email or not senha:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE adm_users SET nome=%s, cargo=%s, email=%s, senha=%s WHERE id=%s",
                    (nome, cargo, email, senha, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário atualizado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para deletar um usuário
@app.route('/usuarios/<int:id>', methods=['DELETE'])
def deletar_usuario(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM adm_users WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Usuário deletado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
