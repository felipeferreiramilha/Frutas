# ==========================================
# HUTTI FURTS & LAZARO E VLADIMIR FRUTAMANIA
# Sistema de Gestão e Vendas
# ==========================================

# Dicionário inicial de produtos e preços por kg ou unidade
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

def exibir_cabecalho():
    print("=" * 60)
    print("      HUTTI FURTS & LAZARO E VLADIMIR FRUTAMANIA      ")
    print("=" * 60)

def menu_admin():
    senha = input("Digite a senha do Administrador (Senha padrão: 1234): ")
    if senha != "1234":
        print("\n[Erro] Senha incorreta! Acesso negado.")
        return

    while True:
        print("\n--- PAINEL DO ADMINISTRADOR ---")
        print("1. Visualizar Produtos e Preços")
        print("2. Modificar Preço de um Produto")
        print("3. Adicionar Novo Produto")
        print("4. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("\n--- CATÁLOGO ATUAL ---")
            for categoria, itens in catalogo.items():
                print(f"\n[{categoria}]")
                for produto, preco in itens.items():
                    print(f"  - {produto}: R$ {preco:.2f}")
                    
        elif opcao == "2":
            print("\nCategorias disponíveis: Frutas, Carnes, Gelados")
            cat = input("Digite a categoria do produto: ").capitalize()
            if cat in catalogo:
                print(f"\nProdutos em {cat}:")
                for p in catalogo[cat]:
                    print(f"  - {p}")
                prod = input("Digite o nome exato do produto que deseja alterar: ")
                if prod in catalogo[cat]:
                    try:
                        novo_preco = float(input(f"Digite o novo preço para {prod} (R$): "))
                        catalogo[cat][prod] = novo_preco
                        print(f"\n[Sucesso] O preço de {prod} foi atualizado para R$ {novo_preco:.2f}!")
                    except ValueError:
                        print("\n[Erro] Digite um valor numérico válido.")
                else:
                    print("\n[Erro] Produto não encontrado.")
            else:
                print("\n[Erro] Categoria inválida.")
                
        elif opcao == "3":
            print("\nCategorias disponíveis: Frutas, Carnes, Gelados")
            cat = input("Digite a categoria onde deseja adicionar: ").capitalize()
            if cat in catalogo:
                nome_novo = input("Digite o nome do novo produto: ")
                try:
                    preco_novo = float(input("Digite o preço do produto (R$): "))
                    catalogo[cat][nome_novo] = preco_novo
                    print(f"\n[Sucesso] Produto '{nome_novo}' adicionado com sucesso em {cat}!")
                except ValueError:
                    print("\n[Erro] Digite um valor numérico válido.")
            else:
                print("\n[Erro] Categoria inválida.")
                
        elif opcao == "4":
            break
        else:
            print("\n[Erro] Opção inválida. Tente novamente.")

def menu_consumidor():
    carrinho = []
    
    while True:
        print("\n--- ÁREA DO CONSUMIDOR - FAÇA SUAS COMPRAS ---")
        print("1. Ver Catálogo de Produtos")
        print("2. Adicionar Produto ao Carrinho")
        print("3. Ver Carrinho e Calcular Total")
        print("4. Finalizar Compra")
        print("5. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("\n--- NOSSO CATÁLOGO ---")
            for categoria, itens in catalogo.items():
                print(f"\n[{categoria}]")
                for produto, preco in itens.items():
                    print(f"  - {produto}: R$ {preco:.2f}")
                    
        elif opcao == "2":
            print("\nCategorias: Frutas | Carnes | Gelados")
            cat = input("Escolha a categoria: ").capitalize()
            if cat in catalogo:
                print(f"\nItens em {cat}:")
                lista_produtos = list(catalogo[cat].keys())
                for i, prod in enumerate(lista_produtos, 1):
                    print(f"  {i}. {prod} - R$ {catalogo[cat][prod]:.2f}")
                
                try:
                    escolha_prod = int(input("Digite o número do produto desejado: ")) - 1
                    if 0 <= escolha_prod < len(lista_produtos):
                        nome_produto = lista_produtos[escolha_prod]
                        preco_produto = catalogo[cat][nome_produto]
                        
                        quantidade = float(input(f"Informe a quantidade ou peso de '{nome_produto}': "))
                        if quantidade > 0:
                            subtotal = preco_produto * quantidade
                            carrinho.append({
                                "produto": nome_produto,
                                "preco_unit": preco_produto,
                                "quantidade": quantidade,
                                "subtotal": subtotal
                            })
                            print(f"\n[Sucesso] {quantidade}x '{nome_produto}' adicionado ao carrinho!")
                        else:
                            print("\n[Erro] A quantidade deve ser maior que zero.")
                    else:
                        print("\n[Erro] Número de produto inválido.")
                except ValueError:
                    print("\n[Erro] Entrada inválida.")
            else:
                print("\n[Erro] Categoria inválida.")
                
        elif opcao == "3":
            if not carrinho:
                print("\nSeu carrinho está vazio.")
            else:
                print("\n--- SEU CARRINHO DE COMPRAS ---")
                total_geral = 0
                for item in carrinho:
                    print(f"- {item['produto']} | Qtd: {item['quantidade']} | Preço Unit.: R$ {item['preco_unit']:.2f} | Subtotal: R$ {item['subtotal']:.2f}")
                    total_geral += item['subtotal']
                print("-" * 40)
                print(f"VALOR TOTAL DA CONTA: R$ {total_geral:.2f}")
                
        elif opcao == "4":
            if not carrinho:
                print("\nSeu carrinho está vazio. Adicione itens antes de finalizar.")
            else:
                print("\n--- FECHAMENTO DE PEDIDO ---")
                total_geral = sum(item['subtotal'] for item in carrinho)
                for item in carrinho:
                    print(f"- {item['produto']} ({item['quantidade']}) ............ R$ {item['subtotal']:.2f}")
                print("=" * 40)
                print(f"TOTAL A PAGAR: R$ {total_geral:.2f}")
                print("\nObrigado por comprar no Hutti Furts e Lazaro e Vladimir Frutamania!")
                print("Volte sempre!")
                break
                
        elif opcao == "5":
            break
        else:
            print("\n[Erro] Opção inválida.")

def main():
    while True:
        exibir_cabecalho()
        print("1. Área do Consumidor (Comprar)")
        print("2. Painel do Administrador (Gerenciar Preços)")
        print("3. Sair do Sistema")
        
        escolha = input("\nQuem é você? Escolha uma opção: ")
        
        if escolha == "1":
            menu_consumidor()
        elif escolha == "2":
            menu_admin()
        elif escolha == "3":
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\n[Erro] Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    main()
