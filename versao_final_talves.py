# Classe Produto que representa um produto no marketplace
class Produto:
    def __init__(self, nome, preco):
        # Inicializa o nome e preço do produto
        self.nome = nome
        self.preco = preco
    
    def __str__(self):
        # Retorna uma representação do produto em formato de string
        return f"{self.nome} - R${self.preco:.2f}"

# Classe Pedido que representa um pedido feito por um comprador
class Pedido:
    def __init__(self, produto, comprador):
        # Inicializa o pedido com o produto e o comprador
        self.produto = produto
        self.comprador = comprador
    
    def __str__(self):
        # Retorna uma representação do pedido em formato de string
        return f"{self.produto.nome} (Comprador: {self.comprador})"

# Classe Marketplace com o padrão de projeto Singleton
class Marketplace:
    __instance = None  # A variável que vai armazenar a única instância da classe
    
    def __new__(cls):
        # Verifica se já existe uma instância da classe
        if cls.__instance is None:
            # Caso não exista, cria uma nova instância e inicializa os atributos
            cls.__instance = super(Marketplace, cls).__new__(cls)
            cls.__instance.__inicializar()
        return cls.__instance  # Retorna a instância única
    
    def __inicializar(self):
        # Inicializa listas de produtos e pedidos
        self.produtos = []
        self.pedidos = []
    
    def adicionar_produto(self, nome, preco):
        # Cria um novo objeto Produto e adiciona à lista de produtos
        produto = Produto(nome, preco)
        self.produtos.append(produto)
        print(f"[Marketplace] Produto adicionado: {produto}")

    def remover_produto(self, nome):
        # Remove o produto com o nome especificado da lista de produtos
        self.produtos = [p for p in self.produtos if p.nome != nome]
        print(f"[Marketplace] Produto removido: {nome}")

    def listar_produtos(self):
        # Exibe todos os produtos disponíveis no marketplace
        if not self.produtos:
            print("[Marketplace] Nenhum produto disponível.")
        else:
            print("\n[Marketplace] Produtos disponíveis:")
            for p in self.produtos:
                print(f"- {p}")

    def realizar_pedido(self, nome_produto, comprador):
        # Realiza um pedido se o produto estiver disponível
        produto = next((p for p in self.produtos if p.nome == nome_produto), None)
        if produto:
            pedido = Pedido(produto, comprador)  # Cria o pedido
            self.pedidos.append(pedido)  # Adiciona o pedido à lista de pedidos
            print(f"[Marketplace] Pedido realizado: {pedido}")
        else:
            print(f"[Marketplace] Produto '{nome_produto}' não encontrado.")

    def cancelar_pedido(self, nome_produto, comprador):
        # Cancela um pedido baseado no nome do produto e o comprador
        self.pedidos = [p for p in self.pedidos if not (p.produto.nome == nome_produto and p.comprador == comprador)]
        print(f"[Marketplace] Pedido cancelado: {nome_produto} por {comprador}")

    def listar_pedidos(self):
        # Exibe todos os pedidos realizados no marketplace
        if not self.pedidos:
            print("[Marketplace] Nenhum pedido realizado ainda.")
        else:
            print("\n[Marketplace] Pedidos realizados:")
            for p in self.pedidos:
                print(f"- {p}")

    def consultar_pedidos_comprador(self, comprador):
        # Exibe os pedidos feitos por um comprador específico
        pedidos = [p for p in self.pedidos if p.comprador == comprador]
        if not pedidos:
            print(f"[Marketplace] {comprador} não realizou pedidos.")
        else:
            print(f"[Marketplace] Pedidos de {comprador}:")
            for p in pedidos:
                print(f" - {p.produto.nome}")

# Função que exibe o menu de opções do marketplace
def exibir_menu():
    print("\n===== MENU DO MARKETPLACE =====")
    print("1. Adicionar produto")
    print("2. Remover produto")
    print("3. Listar produtos")
    print("4. Realizar pedido")
    print("5. Cancelar pedido")
    print("6. Listar pedidos")
    print("7. Consultar pedidos por comprador")
    print("8. Sair")

# Função principal que executa o sistema do marketplace
def executar():
    # Instancia o marketplace (Singleton)
    marketplace = Marketplace()

    while True:
        exibir_menu()  # Exibe o menu
        opcao = input("Escolha uma opção: ")  # Recebe a opção do usuário

        # Ações baseadas na escolha do usuário
        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: R$"))
            marketplace.adicionar_produto(nome, preco)

        elif opcao == "2":
            nome = input("Nome do produto a remover: ")
            marketplace.remover_produto(nome)

        elif opcao == "3":
            marketplace.listar_produtos()

        elif opcao == "4":
            comprador = input("Nome do comprador: ")
            produto = input("Produto desejado: ")
            marketplace.realizar_pedido(produto, comprador)

        elif opcao == "5":
            comprador = input("Nome do comprador: ")
            produto = input("Produto do pedido a cancelar: ")
            marketplace.cancelar_pedido(produto, comprador)

        elif opcao == "6":
            marketplace.listar_pedidos()

        elif opcao == "7":
            comprador = input("Nome do comprador: ")
            marketplace.consultar_pedidos_comprador(comprador)

        elif opcao == "8":
            print("Encerrando sistema... Até logo!")
            break  # Encerra o sistema

        else:
            print("Opção inválida. Tente novamente.")  # Mensagem de erro para opção inválida

# Inicia o sistema
executar()
