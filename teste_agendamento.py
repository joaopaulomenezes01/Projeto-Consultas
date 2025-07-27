
from logging import config
import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, date, timedelta

from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector
from tkinter import messagebox

configure = config 
#para o emailprojetos01@gmail.com usar a seguinte senha: vzyw lush aydc jawv 

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("800x500")
app.title("Sistema de Consultas") #adc titulo p janela do app
frame_inicial = ctk.CTkFrame(app, fg_color="#B0E5F4")
frame_inicial.pack(fill="both", expand=True)
app.configure(fg_color= "#D1E8EF") #adc cor de fundo

def conectar_banco():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Fafa300967@',
        database='sistemadecadastros'
    )


conector = conectar_banco()
cursor = conector.cursor()
cursor.execute('USE sistemadecadastros;')


cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios
(id INT  AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR (11) NOT NULL,
    data_nascimento VARCHAR(10) NOT NULL,
    email VARCHAR(100) NOT NULL  UNIQUE,
    senha VARCHAR(100) NOT NULL) 
''') 

cursor.execute ('''
CREATE TABLE IF NOT EXISTS agendamentos
(id INT AUTO_INCREMENT PRIMARY KEY , 
    regioes VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    profissional VARCHAR(100) NOT NULL,
    horario TIME NOT NULL,
    data DATE NOT NULL,
    convenio VARCHAR(100),
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) 
REFERENCES usuarios(id))  ''') #adc o convenio na tabela
cursor.execute('SELECT * FROM usuarios')
cursor.fetchall() 
cursor.execute('SELECT * FROM agendamentos')
cursor.fetchall()
conector.commit()


def login(): 
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkLabel(app, text="Bem-vindo ao Login!", font=("Segoe Ui", 24, "bold")).pack(pady=10)
    img1 = Image.open("usuario.png")
    ctk_img1 = ctk.CTkImage(light_image=img1, size=(21, 21))
    img2 = Image.open("senha.png")
    ctk_img2 = ctk.CTkImage(light_image=img2, size=(21, 21))
    img3 = Image.open("cliqueaqui.png")
    ctk_img3 = ctk.CTkImage(light_image=img3, size=(21, 21))
    ctk.CTkLabel(master=app, text="Usuário:",font=("Segoe Ui", 14), image= ctk_img1, compound='left').pack(pady=10)

    campo_usuario = ctk.CTkEntry(app, placeholder_text="Digite seu email")
    campo_usuario.pack(pady=10)
    ctk.CTkLabel(master=app, text="Senha:",font=("Segoe Ui", 14), image=ctk_img2, compound='left').pack(pady=10)
    campo_senha = ctk.CTkEntry (app, placeholder_text="Digite sua senha", show='*')
    campo_senha.pack(pady=10)
    resultado = ctk.CTkLabel(app, text='')
    resultado.pack(pady=10)
    
    
    def verificar ():
        img19 = Image.open("alertaerro.png")
        ctk_img19 = ctk.CTkImage(light_image=img19, size=(21, 21))

        email = campo_usuario.get()
        senha = campo_senha.get()
        global id_usuario_logado
        id_usuario_logado = verificar_usuario(email, senha)
        if not email or not senha:
            resultado.configure(text=f"⚠️ Preencha todos os campos!", text_color="orange")
            return
           
        try:
           
           conector = conectar_banco()
           cursor = conector.cursor()
           cursor.execute("SELECT id FROM usuarios WHERE email=%s AND senha=%s", (email, senha))
           usuario = cursor.fetchone()
           conector.close()
           if usuario:
               resultado.configure(text="✅ Login bem-sucedido!", text_color="green")
               app.after(1000,lambda: inicio())
              
           else:
               resultado.configure(text="❌ Email ou senha incorretos.", text_color="red")
               return
        except Exception as e:
            resultado.configure(app, text=f" Usuário não encontrado,\n Por favor, realize seu cadastro.: {e}",image=ctk_img19, compound = 'left', text_color="red")

        
    ctk.CTkButton(app, text="Efetuar Login", command=verificar).pack(pady=10)

    recsenha = ctk.CTkLabel (app, text="Recuperar Senha", text_color='blue', cursor='hand2')
    recsenha.pack(pady=10)
    recsenha.bind("<Button-1>", lambda e: recuperar_senha())

    cads = ctk.CTkLabel(app, text="Não tem cadastro? Clique aqui", image= ctk_img3, compound="right", text_color="blue", cursor="hand2")
    cads.pack(pady=10)
    cads.bind("<Button-1>", lambda e: cadastrando())
def recuperar_senha():
    for widget in app.winfo_children():
        widget.destroy()

    ctk.CTkLabel(app, text="🔐 Recuperação de Senha", font=("Arial", 20)).pack(pady=20)

    entrada_email = ctk.CTkEntry(app, placeholder_text="Digite seu e-mail", width=300)
    entrada_email.pack(pady=10)

    resultado = ctk.CTkLabel(app, text="")
    resultado.pack(pady=10)

    def enviar_email():
        email_destino = entrada_email.get()

        if not email_destino:
            resultado.configure(text="⚠️ Informe o e-mail cadastrado!", text_color="yellow")
            return

        # Verifica se o e-mail existe no banco
        try:
            conector = conectar_banco()
            cursor = conector.cursor()
            cursor.execute("SELECT senha FROM usuarios WHERE email=%s", (email_destino,))
            resultado_consulta = cursor.fetchone()
            conector.close()

            if not resultado_consulta:
                resultado.configure(text="❌ E-mail não cadastrado.", text_color="red")
                return

            senha_usuario = resultado_consulta[0]

            # Configurações do e-mail do sistema
        
            email_sistema = "suporteapp2026@gmail.com"
            senha_sistema = "lbmb fpcn ctmi jhwh"  # Usei senha de app aqui, não a senha real

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(email_sistema, senha_sistema)

            corpo = f"""Olá,

Você solicitou a recuperação da sua senha. Sua senha cadastrada é: {senha_usuario}

Se você não solicitou isso, ignore este e-mail.

Atenciosamente,
Equipe de Suporte"""

            assunto = "Recuperação de Senha - Sistema de Agendamentos"
        
            mensagem = f"Subject: {assunto}\n\n{corpo}"
            server.sendmail(email_sistema, email_destino, mensagem.encode("utf-8"))
            server.quit()

          
            resultado.configure(text="✅ Instruções enviadas para seu e-mail!", text_color="green")
            app.after(3000,login)  # Voltar à tela de login após 3 segundos


        except Exception as erro:
            resultado.configure(text=f" ❌ Erro ao enviar e-mail:\n{erro}", text_color="red")

    ctk.CTkButton(app, text="Enviar", command=enviar_email).pack(pady=10)
    ctk.CTkButton(app, text="Voltar", command=login).pack(pady=5)

#frame_inicial = ctk.CTkFrame(app, fg_color="#A2EBFF")
frame_inicial.pack(fill="both", expand=True)

frame_esquerda = ctk.CTkFrame(frame_inicial, width=400, fg_color="#A2EBFF")
frame_esquerda.pack(side="left", fill="both", expand=True)

imagem = Image.open("img_esteto.png")
ctk_img = ctk.CTkImage(light_image=imagem, size=(300, 300))
label_img = ctk.CTkLabel(frame_esquerda, image=ctk_img, text="")
ctk.CTkLabel(frame_esquerda, text="  Olá! Bem vindo(a) ao \n Sistema de Agendamentos!  ",
font=("Segoe Ui", 20, "bold")).pack(pady=(20, 5))
label_img.pack(expand=True, pady=10)
ctk.CTkLabel(frame_esquerda, text="Agende suas consultas de forma prática\n e segura com poucos cliques.", 
font=("Segoe Ui", 15, "bold")).pack(pady=(5,10))

frame_direita = ctk.CTkFrame(frame_inicial,fg_color="#ffffff")
frame_direita.pack(side="left", fill="both", expand=True)
ctk.CTkLabel(frame_direita, text="Na nossa rede você encontra:", font=("Segoe Ui", 18, "bold")).pack(pady=(8,10))
ctk.CTkLabel(frame_direita, text=" Variedade de especialidades e profissionais ✅ \n\n Histórico de consultas disponíveis ✅ \n\n Confirmação da consulta por e-mail ✅\n\n Variedade de convênios aceitos ✅ \n\n Preços acessíveis ✅",
font=("Segoe Ui", 14,)).pack(pady=(5,10))
ctk.CTkLabel(frame_direita, text="Confira a clínica mais próxima e agende sua consulta!", font=("Segoe Ui", 15, "bold")).pack(pady=(15,5))

ctk.CTkLabel(frame_direita, text="Desenvolvido por: Júlia Gabrielle e João Paulo",
font=("Segoe Ui", 12)).pack(pady=(8,5))
ctk.CTkLabel(frame_direita, text="Versão 1.0", font=("Segoe Ui", 10)).pack(pady=5)
ctk.CTkLabel(frame_direita, text="© 2025 Todos os direitos reservados", font=("Segoe Ui", 12)).pack(pady=8)
ctk.CTkButton(frame_direita, text="Iniciar", command=login).pack(pady=2)

#def mostrar_login():
#    login()


def cadastrar_usuario(nome, cpf, data_nascimento, email, senha):
        conector = conectar_banco()
        cursor = conector.cursor()
        cursor.execute('''
        INSERT INTO usuarios (nome, cpf, data_nascimento, email, senha)
        VALUES (%s, %s, %s, %s, %s)
        ''', (nome, cpf, data_nascimento, email, senha))
        conector.commit()
        conector.close()
      
def verificar_usuario(email, senha):
    conector = conectar_banco()
    cursor = conector.cursor()
    cursor.execute('''
    SELECT id FROM usuarios WHERE email = %s AND senha = %s
    ''', (email, senha))
    usuario = cursor.fetchone()
    return usuario[0] if usuario else None
    
data_nascimento_var = tk.StringVar(app)

horarios = ['08:00', '08:45', '09:30', '10:15', '11:00', '13:00', '14:00', '15:00', '16:00', '17:00']

regioes = {"Região Metropolitana": ["Recife","Paulista","Olinda"],
           "Agreste": ["Garanhuns","Caruaru","Vitória de Santo Antão","Bezerros","Gravatá"],
           "Sertão": ["Petrolina","Floresta","Serra Talhada","Arcoverde","Salgueiro"]}

profissionais_rmr={"Cardiologia": ["Dr. Vinícius Gomes","Dr. Gabriel de Souza","Drª Bárbara Vitória"],
                   "Clínica Geral": ["Dr. Marcos André","Dr. Wallace Bernardo","Drª Beatriz Dias"],
                   "Endocrinologia": ["Dr. José Gonçalves","Drª Mirella Alves","Dr. Thiago Ribeiro"],
                   "Ginecologia": ["Dr. Pedro Alves","Drª Ana Maria","Drª Bruna Rodrigues"],
                   "Nutrição": ["Dr. João Paulo","Drª Maria Alice","Drª Kayllane Letícia"],
                   "Odontologia": ["Drª Letícia Dias","Dr. Matheus Souza","Dr. Rhuan Barros"],
                   "Oftalmologia": ["Dr. Felipe Cunha","Dr. Leandro Moura","Drª Laura Campos"],
                   "Ortopedia": ["Drª Marcela Andrade","Drª Carolina Oliveira","Drª Suellen Ferreira"],
                   "Pediatria": ["Drª Alexandra Barros","Drª Camila Ramos","Dr. Diego dos Reis"],
                   "Psiquiatria": ["Dr. Rodrigo Pontes","Drª Juliana Cunha"] }

profissionais_agreste={ "Cardiologia": ["Dr. Bruno Carvalho","Dr. Manoella Silva"],
                        "Clínica Geral":["Drª Brenda Maria","Dr. Breno Campos"],
                        "Endocrinologia":["Dr. João Victor","Dr. Arthur Rebouças"],
                        "Ginecologia":["Drª Luana Maria","Drª Luna Ribeiro"],
                        "Nutrição": ["Drª Victória Almeida","Dr. Alex de Teixeira"],
                        "Odontologia":["Drª Gleice Batista","Drª Jennifer Barbosa"],
                        "Oftalmologia":["Drª Victória Borges","Drª Selma Morais"],
                        "Ortopedia":["Dr. Carlos Silva","Dr. Rennan Nunes"],
                        "Pediatria":["Dr. Jorge Montes","Drª Lucinda da Rocha"],
                        "Psiquiatria":["Drª Eliana Teixeira","Dr. Davi Soares"] }

profissionais_sertao={ "Cardiologia": ["Drª Dandara Cruz", "Dr. Celso da Luz"],
                       "Clínica Geral":["Dr. Bernardo Maia","Drª Luíza Rebecca","Drª Laíza Santos" ],
                        "Endocrinologia":["Dr. Cleiton Pereira","Drª Danielle Larissa","Drª Diana Cavallazi"],
                        "Ginecologia":["Dr. Alessandro Victor","Dr. Miguel da Costa"],
                        "Nutrição":["Dr. Kléber Eduardo","Dr. Kleyton Paulo"],
                        "Odontologia":["Dr. Pablo Arruda","Drª Esther Silva","Dr. Samuel Queiroz"],
                        "Oftalmologia":["Drª Maura Fontes","Dr. Jonas do Nascimento"],
                        "Ortopedia":["Dr. Christiano Fernando","Dr. Luciano Neves","Drª Fernanda Ramos"],
                        "Pediatria":["Drª Priscilla Fontes","Dr. Ronaldo Santana"],
                        "Psiquiatria":["Dr. Enzo Vieira","Drª Valentina Eduarda"] }

convenios= ['Hapvida', 'Unimed Recife', 'Unimed Caruaru', 'Amil', 'Bradesco Saúde','SulAmérica', 'Cassi', 'GEAP', 'Saúde Caixa', 'Fusex', 'Particular']

def abrir_calendario():
    janela_cal = tk.Toplevel(app)
    janela_cal.title("Escolha a Data")
    calendario = Calendar(janela_cal, date_pattern="dd/mm/yyyy", locale='pt_BR')
    calendario.pack(pady=10)
    def selecionar_data():
        data_nascimento_var.set(calendario.get_date())
        janela_cal.destroy()
    ctk.CTkButton(janela_cal, text="Selecionar", command=selecionar_data).pack(pady=10)

def cadastrando():
    for widget in app.winfo_children(): 
        widget.destroy()
    img14 = Image.open("email.png")
    ctk_img14 = ctk.CTkImage(light_image=img14, size=(21, 21))
    img15 = Image.open("senha.png")
    ctk_img15 = ctk.CTkImage(light_image=img15, size=(21, 21))
    img16 = Image.open("usuario.png")
    ctk_img16 = ctk.CTkImage(light_image=img16, size=(21, 21))
    ctk.CTkLabel(app, text='Nome Completo:').pack(pady=2)
    nome  = ctk.CTkEntry(app, placeholder_text='Digite seu Nome Completo')
    nome.pack(pady=2)
    ctk.CTkLabel(app, text="CPF:").pack(pady=2)
    cpf = ctk.CTkEntry(app, placeholder_text="Digite seu CPF")
    cpf.pack(pady=2)
    ctk.CTkLabel(app, text="Data de Nascimento:").pack(pady=2)
    data = ctk.CTkEntry(app, textvariable=data_nascimento_var, state="readonly", placeholder_text="XX/XX/XXXX")
    data.pack(pady=3)
    ctk.CTkButton(app, text="Selecionar Data", command=abrir_calendario).pack(pady=2)
    ctk.CTkLabel(app, text='Usuário:', image= ctk_img16, compound='left').pack(pady=2)
    email_entry = ctk.CTkEntry(app, placeholder_text='Digite seu Email')
    email_entry.pack(pady=2)
    ctk.CTkLabel(app, text="Senha:", image=ctk_img15, compound='left').pack(pady=5)
    senha_entry = ctk.CTkEntry(app, placeholder_text="Digite sua senha:", show='*')
    senha_entry.pack(pady=2)

    def salvar_cadastro():
        global email_cadastrado, senha_cadastrada
        email_cadastrado = email_entry.get()
        senha_cadastrada = senha_entry.get()

        if not nome.get() or not cpf.get() or not data_nascimento_var.get() or not email_cadastrado or not senha_cadastrada:
            ctk.CTkLabel(app, text="⚠️ Preencha todos os campos!", text_color="yellow").pack(pady=10)
            return
        
        cursor.execute("SELECT email FROM usuarios WHERE email=%s", (email_cadastrado,))
        if cursor.fetchone() is not None:
            ctk.CTkLabel(app, text="❌ Usuário já cadastrado.", text_color="red").pack(pady=10)
            app.after(1000, login)
            return

        sucesso= cadastrar_usuario(nome.get(), cpf.get(), data_nascimento_var.get(), email_cadastrado, senha_cadastrada)
        if sucesso:
            ctk.CTkLabel(app,text="✅ Cadastro realizado com sucesso!", text_color="green").pack(pady=10)
            app.after(1000, login)
        #else:
        #    ctk.CTkLabel(app, text="❌ Usuário já cadastrado.", text_color="red").pack(pady=10)
        #    app.after(1000, login)

    ctk.CTkButton(app, text='Salvar Cadastro', command=salvar_cadastro).pack(pady=10)
    ctk.CTkButton(app, text='Voltar ao Login', command=login).pack(pady=10)

def inicio():
    for widget in app.winfo_children():
        widget.destroy()

    img17=Image.open("escolha2.png")
    ctk_img17 = ctk.CTkImage(light_image=img17, size=(30, 30))
    ctk.CTkLabel(app,text="O que deseja fazer?",font=("Segoe Ui", 20, "bold"),image=ctk_img17,compound='left').pack(pady=(10,10))
    ctk.CTkButton(app, text="Ver meu histórico de agendamentos",font=("Segoe Ui", 14), command=lambda: historico_agendamentos()).pack(pady=20)
    ctk.CTkButton(app,text="Iniciar agendamento de consultas",font=("Segoe Ui", 14), command=lambda:escolher_convenio()).pack(pady=20)
    ctk.CTkButton(app,text="Ver lista de convênios aceitos", font=("Segoe Ui", 14),command=lambda:mostrar_convenios()).pack(pady=20) #adc esse botao

def mostrar_convenios(): #mostra a lista dos convenios
    for widget in app.winfo_children():
        widget.destroy()
    imgconv=Image.open("convenios.png")
    ctk_imgconv=ctk.CTkImage(light_image=imgconv, size=(21, 21))
    ctk.CTkLabel(app,text="Lista de Convênios aceitos pela nossa rede:",font=("Segoe Ui", 20, "bold"), image=ctk_imgconv,compound='left').pack(pady=(10,10))
    for convenio in convenios:
        ctk.CTkLabel(app,text=f"{convenio}",font=("Segoe Ui", 14)).pack(pady=5)
    ctk.CTkButton(app, text='Voltar', command=inicio).pack(pady=5)

def escolher_convenio(): #mostra os convenios para escolha
    for widget in app.winfo_children():
        widget.destroy()
    imgconv=Image.open("convenios.png")
    ctk_imgconv=ctk.CTkImage(light_image=imgconv, size=(21, 21))
    ctk.CTkLabel(app,text="Escolha seu Convênio",font=("Segoe Ui", 18, "bold"), image=ctk_imgconv,compound='left').pack(pady=15)
    ctk.CTkLabel(app,text="❌ Não possui?",font=("Segoe Ui", 16)).pack(pady=10)
    ctk.CTkLabel(app,text="Apenas no mês de inauguração da nossa rede, a Consulta Particular para qualquer especialidade \n está custando R$75,00! Cuide da sua saúde e não perca essa oportunidade!",font=("Segoe Ui", 14,)).pack(pady=20)

    box_convenio = ctk.CTkOptionMenu(app, values=convenios)
    box_convenio.pack(pady=10)
    ctk.CTkButton(app, text="Próximo", command=lambda: salvar_convenio(box_convenio.get())).pack(pady=10)
    ctk.CTkButton(app, text='Voltar', command=inicio).pack(pady=(10,10))

def salvar_convenio(convenio_escolhido):
    global convenio
    convenio=convenio_escolhido
    escolher_regiao()

def escolher_regiao(): 
    for widget in app.winfo_children():
        widget.destroy()
    img4 = Image.open("regiao2.png")
    ctk_img4 = ctk.CTkImage(light_image=img4, size=(21, 21))
    ctk.CTkLabel(app,text="Escolha a região desejada:",font=("Segoe Ui", 18, "bold"), image=ctk_img4,compound='left').pack(pady=10)
    box_regiao=ctk.CTkOptionMenu(app,values=list(regioes.keys()))
    box_regiao.pack(pady=15)
    ctk.CTkButton(app,text="Próximo", command=lambda:escolher_cidade(box_regiao.get())).pack(pady=15)
    ctk.CTkButton(app, text="Voltar", command=lambda: inicio()).pack(pady=15)

def escolher_cidade(regiao): 
    for widget in app.winfo_children():
        widget.destroy()
    img_cidade=Image.open("cidade.png")
    ctk_img_cidade=ctk.CTkImage(light_image=img_cidade, size=(21,21))
    ctk.CTkLabel(app, text= f"Escolha a cidade em {regiao}:",font=("Segoe Ui", 18, "bold"),image=ctk_img_cidade,compound='left').pack(pady=10)
    cidades=regioes.get(regiao,[])
    box_cidade=ctk.CTkOptionMenu(app,values=cidades)
    box_cidade.pack(pady=15)
    ctk.CTkButton(app,text="Próximo", command=lambda: escolher_especialidade(regiao,box_cidade.get())).pack(pady=15)
    ctk.CTkButton(app, text="Voltar", command=lambda: escolher_regiao()).pack(pady=15)


def escolher_especialidade(regiao,cidade):
    for widget in app.winfo_children():
        widget.destroy()
    img5 = Image.open("especialidade.png")
    ctk_img5 = ctk.CTkImage(light_image=img5, size=(21, 21))
    ctk.CTkLabel(app, text="Escolha a especialidade:",font=("Segoe Ui", 18, "bold"),  image= ctk_img5, compound='left').pack(pady=10)
    if regiao=="Região Metropolitana":
        box_esp = ctk.CTkOptionMenu(app, values=list(profissionais_rmr.keys()))
        box_esp.pack(pady=15)
    elif regiao=="Agreste":
        box_esp = ctk.CTkOptionMenu(app, values=list(profissionais_agreste.keys()))
        box_esp.pack(pady=15)
    else:
       box_esp = ctk.CTkOptionMenu(app, values=list(profissionais_sertao.keys()))
       box_esp.pack(pady=15)
    ctk.CTkButton(app, text="Próximo", command=lambda: escolher_profissional(regiao,cidade, box_esp.get())).pack(pady=15)
    ctk.CTkButton(app, text="Voltar", command=lambda: escolher_cidade(regiao)).pack(pady=15)
   

def escolher_profissional(regiao,cidade,especialidade):
    for widget in app.winfo_children():
        widget.destroy()
    data_var = tk.StringVar(app)
    img6 = Image.open("profissional.png")
    ctk_img6 = ctk.CTkImage(light_image=img6, size=(21, 21))
    img7 = Image.open("horarios.png")
    ctk_img7 = ctk.CTkImage(light_image=img7, size=(21, 21))
    img8 = Image.open("calendario.png")
    ctk_img8 = ctk.CTkImage(light_image=img8, size=(21, 21))

    ctk.CTkLabel(app, text=f"Profissionais disponíveis ({especialidade}):",font=("Segoe Ui", 18, "bold"),  image=ctk_img6, compound='left').pack(pady=10)
    if regiao=="Região Metropolitana": 
        nomes = profissionais_rmr.get(especialidade, [])
        box_prof = ctk.CTkOptionMenu(app, values=nomes)
        box_prof.pack(pady=15)
    elif regiao=="Agreste": 
        nomes = profissionais_agreste.get(especialidade, [])
        box_prof = ctk.CTkOptionMenu(app, values=nomes)
        box_prof.pack(pady=15)
    else: 
        nomes = profissionais_sertao.get(especialidade, [])
        box_prof = ctk.CTkOptionMenu(app, values=nomes)
        box_prof.pack(pady=15)
    ctk.CTkLabel(app, text=f"Região: {regiao}",font=("Segoe Ui", 14)).pack(pady=15)
    ctk.CTkLabel(app, text=f"Cidade: {cidade}",font=("Segoe Ui", 14)).pack(pady=15)

    resultado_label = ctk.CTkLabel(app, text="")
    resultado_label.pack(pady=5)
    
    def abrir_calendario():
        janela = tk.Toplevel(app)
        janela.title("Selecionar Data")
        data_inicio=date.today()
        data_final=data_inicio+timedelta(days=30)
        calendario = Calendar(janela, date_pattern="dd/mm/yyyy", locale='pt_BR',mindate=data_inicio,maxdate=data_final)
        calendario.pack(pady=5)

        aviso_dias = ctk.CTkLabel(janela, text="", text_color="red")
        aviso_dias.pack(pady=5)

        def escolher():
            img9 = Image.open("alertaerro.png")
            ctk_img9 = ctk.CTkImage(light_image=img9, size=(21, 21))
            data_escolhida=calendario.get_date()
            data_str=datetime.strptime(data_escolhida,"%d/%m/%Y")
            if data_str.weekday()>=5:
                aviso_dias.configure(text=" Os atendimentos só são realizados em dias úteis. \n Por favor, escolha outra data", image=ctk_img9, compound = 'left')
            else:
                data_var.set(calendario.get_date())
                janela.destroy()
                escolher_horario(box_prof.get(), data_var.get())

        ctk.CTkButton(janela, text="Confirmar Data", command=escolher).pack(pady=10)

    ctk.CTkLabel(app, text='Data da consulta:',font=("Segoe Ui", 16), image=ctk_img8, compound='left').pack(pady=10)
    entrada_data = ctk.CTkEntry(app, textvariable=data_var, state="readonly", placeholder_text="Clique no botão para escolher a data")
    entrada_data.pack(pady=5)
    ctk.CTkButton(app, text="Selecionar Data", command=abrir_calendario).pack(pady=5)
    
    ctk.CTkLabel(app, text="Horários disponíveis:",font=("Segoe Ui", 16), image=ctk_img7, compound='left').pack(pady=5)
    box_horario = ctk.CTkOptionMenu(app, values=["Ver horários"])
    box_horario.pack(pady=5)

    def escolher_horario(profissional,data):
        data_str = datetime.strptime(data, "%d/%m/%Y")
        data_mysql=data_str.strftime("%Y-%m-%d") 
        horarios_ocupados=[]
        cursor.execute("SELECT horario FROM agendamentos WHERE profissional=%s AND data=%s",(profissional, data_mysql))
        resultado=cursor.fetchall()
        for item in resultado:
            horario=(item[0]) #aqui ele retorna do formato do mysql, em formato timedelta
            horario_segundos=int(horario.total_seconds()) #deixa em formto de segundos 
            horas=horario_segundos//3600 #converte p horas
            minutos=(horario_segundos % 3600)//60 #converte p minutos
            horarios_ocupados.append(f'{horas:02d}:{minutos:02d}') #coloca na lista no formato hh:mm
        
        horarios_disponiveis=[]
        for hora in horarios:
            if hora not in horarios_ocupados:
                horarios_disponiveis.append(hora)
        if horarios_disponiveis:
            box_horario.configure(values=horarios_disponiveis)
        else:
            box_horario.configure(values=["Sem horários disponíveis"])

    def confirmar():
        prof = box_prof.get()
        horario = box_horario.get()
        data = data_var.get()

        if not prof or not horario or not data:
            resultado_label.configure(text="⚠️ Preencha todos os campos!", text_color="orange")
        else:
            data_str = datetime.strptime(data, "%d/%m/%Y")
            data_mysql=data_str.strftime("%Y-%m-%d")
            resultado_label.configure(
                text=f"✅ Consulta marcada com {prof} ({especialidade})\n🗓️ {data} às {horario}",
                text_color="green"
            )
            app.after(1000, lambda:confirmar_agendamento(regiao,cidade,especialidade,prof,horario,data_mysql,convenio)) #passa a data pro banco ja no formsto certo

    ctk.CTkButton(app, text="Confirmar Agendamento", command=lambda: confirmar()).pack(pady=10)

    ctk.CTkButton(app, text="Voltar", command=lambda: escolher_especialidade(regiao,cidade)).pack(pady=5)


    resultado_label = ctk.CTkLabel(app, text="")
    resultado_label.pack(pady=5)


def confirmar_agendamento(regiao_escolhida,cidade_escolhida,especialidade_escolhida, profissional, horario, data,convenio):
    for widget in app.winfo_children():
        widget.destroy()
    img10 = Image.open("histórico.png")
    ctk_img10 = ctk.CTkImage(light_image=img10, size=(100, 100))
    img11 = Image.open("confirma2.png")
    ctk_img11 = ctk.CTkImage(light_image=img11, size=(100, 100))
    

    
    ctk.CTkLabel(master=app, text="Agendamento Confirmado!", image=ctk_img11, compound='left' , font=("Arial", 20, "bold")).pack(pady=10)
    cursor.execute("insert into agendamentos (regioes, cidade, especialidade, profissional, horario, data, usuario_id,convenio) values (%s,%s,%s,%s,%s,%s,%s,%s)", (regiao_escolhida, cidade_escolhida, especialidade_escolhida, profissional, horario, data, id_usuario_logado,convenio))
    conector.commit()
    corpo1 = ctk.CTkLabel(app, text=f"Consulta marcada em {regiao_escolhida}, na cidade de {cidade_escolhida}, com {profissional}\nEspecialidade: {especialidade_escolhida}\nData: {data}\nHorário: {horario}\nConvênio: {convenio}", text_color="green")
    corpo1.pack(pady=10)
    ctk.CTkButton(app, text="Sair", command=app.quit).pack(pady=10)
    ctk.CTkButton(app, text="Ver meu histórico de agendamentos", image=ctk_img10, compound='left', command=lambda: historico_agendamentos()).pack(pady=10)
#global id_usuario_logado
def historico_agendamentos():
    for widget in app.winfo_children():
        widget.destroy()
    img13 = Image.open("lupa.png")
    ctk_img13 = ctk.CTkImage(light_image=img13, size=(21, 21))
    ctk.CTkLabel(app, text="Histórico de Agendamentos", image=ctk_img13, compound='right').pack(pady=10)

    cursor.execute('SELECT nome FROM usuarios WHERE id=%s', (id_usuario_logado,))
    nomes=cursor.fetchone()
    if not nomes:
        nome_usuario_logado='Usuário não encontrado'
    else:
        nome_usuario_logado=nomes[0]    
        ctk.CTkLabel(app, text=f"Consultas de {nome_usuario_logado}:").pack(pady=5)
    
    cursor.execute('SELECT * FROM agendamentos WHERE usuario_id=%s', (id_usuario_logado,))
    agendamentos = cursor.fetchall()
    global corpo1_text
    corpo1_text=''
    if not agendamentos:
        corpo1_text = "Nenhum agendamento encontrado."
        ctk.CTkLabel(app, text=corpo1_text).pack(pady=10)
    else:
        for agendamento in agendamentos:
            corpo1_text += f"Especialidade: {agendamento[3]}\n Profissional: {agendamento[4]}\n Horário: {agendamento[5]}\n Data: {agendamento[6]}\n Convenio:{agendamento[8]}"
            convenio=agendamento[8]
            if convenio=="Particular":
                ctk.CTkLabel(app, text="Preço da consulta: R$75,00.").pack(pady=5)
            ctk.CTkLabel(app, text=corpo1_text).pack(pady=5)

    ctk.CTkButton(app, text="Voltar", command=inicio).pack(pady=10)
    ctk.CTkButton(app, text="Enviar E-mail de Confirmação", command=enviar_email).pack(pady=10)

def enviar_email():
    global email_cadastrado, senha_cadastrada, email_sistema
    if not email_cadastrado or not senha_cadastrada:
        ctk.CTkLabel(app, text="⚠️ Preencha os campos de email e senha antes de enviar o email.", text_color="orange").pack(pady=10)
        return
    #ctk.CTkButton(app, text="Enviar E-mail de Confirmação", command=enviar_email).pack(pady=10)
    host = "smtp.gmail.com" # servidor SMTP do Gmail
    port = 587  # porta para conexão TLS
    login = email_cadastrado 
    senha = senha_cadastrada

    server = smtplib.SMTP(host, port) 
    server.ehlo()
    server.starttls()
    server.ehlo() 
    server.login(login, senha)


    detalhes_agendamento = corpo1_text if "corpo1_text" in globals() and corpo1_text is not None else "Detalhes do agendamento não disponíveis."
    corpo = 'Olá,\n\nSua consulta foi agendada com sucesso!\n\nDetalhes do agendamento:\n' + detalhes_agendamento + '\n\nAgradecemos por escolher nosso serviço.\n\nAtenciosamente,\nEquipe de Agendamento'
    email_msg = MIMEMultipart()
    email_msg['From'] = email_sistema
    email_msg['To'] = login
    email_msg['Subject'] = 'Confirmação de Agendamento'
    email_msg.attach(MIMEText(corpo, 'plain'))
    server.sendmail(email_sistema, login, email_msg.as_string())
    server.quit()

    ctk.CTkLabel(app, text="✅ E-mail enviado com sucesso!", text_color="green").pack(pady=10)  
app.mainloop()

