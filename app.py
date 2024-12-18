from flask import Flask, render_template, request, flash, jsonify,redirect, url_for
from crypto import enviar_dados
import json

app = Flask(__name__)
app.config["SECRET_KEY"] = "8jUCWYBssHyW72CkhmEWOw"

currentUser = " ";

@app.route("/", methods = ["POST", "GET"])
def home():   
        if request.method == 'POST':
            msg = request.form.get('optionsInput')
                           
            if msg == '1':
                return redirect("/signup")
            elif msg == '2':
                return redirect("/login")
            elif msg == '3':
                print("Você precisa fazer login primeiro")
                return redirect("/login")
            elif msg == '0':
                return redirect("/")
            else:
                print("Opção inválida. Tente novamente.")
                return render_template('index.html')
        else:
             return render_template('index.html')
            
@app.route("/signup", methods=['POST', 'GET'])
def criar_usuario():
    if request.method == 'POST':
        data = request.form
        nickname = data.get("User")
        senha = data.get("Pass")
        dados = {"flag": 3, "User": nickname, "Pass": senha}

        response = enviar_dados(dados)
        print(response)

        if (response):
            flash('User Created!', category='error')
            return redirect("/login")
        else:
            flash('Error. Try again.', category='error')
            return render_template('signUp.html')
    else:
        return render_template('signUp.html')

@app.route("/login", methods=['POST', 'GET'])
def autenticar_usuario():
    if request.method == 'POST':
        data = request.form
        nickname = data.get("User")
        senha = data.get("Pass")
        dados = {"flag": 0, "User": nickname, "Pass": senha}

        response = enviar_dados(dados)
        print(response)

        if (response):
            currentUser = nickname
            return redirect(url_for("enviar_mensagem", currentUser = currentUser, mensagens = response))
        else:
            flash('Error. Cant authenticate. Try again.', category='error')
            return render_template('login.html')

    else:
        return render_template("login.html")
    

@app.route("/messages", methods=['POST', 'GET'])
def enviar_mensagem():
    dados = {"flag": 1}
    #msgs = enviar_dados(dados)
    data = enviar_dados(dados)
    msgs = data
    print(msgs)
    currentUser = request.args.get('currentUser')
    if request.method == 'POST':
        data = request.form
        remetente = currentUser
        destinatario = data.get("destinatario")
        conteudo_email = request.form.get('messageInput')
        if conteudo_email:
            dados = {"flag": 1, "User": remetente, "destinatario": destinatario, "conteudo_email": conteudo_email}
            print(dados)
            response = enviar_dados(dados)

            print(response)
        
            if (response):
                
                return render_template('messages.html', currentUser = currentUser, msgs = msgs)
                
            else:
                flash('Error. Try again.', category='error')
                return render_template('messages.html', currentUser = currentUser, msgs = msgs)
        
    
    
    return render_template('messages.html', currentUser = currentUser, msgs = msgs)
