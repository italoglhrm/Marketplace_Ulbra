import sys
import time
import os
from colorama import Fore, Style, init
from tabulate import tabulate

# Inicializa o Colorama para cores no terminal
init(autoreset=True)

# ====================== CLASSES ======================
class Usuario:
    def __init__(self, id_usuario: int, nome: str):
        self.id_usuario = id_usuario
        self.nome = nome

class Comprador(Usuario):
    def __init__(self, id_usuario: int, nome: str):
        super().__init__(id_usuario, nome)
        self.carrinho = []

    def adicionar_ao_carrinho(self, produto, quantidade):
        if produto.estoque.verificar_estoque() >= quantidade:
            self.carrinho.append((produto, quantidade))
            produto.estoque.remover_estoque(quantidade)
            print(f"{Fore.GREEN}✅ {quantidade}x {produto.nome} adicionado ao carrinho.")
        else:
            print(f"{Fore.RED}⚠ Estoque insuficiente!")

class Vendedor(Usuario):
    def __init__(self, id_usuario: int, nome: str):
        super().__init__(id_usuario, nome)
        self.produtos = []

    def adicionar_produto(self, produto):
        self.produtos.append(produto)

class Estoque:
    def __init__(self, produto_id, quantidade):
        self.produto_id = produto_id
        self.quantidade = quantidade

    def adicionar_estoque(self, quantidade):
        self.quantidade += quantidade

    def remover_estoque(self, quantidade):
        if quantidade > self.quantidade:
            return False
        self.quantidade -= quantidade
        return True

    def verificar_estoque(self):
        return self.quantidade

class Produto:
    def __init__(self, id_produto, nome, preco, vendedor_id, quantidade_inicial):
        self.id_produto = id_produto
        self.nome = nome
        self.preco = preco
        self.vendedor_id = vendedor_id
        self.estoque = Estoque(id_produto, quantidade_inicial)

# ====================== SINGLETON DO MARKETPLACE ======================
class Marketplace:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Marketplace, cls).__new__(cls)
            cls._instance.produtos = []
            cls._instance.usuarios = []
        return cls._instance  

    def cadastrar_vendedor(self, nome):
        vendedor = Vendedor(len(self.usuarios) + 1, nome)
        self.usuarios.append(vendedor)
        return vendedor

    def cadastrar_comprador(self, nome):
        comprador = Comprador(len(self.usuarios) + 1, nome)
        self.usuarios.append(comprador)
        return comprador

    def listar_produtos(self):
        if not self.produtos:
            print(f"{Fore.YELLOW}⚠ Nenhum produto disponível no momento.")
            return
        
        tabela = [[p.id_produto, p.nome, f"R${p.preco:.2f}", p.estoque.verificar_estoque()] for p in self.produtos]
        print(f"\n{Fore.CYAN}📌 Produtos Disponíveis:")
        print(tabulate(tabela, headers=["ID", "Nome", "Preço", "Estoque"], tablefmt="double_grid"))

    def adicionar_produto(self, nome, preco, vendedor, quantidade):
        produto = Produto(len(self.produtos) + 1, nome, preco, vendedor.id_usuario, quantidade)
        self.produtos.append(produto)
        vendedor.adicionar_produto(produto)

    def comprar_produto(self, comprador, produto_id, quantidade):
        produto = next((p for p in self.produtos if p.id_produto == produto_id), None)
        if produto:
            comprador.adicionar_ao_carrinho(produto, quantidade)
        else:
            print(f"{Fore.RED}⚠ Produto não encontrado!")

# ====================== INTERFACE DO TERMINAL ======================
def limpar_terminal():
    os.system("cls" if os.name == "nt" else "clear")

def loading(texto):
    print(f"{Fore.MAGENTA}{texto}", end="")
    for _ in range(3):
        time.sleep(0.5)
        print(".", end="", flush=True)
    print()

def barra():
    print(f"{Fore.BLUE}" + "="*40)

def cabecalho():
    limpar_terminal()
    print(f"{Fore.CYAN}" + "="*40)
    print(f"{Fore.YELLOW}{' 🛒  TERMINAL MARKETPLACE ':^40}")
    print(f"{Fore.CYAN}" + "="*40)

def menu_principal():
    barra()
    print(f"{Fore.GREEN}📌 MENU PRINCIPAL")
    print(f"{Fore.YELLOW}1️⃣ Adicionar produto")
    print(f"{Fore.YELLOW}2️⃣ Listar produtos")
    print(f"{Fore.YELLOW}3️⃣ Comprar produto")
    print(f"{Fore.YELLOW}4️⃣ Ver carrinho")
    print(f"{Fore.YELLOW}5️⃣ Sair")
    barra()
    return input(f"{Fore.BLUE}Escolha uma opção: {Fore.RESET}")

def exibir_carrinho(comprador):
    if not comprador.carrinho:
        print(f"{Fore.YELLOW}🛒 Carrinho vazio!")
    else:
        tabela = [[p.nome, qtd, f"R${p.preco * qtd:.2f}"] for p, qtd in comprador.carrinho]
        print(f"\n{Fore.GREEN}🛒 Seu Carrinho:")
        print(tabulate(tabela, headers=["Produto", "Qtd", "Total"], tablefmt="double_grid"))

def main():
    marketplace = Marketplace()  

    cabecalho()
    nome_vendedor = input(f"{Fore.CYAN}Digite o nome do vendedor: {Fore.RESET}")
    vendedor = marketplace.cadastrar_vendedor(nome_vendedor)

    nome_comprador = input(f"{Fore.CYAN}Digite o nome do comprador: {Fore.RESET}")
    comprador = marketplace.cadastrar_comprador(nome_comprador)

    while True:
        cabecalho()
        opcao = menu_principal()

        if opcao == "1":
            nome_produto = input(f"{Fore.CYAN}Nome do produto: {Fore.RESET}")
            preco = float(input(f"{Fore.CYAN}Preço do produto: {Fore.RESET}"))
            quantidade = int(input(f"{Fore.CYAN}Quantidade inicial: {Fore.RESET}"))
            marketplace.adicionar_produto(nome_produto, preco, vendedor, quantidade)
            loading("Cadastrando produto")
            print(f"{Fore.GREEN}✅ Produto cadastrado com sucesso!")
            time.sleep(1)

        elif opcao == "2":
            cabecalho()
            marketplace.listar_produtos()
            input(f"{Fore.YELLOW}Pressione ENTER para voltar...")

        elif opcao == "3":
            cabecalho()
            marketplace.listar_produtos()
            produto_id = int(input(f"{Fore.CYAN}Digite o ID do produto para comprar: {Fore.RESET}"))
            quantidade = int(input(f"{Fore.CYAN}Quantidade: {Fore.RESET}"))
            marketplace.comprar_produto(comprador, produto_id, quantidade)
            time.sleep(1)

        elif opcao == "4":
            cabecalho()
            exibir_carrinho(comprador)
            input(f"{Fore.YELLOW}Pressione ENTER para voltar...")

        elif opcao == "5":
            print(f"{Fore.RED}👋 Saindo do Marketplace... Até mais!")
            sys.exit()

        else:
            print(f"{Fore.RED}❌ Opção inválida! Tente novamente.")
            time.sleep(1)

if __name__ == "__main__":
    main()
