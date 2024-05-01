from abc import ABC, abstractmethod
from datetime import datetime
import tkinter as tk
from tkinter import simpledialog, messagebox


# Interfaces e classes relacionadas a transações
class Transacao(ABC):
    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        conta.depositar(self.valor)
        conta._historico.adicionar_transacao(self)

    def __str__(self):
        return f"Depósito de {Conta.formatar_valor(self.valor)} em {self.data.strftime('%Y-%m-%d %H:%M:%S')}."


class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor
        self.data = datetime.now()

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta._historico.adicionar_transacao(self)
        else:
            raise ValueError("Saldo insuficiente.")

    def __str__(self):
        return f"Saque de {Conta.formatar_valor(self.valor)} em {self.data.strftime('%Y-%m-%d %H:%M:%S')}."


# Classes relacionadas aos clientes e históricos
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# Classes relacionadas às contas
class Conta:
    def __init__(self, numero, agencia, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = Historico()

    def get_historico(self):
        return self._historico

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, valor):
        if valor >= 0:
            self._saldo = valor
        else:
            raise ValueError("O saldo não pode ser negativo.")

    def depositar(self, valor):
        self._saldo += valor

    def sacar(self, valor):
        if valor <= self._saldo:
            self._saldo -= valor
            return True
        else:
            return False

    @staticmethod
    def formatar_valor(valor):
        return f"R${valor:.2f}".replace(".", ",")


class ContaCorrente(Conta):
    def __init__(self, numero, agencia, cliente, limite, limite_saques):
        super().__init__(numero, agencia, cliente)
        self.limite = limite
        self.limite_saques = limite_saques


class SistemaBancario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancário")
        self.geometry("300x350")  # Define o tamanho da janela
        self.clientes = []
        self.conta_atual = None

        self.iniciar_interface()

    def iniciar_interface(self):
        # Botão de login
        self.botao_login = tk.Button(self, text="Login", command=self.login)
        self.botao_login.pack(pady=10)

        # Botão de registro
        self.botao_registro = tk.Button(self, text="Registrar", command=self.registrar)
        self.botao_registro.pack(pady=10)

        # Botão para depósito
        self.botao_deposito = tk.Button(
            self, text="Depositar", command=self.realizar_deposito
        )
        self.botao_deposito.pack(pady=10)

        # Botão para saque
        self.botao_saque = tk.Button(self, text="Sacar", command=self.realizar_saque)
        self.botao_saque.pack(pady=10)

        # Botão para exibir extrato
        self.botao_extrato = tk.Button(
            self, text="Extrato", command=self.mostrar_extrato
        )
        self.botao_extrato.pack(pady=10)

        # Mensagem de boas-vindas ou status
        self.label_status = tk.Label(self, text="Bem-vindo ao Sistema Bancário!")
        self.label_status.pack(pady=20)

    def atualizar_interface(self):
        if self.conta_atual:
            self.label_status.config(
                text=f"Bem-vindo, {self.conta_atual._cliente.nome}\nSaldo atual: {Conta.formatar_valor(self.conta_atual._saldo)}"
            )
        else:
            self.label_status.config(text="Login necessário")

    # Definições para os métodos registrar, login, realizar_deposito, realizar_saque, mostrar_extrato conforme sua implementação anterior...

    def registrar(self):
        # Lógica de registro de novo cliente e conta
        nome = simpledialog.askstring(
            "Registro", "Digite seu nome completo:", parent=self
        )
        cpf = simpledialog.askstring("Registro", "Digite seu CPF:", parent=self)
        endereco = simpledialog.askstring(
            "Registro", "Digite seu endereço:", parent=self
        )
        data_nascimento = simpledialog.askstring(
            "Registro", "Digite sua data de nascimento (DD/MM/AAAA):", parent=self
        )
        senha = simpledialog.askstring(
            "Registro", "Crie uma senha:", parent=self, show="*"
        )

        if nome and cpf and endereco and data_nascimento and senha:
            novo_cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
            nova_conta = ContaCorrente(
                len(self.clientes) + 1, "001", novo_cliente, 1000.0, 10
            )
            novo_cliente.adicionar_conta(nova_conta)
            self.clientes.append(novo_cliente)
            messagebox.showinfo(
                "Registro concluído",
                f"{nome}, sua conta foi criada com sucesso.\nNúmero da conta: {nova_conta._numero}",
                parent=self,
            )

    def login(self):
        # Lógica de login de cliente existente
        cpf = simpledialog.askstring("Login", "Digite seu CPF:", parent=self)
        senha = simpledialog.askstring(
            "Login", "Digite sua senha:", parent=self, show="*"
        )

        cliente_encontrado = next((c for c in self.clientes if c.cpf == cpf), None)
        if cliente_encontrado and senha:
            self.conta_atual = cliente_encontrado.contas[
                0
            ]  # Asumindo que o cliente possui apenas uma conta
            self.atualizar_interface()
        else:
            messagebox.showerror(
                "Erro de login", "CPF ou senha incorretos.", parent=self
            )

    def realizar_deposito(self):
        # Lógica para realizar um depósito
        valor = simpledialog.askfloat(
            "Depósito", "Digite o valor do depósito:", parent=self
        )
        if valor and valor > 0:
            transacao = Deposito(valor)
            transacao.registrar(self.conta_atual)
            messagebox.showinfo(
                "Depósito realizado",
                f"Depósito de {Conta.formatar_valor(valor)} efetuado.",
                parent=self,
            )
            self.atualizar_interface()

    def realizar_saque(self):
        # Lógica para realizar um saque
        valor = simpledialog.askfloat("Saque", "Digite o valor do saque:", parent=self)
        if valor and valor > 0:
            try:
                transacao = Saque(valor)
                transacao.registrar(self.conta_atual)
                messagebox.showinfo(
                    "Saque realizado",
                    f"Saque de {Conta.formatar_valor(valor)} efetuado.",
                    parent=self,
                )
                self.atualizar_interface()
            except ValueError as e:
                messagebox.showerror("Erro no saque", str(e), parent=self)

    def mostrar_extrato(self):
        # Lógica para mostrar o extrato da conta
        historico_transacoes = "\n".join(
            str(transacao) for transacao in self.conta_atual._historico.transacoes
        )
        messagebox.showinfo(
            "Extrato", f"Extrato da conta:\n{historico_transacoes}", parent=self
        )


if __name__ == "__main__":
    app = SistemaBancario()
    app.mainloop()
