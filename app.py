import tkinter as tk
from tkinter import simpledialog


class sistema_bancario(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema Bancário")
        self.geometry("200x200")

        self.saldo = 0  # Saldo inicial

        self.label_saldo = tk.Label(self, text=f"Saldo: R${self.saldo}")
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
        # implementando a logica de deposito aqui
        deposito = simpledialog.askfloat(
            "Despósito", "Digite o valor que deseja depositar:", parent=self
        )
        if deposito is not None:
            self.saldo += deposito
            self.label_saldo.config(text=f"Saldo: R${self.saldo}")

    def sacar(self):
        saque = simpledialog.askfloat(
            "Saque", "Digite o valor que deseja sacar:", parent=self
        )
        if saque is not None:
            if saque <= self.saldo:
                self.saldo -= saque
                self.label_saldo.config(text=f"Saldo: R${self.saldo}")
            else:
                tk.messagebox.showerror("Erro", "Saldo insuficiente.")

    def extrato(self):
        # Implementar a logica do extrato aqui
        tk.messagebox.showinfo("Extrato", f"Saldo atual: R${self.saldo}")


if __name__ == "__main__":
    app = sistema_bancario()
    app.mainloop()
