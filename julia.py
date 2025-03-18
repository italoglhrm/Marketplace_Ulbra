class MarketplaceManager:
    """Singleton que gerencia produtos e pedidos."""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MarketplaceManager, cls).__new__(cls)
            cls._instance.produtos = []
            cls._instance.pedidos = []
        return cls._instance

    def adicionar_produto(self, produto):
        self.produtos.append(produto)
    
    def listar_produtos(self):
        return self.produtos

    def realizar_pedido(self, pedido):
        self.pedidos.append(pedido)
    
    def listar_pedidos(self):
        return self.pedidos


class Produto:
    """Representa um produto no marketplace."""
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco
    
    def __repr__(self):
        return f"{self.nome} - R$ {self.preco:.2f}"


class Pedido:
    """Representa um pedido realizado por um cliente."""
    def __init__(self, cliente, produto):
        self.cliente = cliente
        self.produto = produto
    
    def __repr__(self):
        return f"Pedido de {self.cliente}: {self.produto}"


class Cliente:
    """Representa um cliente do marketplace."""
    def __init__(self, nome):
        self.nome = nome
    
    def __repr__(self):
        return self.nome


def menu():
    marketplace = MarketplaceManager()
    
    while True:
        print("\n--- Marketplace ---")
        print("1. Adicionar Produto")
        print("2. Listar Produtos")
        print("3. Realizar Pedido")
        print("4. Listar Pedidos")
        print("5. Sair")
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            nome = input("Nome do produto: ")
            preco = float(input("Preço do produto: "))
            marketplace.adicionar_produto(Produto(nome, preco))
            print("Produto adicionado com sucesso!")
        
        elif opcao == "2":
            produtos = marketplace.listar_produtos()
            if produtos:
                print("\nProdutos disponíveis:")
                for produto in produtos:
                    print(produto)
            else:
                print("Nenhum produto cadastrado.")
        
        elif opcao == "3":
            nome_cliente = input("Nome do cliente: ")
            cliente = Cliente(nome_cliente)
            produtos = marketplace.listar_produtos()
            if not produtos:
                print("Nenhum produto disponível para compra.")
                continue
            
            print("\nEscolha um produto pelo número:")
            for i, produto in enumerate(produtos):
                print(f"{i + 1}. {produto}")
                escolha = int(input("Digite o número do produto: ")) - 1
                if 0 <= escolha < len(produtos):
                    marketplace.realizar_pedido(Pedido(cliente, produtos[escolha]))
                    print("Pedido realizado com sucesso!")
                else:
                    print("Escolha inválida.")
        
        elif opcao == "4":
            pedidos = marketplace.listar_pedidos()
            if pedidos:
                print("\nPedidos realizados:")
                for pedido in pedidos:
                    print(pedido)
            else:
                print("Nenhum pedido realizado.")
        
        elif opcao == "5":
            print("Saindo...")
            break
        else:
            print("Opção inválida, tente novamente.")


if __name__ == "__main__":
    menu()
