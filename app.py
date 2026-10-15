meu_projeto/
├── app.py
└── templates/
    ├── base.html
    ├── loja.html
    ├── carrinho.html
    ├── login.html
    └── admin.html
    from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "chave_secreta_hutti_furts_2026"

# Credenciais do Administrador
ADMIN_USER = "Felipe"
ADMIN_PASS = "123456789"

# Catálogo em memória
catalogo = {
    "Frutas": {
        "Maçã": 6.50,
        "Banana": 4.50,
        "Morango (Caixa)": 9.00,
        "Manga": 7.00,
        "Abacaxi": 8.50
    },
    "Carnes": {
        "Alcatra Bovina (kg)": 42.00,
        "Peito de Frango (kg)": 19.90,
        "Lombo Suíno (kg)": 24.50,
        "Carne Moída (kg)": 32.00
    },
    "Gelados": {
        "Sorvete de Chocolate (1L)": 22.00,
        "Sorvete de Morango (1L)": 22.00,
        "Açaí Tradicional (1L)": 26.00,
        "Picolé de Frutas": 4.00
    }
}

# Inicializa carrinho na sessão do usuário
def obter_carrinho():
    if "carrinho" not in session:
        session["carrinho"] = []
    return session["carrinho"]

# Rota principal - Loja
@app.route("/")
def loja():
    carrinho = obter_carrinho()
    total_itens = sum(item["quantidade"] for item in carrinho)
    return render_template("loja.html", catalogo=catalogo, total_itens=total_itens)

# Adicionar item ao carrinho
@app.route("/adicionar", methods=["POST"])
def adicionar_carrinho():
    categoria = request.form.get("categoria")
    produto_nome = request.form.get("produto")
    
    try:
        quantidade = float(request.form.get("quantidade", 1))
        if quantidade <= 0:
            raise ValueError()
    except ValueError:
        flash("Informe uma quantidade válida superior a 0.", "danger")
        return redirect(url_for("loja"))

    if categoria in catalogo and produto_nome in catalogo[categoria]:
        preco_unit = catalogo[categoria][produto_nome]
        subtotal = preco_unit * quantidade

        carrinho = obter_carrinho()
        
        # Se o item já estiver no carrinho, atualiza a quantidade
        encontrado = False
        for item in carrinho:
            if item["produto"] == produto_nome:
                item["quantidade"] += quantidade
                item["subtotal"] = item["quantidade"] * item["preco_unit"]
                encontrado = True
                break
        
        if not encontrado:
            carrinho.append({
                "produto": produto_nome,
                "preco_unit": preco_unit,
                "quantidade": quantidade,
                "subtotal": subtotal
            })
            
        session.modified = True
        flash(f"{quantidade}x {produto_nome} adicionado(s) ao carrinho!", "success")

    return redirect(url_for("loja"))

# Visualizar Carrinho
@app.route("/carrinho")
def ver_carrinho():
    carrinho = obter_carrinho()
    total = sum(item["subtotal"] for item in carrinho)
    return render_template("carrinho.html", carrinho=carrinho, total=total)

# Esvaziar Carrinho
@app.route("/limpar", methods=["POST"])
def limpar_carrinho():
    session["carrinho"] = []
    flash("Carrinho esvaziado com sucesso.", "info")
    return redirect(url_for("ver_carrinho"))

# Tela de Login do Administrador
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form.get("usuario")
        senha = request.form.get("senha")

        if usuario == ADMIN_USER and senha == ADMIN_PASS:
            session["admin_logado"] = True
            flash("Login efetuado com sucesso!", "success")
            return redirect(url_for("admin"))
        else:
            flash("Usuário ou senha incorretos!", "danger")

    return render_template("login.html")

# Logout do Admin
@app.route("/logout")
def logout():
    session.pop("admin_logado", None)
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for("loja"))

# Painel Administrativo
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("admin_logado"):
        flash("Acesso restrito. Faça login primeiro.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        acao = request.form.get("acao")
        
        if acao == "alterar":
            cat = request.form.get("categoria")
            prod = request.form.get("produto")
            try:
                novo_preco = float(request.form.get("preco"))
                if cat in catalogo and prod in catalogo[cat]:
                    catalogo[cat][prod] = novo_preco
                    flash(f"Preço de '{prod}' alterado para R$ {novo_preco:.2f}!", "success")
            except ValueError:
                flash("Preço inválido.", "danger")
                
        elif acao == "adicionar":
            cat = request.form.get("categoria")
            novo_prod = request.form.get("novo_produto")
            try:
                preco = float(request.form.get("novo_preco"))
                if cat in catalogo and novo_prod:
                    catalogo[cat][novo_prod] = preco
                    flash(f"Produto '{novo_prod}' cadastrado em {cat}!", "success")
            except ValueError:
                flash("Valor numérico inválido para o preço.", "danger")

    return render_template("admin.html", catalogo=catalogo)

if __name__ == "__main__":
    app.run(debug=True)
