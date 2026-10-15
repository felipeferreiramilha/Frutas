from flask import Flask, render_template_string, request, redirect, url_for, session, flash

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

# Template HTML base único
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hutti Furts & Lázaro e Vladimir Frutamania</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px; color: #333; }
        .container { max-width: 950px; margin: 0 auto; background: #ffffff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.08); }
        header { text-align: center; margin-bottom: 25px; border-bottom: 2px solid #e9ecef; padding-bottom: 15px; }
        h1 { color: #2c3e50; margin: 0; font-size: 28px; }
        h3 { color: #27ae60; margin: 5px 0 0 0; font-weight: 500; }
        nav { display: flex; justify-content: center; gap: 12px; margin-bottom: 25px; background: #eef2f7; padding: 12px; border-radius: 8px; }
        nav a { text-decoration: none; color: #34495e; font-weight: 600; padding: 8px 16px; border-radius: 6px; transition: 0.2s; }
        nav a:hover { background-color: #27ae60; color: white; }
        .alert { padding: 12px 18px; border-radius: 6px; margin-bottom: 20px; font-weight: 500; }
        .alert-success { background-color: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .alert-danger { background-color: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .alert-warning { background-color: #fff3cd; color: #856404; border: 1px solid #ffeeba; }
        .alert-info { background-color: #d1ecf1; color: #0c5460; border: 1px solid #bee5eb; }
        table { width: 100%; border-collapse: collapse; margin-top: 15px; }
        th, td { padding: 12px; border-bottom: 1px solid #dee2e6; text-align: left; }
        th { background-color: #f1f3f5; color: #495057; }
        .btn { background-color: #27ae60; color: white; border: none; padding: 9px 15px; border-radius: 5px; cursor: pointer; font-weight: 600; text-decoration: none; display: inline-block; }
        .btn:hover { background-color: #219150; }
        .btn-danger { background-color: #e74c3c; }
        .btn-danger:hover { background-color: #c0392b; }
        .btn-secondary { background-color: #7f8c8d; }
        .btn-secondary:hover { background-color: #6c757d; }
        input, select { padding: 8px 12px; border: 1px solid #ced4da; border-radius: 5px; margin-top: 5px; margin-bottom: 15px; width: 100%; }
        .card { background: #fdfdfd; border: 1px solid #e2e8f0; border-radius: 8px; padding: 20px; margin-bottom: 25px; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>HUTTI FURTS</h1>
            <h3>Lázaro e Vladimir Frutamania</h3>
        </header>

        <nav>
            <a href="{{ url_for('loja') }}">🛒 Loja</a>
            <a href="{{ url_for('ver_carrinho') }}">🛍️ Carrinho</a>
            {% if session.get('admin_logado') %}
                <a href="{{ url_for('admin') }}">⚙️ Painel Admin</a>
                <a href="{{ url_for('logout') }}" style="color: #e74c3c;">Sair (Felipe)</a>
            {% else %}
                <a href="{{ url_for('login') }}">🔐 Área do Admin</a>
            {% endif %}
        </nav>

        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}

        {{ CONTEUDO | safe }}
    </div>
</body>
</html>
"""

def obter_carrinho():
    if "carrinho" not in session:
        session["carrinho"] = []
    return session["carrinho"]

def renderizar(conteudo_html, **kwargs):
    html_final = HTML_LAYOUT.replace("{{ CONTEUDO | safe }}", conteudo_html)
    return render_template_string(html_final, **kwargs)

@app.route("/")
def loja():
    conteudo = """
    <h2>Nosso Catálogo</h2>
    {% for categoria, produtos in catalogo.items() %}
        <div class="card">
            <h3 style="color: #2980b9; margin-top:0;">{{ categoria }}</h3>
            <table>
                <thead>
                    <tr>
                        <th>Produto</th>
                        <th>Preço Unitário / kg</th>
                        <th style="width: 220px;">Quantidade</th>
                    </tr>
                </thead>
                <tbody>
                    {% for prod, preco in produtos.items() %}
                    <tr>
                        <td><strong>{{ prod }}</strong></td>
                        <td>R$ {{ "%.2f"|format(preco) }}</td>
                        <td>
                            <form action="{{ url_for('adicionar_carrinho') }}" method="POST" style="display: flex; gap: 8px; align-items: center;">
                                <input type="hidden" name="categoria" value="{{ categoria }}">
                                <input type="hidden" name="produto" value="{{ prod }}">
                                <input type="number" name="quantidade" step="0.1" min="0.1" value="1" style="width: 80px; margin: 0;" required>
                                <button type="submit" class="btn">Adicionar</button>
                            </form>
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    {% endfor %}
    """
    return renderizar(conteudo, catalogo=catalogo)

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

@app.route("/carrinho")
def ver_carrinho():
    carrinho = obter_carrinho()
    total = sum(item["subtotal"] for item in carrinho)
    conteudo = """
    <h2>Seu Carrinho de Compras</h2>
    {% if not carrinho %}
        <p>O seu carrinho está vazio no momento.</p>
        <a href="{{ url_for('loja') }}" class="btn">Ir às Compras</a>
    {% else %}
        <table>
            <thead>
                <tr>
                    <th>Produto</th>
                    <th>Quantidade / Peso</th>
                    <th>Preço Unitário</th>
                    <th>Subtotal</th>
                </tr>
            </thead>
            <tbody>
                {% for item in carrinho %}
                <tr>
                    <td>{{ item.produto }}</td>
                    <td>{{ item.quantidade }}</td>
                    <td>R$ {{ "%.2f"|format(item.preco_unit) }}</td>
                    <td>R$ {{ "%.2f"|format(item.subtotal) }}</td>
                </tr>
                {% endfor %}
                <tr style="font-size: 1.1em; background-color: #f8f9fa;">
                    <td colspan="3" style="text-align: right;"><strong>VALOR TOTAL DA CONTA:</strong></td>
                    <td><strong style="color: #27ae60;">R$ {{ "%.2f"|format(total) }}</strong></td>
                </tr>
            </tbody>
        </table>

        <div style="margin-top: 25px; display: flex; gap: 15px;">
            <form action="{{ url_for('limpar_carrinho') }}" method="POST">
                <button type="submit" class="btn btn-danger">Esvaziar Carrinho</button>
            </form>
            <a href="{{ url_for('loja') }}" class="btn btn-secondary">Continuar Comprando</a>
        </div>
    {% endif %}
    """
    return renderizar(conteudo, carrinho=carrinho, total=total)

@app.route("/limpar", methods=["POST"])
def limpar_carrinho():
    session["carrinho"] = []
    flash("Carrinho esvaziado com sucesso.", "info")
    return redirect(url_for("ver_carrinho"))

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

    conteudo = """
    <div class="card" style="max-width: 400px; margin: 0 auto;">
        <h2 style="text-align: center;">Acesso Administrativo</h2>
        <form method="POST">
            <label for="usuario">Usuário:</label>
            <input type="text" id="usuario" name="usuario" placeholder="Digite o usuário" required>

            <label for="senha">Senha:</label>
            <input type="password" id="senha" name="senha" placeholder="Digite a senha" required>

            <button type="submit" class="btn" style="width: 100%;">Entrar</button>
        </form>
    </div>
    """
    return renderizar(conteudo)

@app.route("/logout")
def logout():
    session.pop("admin_logado", None)
    flash("Sessão encerrada com sucesso.", "info")
    return redirect(url_for("loja"))

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

    conteudo = """
    <h2>Painel do Administrador</h2>

    <div class="card">
        <h3>1. Modificar Preço de Produto Existente</h3>
        <form method="POST">
            <input type="hidden" name="acao" value="alterar">
            
            <label>Categoria:</label>
            <select name="categoria" required>
                {% for cat in catalogo.keys() %}
                    <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select>

            <label>Nome do Produto (Exatamente como consta no catálogo):</label>
            <input type="text" name="produto" placeholder="Ex: Maçã" required>

            <label>Novo Preço (R$):</label>
            <input type="number" step="0.01" name="preco" placeholder="Ex: 7.50" required>

            <button type="submit" class="btn">Atualizar Preço</button>
        </form>
    </div>

    <div class="card">
        <h3>2. Adicionar Novo Produto ao Catálogo</h3>
        <form method="POST">
            <input type="hidden" name="acao" value="adicionar">
            
            <label>Categoria:</label>
            <select name="categoria" required>
                {% for cat in catalogo.keys() %}
                    <option value="{{ cat }}">{{ cat }}</option>
                {% endfor %}
            </select>

            <label>Nome do Novo Produto:</label>
            <input type="text" name="novo_produto" placeholder="Ex: Melancia" required>

            <label>Preço (R$):</label>
            <input type="number" step="0.01" name="novo_preco" placeholder="Ex: 12.00" required>

            <button type="submit" class="btn">Cadastrar Produto</button>
        </form>
    </div>
    """
    return renderizar(conteudo, catalogo=catalogo)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8501, debug=True)
