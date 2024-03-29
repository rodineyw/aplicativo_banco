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

    def depositar(self, valor):
        self.saldo += valor

    def sacar(self, valor):
        if valor <= self.saldo:
            self.saldo -= valor
            return True
        else:
            return False

    def transferir(self, conta_destino, valor):
        if self.sacar(valor):
            conta_destino.depositar(valor)
            return True
        else:
            return False


class SistemaBancario(tk.Tk):
    def __init__(self, usuario):
        super().__init__()
        self.conta = ContaCorrente(numero=1234, usuario=usuario)
        self.title("Sistema Bancário")
        self.geometry("200x200")

        self.extrato_count = 0  # contador para solicitação de extrato
        self.extrato_limit = 3  # Limite de solicitação de extrato

        self.label_saldo = tk.Label(self, text=f"Saldo: R${self.conta.saldo}")
        self.label_saldo.pack(pady=10)

        self.button_depositar = tk.Button(
            self, text="Depositar", command=self.depositar
        )
        self.button_depositar.pack(pady=5)

        self.button_sacar = tk.Button(self, text="Sacar", command=self.sacar)
        self.button_sacar.pack(pady=5)

        self.button_extrato = tk.Button(self, text="Extrato", command=self.extrato)
        self.button_extrato.pack(pady=5)

    def depositar(self):
        deposito = simpledialog.askfloat(
            "Depósito", "Digite o valor que deseja depositar:", parent=self
        )
        if deposito is not None:
            self.conta.depositar(deposito)
            self.atualizar_saldo()

    def sacar(self):
        saque = simpledialog.askfloat(
            "Saque", "Digite o valor que deseja sacar:", parent=self
        )
        if saque is not None and self.conta.sacar(saque):
            self.atualizar_saldo()
        else:
            tk.messagebox.showerror("Erro", "Saldo insuficiente.", parent=self)

    def extrato(self):
        if self.extrato_count < self.extrato_limit:
            self.extrato_count += 1
            messagebox.showinfo(
                "Extrato",
                f"Solicitação de extrato {self.extrato_count}.\nSaldo atual: R${self.conta.saldo}",
                parent=self,
            )
        else:
            messagebox.showwarning(
                "Limite atingido!",
                f"Você já atingiu o limite de {self.extrato_limit} solicitações de extrato.",
                parent=self,
            )

    def atualizar_saldo(self):
        self.label_saldo.config(text=f"Saldo: R${self.conta.saldo}")


if __name__ == "__main__":
    usuario_info = Usuario(nome="Rodiney Wanderson", cpf="123.456.789-00")
    app = SistemaBancario(usuario=usuario_info)
    app.mainloop()
