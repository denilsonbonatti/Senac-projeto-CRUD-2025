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
            return jsonify({'mensagem': 'Usuário não encontrado'}), 401
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
    
# Rota para listar todos os produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, produto, quantidade, imagem, validade FROM produtos")
        dados = cur.fetchall()
        cur.close()
        return jsonify(dados)
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para consultar um produto pelo ID
@app.route('/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT id, produto, quantidade, imagem, validade FROM produtos WHERE id = %s", (id,))
        dado = cur.fetchone()
        cur.close()
        
        if dado:
            produto = {
                'id': dado[0],
                'produto': dado[1],
                'quantidade': dado[2],
                'imagem': dado[3],
                'validade': dado[4]
            }
            return jsonify(produto), 200
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para adicionar um novo produto
@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.json
    produto = dados.get('produto')
    quantidade = dados.get('quantidade')
    imagem = dados.get('imagem')
    validade = dados.get('validade')
    
    if not produto or not quantidade or not imagem or not validade:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO produtos (produto, quantidade, imagem, validade) VALUES (%s, %s, %s, %s)",
                    (produto, quantidade, imagem, validade))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Produto criado com sucesso'}), 201
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500


# Rota para atualizar um produto existente
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    dados = request.json
    produto = dados.get('produto')
    quantidade = dados.get('quantidade')
    imagem = dados.get('imagem')
    validade = dados.get('validade')
    
    if not produto or not quantidade or not imagem or not validade:
        return jsonify({'mensagem': 'Todos os campos são obrigatórios'}), 400
    
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE produtos SET produto=%s, quantidade=%s, imagem=%s, validade=%s WHERE id=%s",
                    (produto, quantidade, imagem, validade, id))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Produto atualizado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

# Rota para deletar um produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM produtos WHERE id = %s", (id,))
        mysql.connection.commit()
        cur.close()
        return jsonify({'mensagem': 'Produto deletado com sucesso'})
    except Exception as e:
        return jsonify({'mensagem': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
