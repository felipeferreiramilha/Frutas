import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

st.set_page_config(page_title="Hutti Furts & Lázaro e Vladimir Frutamania", layout="centered")

# Inicializar estados no session_state
if "catalogo" not in st.session_state:
    st.session_state.catalogo = {
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

if "carrinho" not in st.session_state:
    st.session_state.carrinho = []

if "admin_logado" not in st.session_state:
    st.session_state.admin_logado = False

if "cliente_logado" not in st.session_state:
    st.session_state.cliente_logado = True  # Já inicia logado para facilitar
    st.session_state.cliente_email = "felipeferreiramilha@gmail.com"
    st.session_state.cliente_nome = "Felipe Ferreira"

# Função para enviar e-mail de confirmação
def enviar_email_compra(destinatario, carrinho, total):
    # ATENÇÃO: Para enviar e-mails reais via Gmail, configure seu e-mail e sua "Senha de App" do Google abaixo.
    # Caso deixe com os valores de exemplo, o sistema simulará o envio com sucesso sem travar o aplicativo.
    remetente = "seu_email_aqui@gmail.com"
    senha_app = "sua_senha_de_app_aqui"
    
    # Montar o resumo dos itens
    resumo_itens = ""
    for item in carrinho:
        resumo_itens += f"- {item['produto']} | Qtd: {item['quantidade']} | Subtotal: R$ {item['subtotal']:.2f}\n"

    # Se não configurou credenciais reais, simula o envio com sucesso
    if remetente == "seu_email_aqui@gmail.com":
        return True

    try:
        msg = MIMEMultipart()
        msg['From'] = remetente
        msg['To'] = destinatario
        msg['Subject'] = "🛒 Comprovante de Compra - Hutti Furts & Lázaro e Vladimir Frutamania"
        
        corpo = f"""Olá, {st.session_state.cliente_nome}!\n\nSua compra foi realizada com sucesso!\n\nItens do Pedido:\n{resumo_itens}\nVALOR TOTAL DA CONTA: R$ {total:.2f}\n\nObrigado por comprar no Hutti Furts e Lázaro e Vladimir Frutamania! Volte sempre!"""
        msg.attach(MIMEText(corpo, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remetente, senha_app)
        server.sendmail(remetente, destinatario, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")
        return False

# Cabeçalho
st.title("🍎 HUTTI FURTS")
st.subheader("Lázaro e Vladimir Frutamania")
st.markdown("---")

# Menu de navegação lateral
menu = st.sidebar.radio("Navegação", ["Loja / Comprar", "Carrinho", "Área do Cliente / Login", "Painel do Administrador"])

# ==================== LOJA ====================
if menu == "Loja / Comprar":
    st.header("🛒 Catálogo de Produtos")
    
    for categoria, produtos in st.session_state.catalogo.items():
        st.markdown(f"### 📂 {categoria}")
        for prod, preco in produtos.items():
            cols = st.columns([3, 2, 2])
            cols[0].write(f"**{prod}**")
            cols[1].write(f"R$ {preco:.2f}")
            
            with cols[2]:
                qtd = st.number_input(
                    f"Qtd {prod}", 
                    min_value=0.1, 
                    value=1.0, 
                    step=0.1, 
                    key=f"qtd_{categoria}_{prod}", 
                    label_visibility="collapsed"
                )
                if st.button("Adicionar", key=f"btn_{categoria}_{prod}"):
                    subtotal = preco * qtd
                    encontrado = False
                    for item in st.session_state.carrinho:
                        if item["produto"] == prod:
                            item["quantidade"] += qtd
                            item["subtotal"] = item["quantidade"] * item["preco_unit"]
                            encontrado = True
                            break
                    if not encontrado:
                        st.session_state.carrinho.append({
                            "produto": prod,
                            "preco_unit": preco,
                            "quantidade": qtd,
                            "subtotal": subtotal
                        })
                    st.success(f"{qtd}x {prod} adicionado ao carrinho!")
        st.markdown("")

# ==================== CARRINHO ====================
elif menu == "Carrinho":
    st.header("🛍️ Seu Carrinho de Compras")
    
    if not st.session_state.carrinho:
        st.info("O seu carrinho está vazio no momento.")
    else:
        total_geral = 0
        for i, item in enumerate(st.session_state.carrinho):
            cols = st.columns([3, 2, 2, 2])
            cols[0].write(f"**{item['produto']}**")
            cols[1].write(f"Qtd: {item['quantidade']}")
            cols[2].write(f"R$ {item['subtotal']:.2f}")
            if cols[3].button("Remover", key=f"rem_{i}"):
                st.session_state.carrinho.pop(i)
                st.rerun()
            total_geral += item['subtotal']
        
        st.markdown("---")
        st.markdown(f"### 💰 VALOR TOTAL DA CONTA: R$ {total_geral:.2f}")
        st.write(f"📧 **E-mail de destino do comprovante:** `{st.session_state.cliente_email}`")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Esvaziar Carrinho", type="secondary"):
                st.session_state.carrinho = []
                st.rerun()
        with col2:
            if st.button("Finalizar Compra", type="primary"):
                sucesso = enviar_email_compra(st.session_state.cliente_email, st.session_state.carrinho, total_geral)
                if sucesso:
                    st.success(f"Compra finalizada com sucesso! Comprovante enviado para {st.session_state.cliente_email}.")
                    st.session_state.carrinho = []
                else:
                    st.error("Compra finalizada, mas houve um erro ao enviar o e-mail.")

# ==================== ÁREA DO CLIENTE ====================
elif menu == "Área do Cliente / Login":
    st.header("👤 Área do Cliente")
    st.markdown("Gerencie seu cadastro e e-mail para recebimento de comprovantes de compras.")
    
    with st.form("form_cliente"):
        nome_input = st.text_input("Seu Nome", value=st.session_state.cliente_nome)
        email_input = st.text_input("Seu E-mail para Comprovantes", value=st.session_state.cliente_email)
        
        salvar = st.form_submit_button("Salvar Dados do Cliente")
        if salvar:
            st.session_state.cliente_nome = nome_input
            st.session_state.cliente_email = email_input
            st.success("Dados do cliente atualizados com sucesso!")

# ==================== ADMINISTRAÇÃO ====================
elif menu == "Painel do Administrador":
    st.header("⚙️ Painel do Administrador")
    
    if not st.session_state.admin_logado:
        st.markdown("Insira suas credenciais para gerenciar os produtos e preços.")
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        
        if st.button("Entrar"):
            if usuario == "Felipe" and senha == "123456789":
                st.session_state.admin_logado = True
                st.success("Login realizado com sucesso!")
                st.rerun()
            else:
                st.error("Usuário ou senha incorretos!")
    else:
        st.success("Logado como Administrador (Felipe)")
        if st.button("Sair da Conta"):
            st.session_state.admin_logado = False
            st.rerun()
            
        st.markdown("---")
        st.subheader("✏️ Modificar Preço de um Produto")
        cat_escolhida = st.selectbox("Categoria", list(st.session_state.catalogo.keys()))
        prod_escolhido = st.selectbox("Produto", list(st.session_state.catalogo[cat_escolhida].keys()))
        novo_preco = st.number_input(
            "Novo Preço (R$)", 
            min_value=0.0, 
            value=float(st.session_state.catalogo[cat_escolhida][prod_escolhido]), 
            step=0.5
        )
        
        if st.button("Atualizar Preço"):
            st.session_state.catalogo[cat_escolhida][prod_escolhido] = novo_preco
            st.success(f"O preço de '{prod_escolhido}' foi atualizado para R$ {novo_preco:.2f}!")

        st.markdown("---")
        st.subheader("➕ Adicionar Novo Produto")
        cat_novo = st.selectbox("Categoria", list(st.session_state.catalogo.keys()), key="cat_novo")
        nome_novo = st.text_input("Nome do Novo Produto")
        preco_novo = st.number_input("Preço (R$)", min_value=0.0, value=5.00, step=0.5)
        
        if st.button("Cadastrar Produto"):
            if nome_novo:
                st.session_state.catalogo[cat_novo][nome_novo] = preco_novo
                st.success(f"Produto '{nome_novo}' cadastrado com sucesso em {cat_novo}!")
            else:
                st.error("Por favor, digite o nome do produto.")
