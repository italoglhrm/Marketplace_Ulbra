class Marketplace:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Marketplace, cls).__new__(cls)
            cls.__instance.__inicializar()
        return cls.__instance

    def __inicializar(self):
        self.produtos = []
        self.pedidos = []

    def adicionar_produto(self, nome, preco):
        self.produtos.append({"nome": nome, "preco": preco})
        print(f"[Marketplace] Produto adicionado: {nome} - R${preco:.2f}")

    def remover_produto(self, nome):
        self.produtos = [p for p in self.produtos if p["nome"] != nome]
        print(f"[Marketplace] Produto removido: {nome}")

    def listar_produtos(self):
        if not self.produtos:
            print("[Marketplace] Nenhum produto disponível.")
        else:
            print("\n[Marketplace] Produtos disponíveis:")
            for p in self.produtos:
                print(f"- {p['nome']} (R${p['preco']:.2f})")

    def realizar_pedido(self, nome_produto, comprador):
        produto = next((p for p in self.produtos if p["nome"] == nome_produto), None)
        if produto:
            self.pedidos.append({"produto": nome_produto, "comprador": comprador})
            print(f"[Marketplace] Pedido realizado: {nome_produto} por {comprador}")
        else:
            print(f"[Marketplace] Produto '{nome_produto}' não encontrado.")

    def cancelar_pedido(self, nome_produto, comprador):
        self.pedidos = [p for p in self.pedidos if not (p["produto"] == nome_produto and p["comprador"] == comprador)]
        print(f"[Marketplace] Pedido cancelado: {nome_produto} por {comprador}")

    def listar_pedidos(self):
        if not self.pedidos:
            print("[Marketplace] Nenhum pedido realizado ainda.")
        else:
            print("\n[Marketplace] Pedidos realizados:")
            for p in self.pedidos:
                print(f"- {p['produto']} (Comprador: {p['comprador']})")

    def consultar_pedidos_comprador(self, comprador):
        pedidos = [p for p in self.pedidos if p["comprador"] == comprador]
        if not pedidos:
            print(f"[Marketplace] {comprador} não realizou pedidos.")
        else:
            print(f"[Marketplace] Pedidos de {comprador}:")
            for p in pedidos:
                print(f" - {p['produto']}")

    def iniciar_chat(self, comprador):
        print(f"[Chat iniciado com suporte para {comprador}]")
        while True:
            msg = input(f"{comprador}: ")
            if msg.lower() == "sair":
                print("[Chat encerrado]")
                break
            print("[Suporte]: Mensagem recebida! Em que mais posso ajudar?")


# =======================
# Menu de interação
# =======================
def exibir_menu():
    print("\n===== MENU DO MARKETPLACE =====")
    print("1. Adicionar produto")
    print("2. Remover produto")
    print("3. Listar produtos")
    print("4. Realizar pedido")
    print("5. Cancelar pedido")
    print("6. Listar pedidos")
    print("7. Consultar pedidos por comprador")
    print("8. Iniciar chat com suporte")
    print("9. Sair")


def executar():
    marketplace = Marketplace()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ")

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
            comprador = input("Nome do comprador: ")
            marketplace.iniciar_chat(comprador)

        elif opcao == "9":
            print("Encerrando sistema... Até logo!")
            break

        else:
            print("Opção inválida. Tente novamente.")

executar()