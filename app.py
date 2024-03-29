import tkinter as tk
from tkinter import simpledialog, messagebox


class Usuario:
    def __init__(self, nome, cpf):
        self.nome = nome
        self.cpf = cpf


class ContaCorrente:
    def __init__(self, numero, usuario):
        self.numero = numero
        self.usuario = usuario
        self.saldo = 0

    @staticmethod
    def formatar_valor(valor):
        return f"R$ {valor:,.2f}".replace(",", "x").replace(".", ",").replace("x", ".")

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        else:
            return False


class SistemaBancario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancário")
        self.geometry("300x350")
        self.usuarios = []  # Lista de usuários e contas
        self.conta_atual = None

        self.iniciar_interface()

    def iniciar_interface(self):
        self.label_boas_vindas = tk.Label(self, text="Bem-vindo ao Sistema Bancário!")
        self.label_boas_vindas.pack(pady=10)

        self.button_login = tk.Button(self, text="Login", command=self.login)
        self.button_login.pack(pady=5)

        self.button_registrar = tk.Button(
            self, text="Registrar", command=self.registrar
        )
        self.button_registrar.pack(pady=5)

    def atualizar_interface(self):
        self.label_boas_vindas.config(
            text=f"Bem-vindo {self.conta_atual.usuario.nome}!"
        )
        saldo_formatado = ContaCorrente.formatar_valor(self.conta_atual.saldo)
        self.label_saldo = tk.Label(self, text=f"Saldo: {saldo_formatado}")
        self.label_saldo.pack(pady=10)

        self.extrato_count = 0  # contador para solicitação de extrato
        self.extrato_limit = 3  # Limite de solicitação de extrato

        self.button_depositar = tk.Button(
            self, text="Depositar", command=self.depositar
        )
        self.button_depositar.pack(pady=5)

        self.button_sacar = tk.Button(self, text="Sacar", command=self.sacar)
        self.button_sacar.pack(pady=5)

        self.button_extrato = tk.Button(self, text="Extrato", command=self.extrato)
        self.button_extrato.pack(pady=5)

    def registrar(self):
        nome = simpledialog.askstring("Registro", "Digite seu nome:", parent=self)
        cpf = simpledialog.askstring("Registro", "Digite seu CPF:", parent=self)
        if nome and cpf:  # Verifica se nome e cpf foram fornecidos
            usuario = Usuario(nome, cpf)
            self.usuarios.append(usuario)
            conta = ContaCorrente(numero=len(self.usuarios), usuario=usuario)
            messagebox.showinfo(
                "Registro",
                f"Usuario {nome} registrado com sucesso.\nNúmero da conta: {conta.numero}",
                parent=self,
            )

    def login(self):
        nome = simpledialog.askstring("Login", "Digite seu nome:", parent=self)
        usuario = next((u for u in self.usuarios if u.nome == nome), None)
        if usuario:
            self.conta_atual = ContaCorrente(
                numero=self.usuarios.index(usuario) + 1, usuario=usuario
            )
            self.atualizar_interface()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.", parent=self)

    def depositar(self):
        valor = simpledialog.askfloat(
            "Depósito", "Digite o valor que deseja depositar:", parent=self
        )
        if valor:
            self.conta_atual.depositar(valor)
            saldo_formatado = ContaCorrente.formatar_valor(self.conta_atual.saldo)
            self.label_saldo.config(text=f"Saldo: {saldo_formatado}")

    def sacar(self):
        valor = simpledialog.askfloat(
            "Saque", "Digite o valor que deseja sacar:", parent=self
        )
        if valor and self.conta_atual.sacar(valor):
            saldo_formatado = ContaCorrente.formatar_valor(self.conta_atual.saldo)
            self.label_saldo.config(text=f"Saldo: {saldo_formatado}")
        else:
            messagebox.showerror("Erro", "Saldo insuficiente.", parent=self)

    def extrato(self):
        saldo_formatado = ContaCorrente.formatar_valor(self.conta_atual.saldo)
        messagebox.showinfo("Extrato", f"Saldo atual: {saldo_formatado}", parent=self)


if __name__ == "__main__":
    app = SistemaBancario()
    app.mainloop()
