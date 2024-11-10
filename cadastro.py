from flask import Flask, render_template, request, redirect, url_for, flash
import re

app = Flask(__name__)
app.secret_key = 'chave_secreta_para_sessoes'

# Função para validar e-mail com expressão regular
def validar_email(email):
    padrao = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(padrao, email) is not None

# Rota para o formulário de cadastro e a lista de usuários
@app.route('/')
def cadastro():
    # Carregar dados do arquivo
    usuarios = []
    try:
        with open('cadastros.txt', 'r') as f:
            for linha in f:
                nome, email = linha.strip().split(',')
                usuarios.append({'nome': nome, 'email': email})
    except FileNotFoundError:
        pass
    return render_template('cadastro.html', usuarios=usuarios)

# Rota para processar o formulário de cadastro
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        nome = request.form['nome']
        email = request.form['email']
        
        if not validar_email(email):
            flash("E-mail inválido. Tente novamente.", "error")
            return redirect(url_for('cadastro'))

        # Salvar dados no arquivo
        with open('cadastros.txt', 'a') as f:
            f.write(f"{nome},{email}\n")

        flash("Cadastro realizado com sucesso!", "success")
        return redirect(url_for('cadastro'))

    except KeyError as e:
        flash(f"Erro no campo: {e}", "error")
        return redirect(url_for('cadastro'))

# Rota para a busca de usuários
@app.route('/buscar', methods=['GET'])
def buscar():
    query = request.args.get('query', '').lower()
    usuarios_filtrados = []
    try:
        with open('cadastros.txt', 'r') as f:
            for linha in f:
                nome, email = linha.strip().split(',')
                if query in nome.lower():
                    usuarios_filtrados.append({'nome': nome, 'email': email})
    except FileNotFoundError:
        pass
    return render_template('cadastro.html', usuarios=usuarios_filtrados, query=query)

if __name__ == '__main__':
    app.run(debug=True)
