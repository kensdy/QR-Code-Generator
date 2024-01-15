import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import qrcode
import webbrowser

class GeradorQRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerador de QR Code")

        style = ttk.Style()
        style.configure('TLabel', font=('Helvetica', 12))
        style.configure('TButton', font=('Helvetica', 12))

        # Adiciona um notebook para as abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)

        # Página de Início
        self.pagina_inicio = tk.Frame(self.notebook)
        self.notebook.add(self.pagina_inicio, text="Inicio")

        # Rótulo para instruir o usuário
        instrucao_label = tk.Label(self.pagina_inicio, text="Insira o conteúdo do QR code", font=('Helvetica', 14))
        instrucao_label.pack(fill=tk.X, pady=5)

        # Frame para o campo de entrada do link
        link_frame = tk.Frame(self.pagina_inicio)
        link_frame.pack(fill=tk.X, pady=5)

        # Variável para armazenar o link digitado pelo usuário
        self.link_var = tk.StringVar()

        # Campo de entrada para o link
        self.link_entry = tk.Entry(link_frame, textvariable=self.link_var, width=30)
        self.link_entry.pack(fill=tk.X, ipadx=10, ipady=5, pady=5)

        # Botão para gerar QR code
        gerar_qr_button = tk.Button(self.pagina_inicio, text="Gerar QR Code", command=self.criar_qr_code, bg='#4CAF50', fg='white')
        gerar_qr_button.pack(fill=tk.X, ipadx=10, ipady=5, pady=5)

        # Botão para escolher o local e nome do arquivo
        salvar_button = tk.Button(self.pagina_inicio, text="Salvar Como", command=self.salvar_como, bg='#008CBA', fg='white')
        salvar_button.pack(fill=tk.X, ipadx=10, ipady=5, pady=5)

        # Página de Guia
        self.pagina_guia = tk.Frame(self.notebook)
        self.notebook.add(self.pagina_guia, text="Guia")

        # Conteúdo formatado usando widget de texto e scrollbar
        guia_texto = """
        QR Code Guia

        QR Code é um tipo de código de barras moderno que armazena informações, notável por sua capacidade de conter mais dados. Escaneados por câmeras de smartphones, os QR codes facilitam o acesso a links, informações de contato, eventos, redes Wi-Fi, entre outros. Este guia exemplifica como e para que os QR codes podem ser gerados, destacando sua versatilidade em diferentes contextos, desde compartilhar dados de contato até simplificar a conexão a redes Wi-Fi.

        - Link/URL: `https://www.example.com`
        - Texto Simples: `Texto simples para o QR code.`
        - Wi-Fi Credentials: `WIFI:T:WPA;S:MinhaRedeWiFi;P:MinhaSenha123;;`
        - Geolocalização (coordenadas GPS): `geo:37.7749,-122.4194`
        - Mensagem de Texto (SMS): `SMSTO:+123456789:Texto da mensagem`
        - E-mails: `mailto:exemplo@email.com`
        - Números de Telefone: `tel:+123456789`
        - Bitcoin Address: `bitcoin:1DvF8f1hNvECX3HJ5ovC7eAeDXYFZPz8qp`
        - Anotações de Texto: `NOTE:Texto da anotação`
        - Conectar a uma Rede Bluetooth: `bluetooth:Endereço_MAC_do_Dispositivo`
        """

        guia_texto_widget = tk.Text(self.pagina_guia, wrap=tk.WORD, width=80, height=25)
        guia_texto_widget.insert(tk.END, guia_texto)
        guia_texto_widget.config(state=tk.DISABLED)

        scrollbar = tk.Scrollbar(self.pagina_guia, command=guia_texto_widget.yview)
        guia_texto_widget.config(yscrollcommand=scrollbar.set)

        guia_texto_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Página de Informações
        self.pagina_informacoes = tk.Frame(self.notebook)
        self.notebook.add(self.pagina_informacoes, text="Informações")

        # Adiciona uma imagem, nome e link
        imagem_url = "img.png"  # Substitua pelo caminho real da sua imagem
        self.adicionar_informacao(imagem_url, "Programa Criado por Kensdy", "Confira o Repositorio do projeto aqui https://github.com/kensdy/QR-Code-Generator")

    def adicionar_informacao(self, imagem_url, nome, texto):
        imagem = Image.open(imagem_url)
        imagem.thumbnail((100, 100))
        imagem_tk = ImageTk.PhotoImage(imagem)

        label_imagem = tk.Label(self.pagina_informacoes, image=imagem_tk)
        label_imagem.image = imagem_tk
        label_imagem.pack(pady=10)

        label_nome = tk.Label(self.pagina_informacoes, text=nome, font=("Helvetica", 16, "bold"))
        label_nome.pack(pady=5)

        # Label de texto com link clicável
        label_texto = tk.Label(self.pagina_informacoes, text=texto, wraplength=400, justify="left", foreground="blue", cursor="hand2", font=('Helvetica', 10))
        label_texto.pack(pady=10)
        label_texto.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/kensdy/QR-Code-Generator"))

    def criar_qr_code(self):
        link = self.link_var.get()

        if not link:
            messagebox.showwarning("Aviso", "Por favor, insira um conteúdo para o QR code.")
            return

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        self.qr_image = img

        messagebox.showinfo("Sucesso", "QR code criado com sucesso. Clique em 'Salvar Como' para escolher o local do arquivo.")

    def salvar_como(self):
        if hasattr(self, 'qr_image'):
            nome_arquivo = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("Arquivos PNG", "*.png")], title="Salvar Como")

            if nome_arquivo:
                self.qr_image.save(nome_arquivo)
                messagebox.showinfo("Sucesso", f"QR code salvo como {nome_arquivo}")
        else:
            messagebox.showwarning("Aviso", "Por favor, primeiro gere o QR code.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GeradorQRCodeApp(root)
    root.mainloop()
