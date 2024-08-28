from flask import Flask, url_for, request, render_template, redirect 
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    conn.row_factory = sqlite3.Row  # Opcional: permite acessar colunas pelo nome
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM usuario")
    emails = cursor.fetchall()
    return render_template('pages/index.html', emails=emails)

@app.route('/update_user/<email>', methods=['POST'])
def update_user(email):
    conn = get_db_connection()
    cursor = conn.cursor()

    new_email = request.form['email']
    new_password = request.form['password']
    
    # Validação simples (verifique se os campos não estão vazios, por exemplo)
    if not new_email or not new_password:
        return "Email e senha são obrigatórios.", 400

    # Atualiza o usuário no banco de dados
    cursor.execute("""
        UPDATE usuario
        SET email = ?, senha = ?
        WHERE email = ?
    """, (new_email, new_password, email))
    
    conn.commit()
    conn.close()
    
    return redirect(url_for('user_page', email=new_email))

@app.route('/user/<email>')
def user_page(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuario WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return render_template('pages/user.html', user=user)
    else:
        return "Usuário não encontrado", 404

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            # Obtendo dados do formulário
            email = request.form['email']
            senha = request.form['password']
            
            #conexao
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Inserindo dados na tabela
            sql = "INSERT INTO usuario (email, senha) VALUES (?, ?)"
            cursor.execute(sql, (email, senha))
            conn.commit()
            
            return redirect('/')
        except KeyError as e:
            return f"Campo ausente: {str(e)}", 400
        finally:
            conn.close()  # Fechar a conexão
    else:
        return render_template('pages/register.html')
    
@app.route("/create_database")
def create_database():
    db = 'database.sqlite'
    schema = 'database/schema.sql'
    
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    
    with open(schema, 'r') as banco:
        schema_sql = banco.read()
        cursor.executescript(schema_sql)
    return 'BANCO CRIADO'


if __name__ == '__main__':
    app.run(debug=True)