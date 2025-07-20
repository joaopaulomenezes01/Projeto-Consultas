#alterações p teste:

#subi a def do login e rec senha pro início já q precisa chamar já na 1 tela
#login ao lado direito da tela de apresenação do app
#separei profissionais por regiao
#condicionais pra mostrar os profissionais disponíveis naquela regiao
#escolhe primeiro a data, pra depois ver os horarios disponíveis daquela data, pra o profissional escolhido
#condicionais p verificar se o horario daquele profissional ainda ta disponivel

import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime, date, timedelta

from PIL import Image, ImageTk
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mysql.connector

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.geometry("800x500")
frame_inicial = ctk.CTkFrame(app, fg_color="#d1d1d1")
conector = mysql.connector.connect(
    host='localhost', 
    user='root', 
    password='Fafa300967@', )

cursor = conector.cursor()
cursor.execute('''CREATE DATABASE IF NOT EXISTS sistemadecadastros;''')
conector.database = 'sistemadecadastros'
cursor.execute('USE sistemadecadastros;')


cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios
(id INT  AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR (11) NOT NULL,
    data_nascimento VARCHAR(8) NOT NULL,
    email VARCHAR(100) NOT NULL  UNIQUE,
    senha VARCHAR(100) NOT NULL) 
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS agendamentos
(id INT AUTO_INCREMENT PRIMARY KEY , 
    regioes VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    profissional VARCHAR(100) NOT NULL,
    horario TIME NOT NULL,
    data DATE NOT NULL,
    usuario_id INT NOT NULL,
    FOREIGN KEY (usuario_id) 
REFERENCES usuarios(id))
                ON DELETE CASCADE
''')
cursor.execute('SELECT * FROM usuarios')
cursor.execute('SELECT * FROM agendamentos')
conector.commit()
conector.close()
def login(): #subi o login aqui
    for widget in frame_direita.winfo_children():
        widget.destroy()

    img1 = Image.open("usuario.png")
    ctk_img1 = ctk.CTkImage(light_image=img1, size=(21, 21))
    img2 = Image.open("senha.png")
    ctk_img2 = ctk.CTkImage(light_image=img2, size=(21, 21))
    img3 = Image.open("cliqueaqui.png")
    ctk_img3 = ctk.CTkImage(light_image=img3, size=(21, 21))
    ctk.CTkLabel(master=frame_direita, text="Usuário:", image= ctk_img1, compound='left').pack(pady=10)

    campo_usuario = ctk.CTkEntry(frame_direita, placeholder_text="Digite seu email")
    campo_usuario.pack(pady=10)
    ctk.CTkLabel(master=frame_direita, text="Senha:", image=ctk_img2, compound='left').pack(pady=10)
    campo_senha = ctk.CTkEntry (frame_direita, placeholder_text="Digite sua senha", show='*')
    campo_senha.pack(pady=10)
    resultado = ctk.CTkLabel(frame_direita, text='')
    resultado.pack(pady=10)
    def verificar():
        email=campo_usuario.get()
        senha=campo_senha.get()
        if not campo_usuario.get() or not campo_senha.get():
          resultado.configure(text="⚠️ Preencha todos os campos!", text_color="yellow")
          return
        global id_usuario_logado
        id_usuario_logado=verificar_usuario(email, senha)
        if id_usuario_logado:
          resultado.configure(text="✅ Login bem-sucedido!", text_color="green")
          frame_direita.after(1000,lambda: inicio()) 
        else:
         resultado.configure(text="❌ Email ou senha incorretos.", text_color="red")
    ctk.CTkButton(frame_direita, text="Efetuar Login", command=verificar).pack(pady=10)
    
    recsenha = ctk.CTkLabel (frame_direita, text="Recuperar Senha", text_color='blue', cursor='hand2') 
    recsenha.pack(pady=10)
    recsenha.bind("<Button-1>", lambda e: recuperar_senha())

    cads = ctk.CTkLabel(frame_direita, text="Não tem cadastro? Clique aqui", image= ctk_img3, compound="right", text_color="blue", cursor="hand2")
    cads.pack(pady=10)
    cads.bind("<Button-1>", lambda e: cadastrando())
    
    def recuperar_senha():
        for widget in frame_direita.winfo_children():
            widget.destroy()
        
        host = "smtp.gmail.com" # servidor SMTP do Gmail
        port = 587  # porta para conexão TLS
        login = email_cadastrado 
        senha = senha_cadastrada

        server = smtplib.SMTP(host, port) 
        server.starttls()
        server.ehlo() 
        server.login(login, senha)

        corpo = f"Olá,\n\nVocê solicitou a recuperação de senha. Sua senha é: {senha_cadastrada}\n\nSe você não solicitou essa recuperação, por favor, ignore este email.\n\nAtenciosamente,\nEquipe de Suporte."
        email_msg = MIMEMultipart()
        email_msg['From'] = login
        email_msg['To'] = email_cadastrado
        email_msg['Subject'] = 'Confirmação de Agendamento'
        email_msg.attach(MIMEText(corpo, 'plain'))
        server.sendmail(login, email_cadastrado, email_msg.as_string())
        server.quit()
        resultado.configure(text="✅ Instruções de recuperação enviadas para o seu email.", text_color="green")    

def mostrar_login(): #agora ele consegue mostrar dividido a tela
    login()

frame_inicial.pack(fill="both", expand=True)

frame_esquerda = ctk.CTkFrame(frame_inicial, width=400, fg_color="cyan")
frame_esquerda.pack(side="left", fill="both")

imagem = Image.open("testa.jpeg")
ctk_img = ctk.CTkImage(light_image=imagem, size=(300, 300))
label_img = ctk.CTkLabel(frame_esquerda, image=ctk_img, text="")
ctk.CTkLabel(frame_esquerda, text=" Sistema de Agendamento de Consultas ",
font=("Comic Sans MS", 20, "bold")).pack(pady=(50, 10))
label_img.pack(expand=True)
ctk.CTkLabel(frame_esquerda, text="Desenvolvido por: Júlia Gabrielle e João Paulo",
font=("Comic Sans MS", 14)).pack(pady=5)
ctk.CTkLabel(frame_esquerda, text="Versão 1.0", font=("Comic Sans MS", 14)).pack(pady=5)
ctk.CTkLabel(frame_esquerda, text="© 2025 Todos os direitos reservados", font=("Comic Sans MS", 12)).pack(pady=10)

frame_direita = ctk.CTkFrame(frame_inicial,fg_color="#d1d1d1")
frame_direita.pack(side="left", fill="both", expand=True)



def cadastrar_usuario(nome, cpf, data_nascimento, email, senha):
    try:
        cursor.execute('''
        INSERT INTO usuarios (nome, cpf, data_nascimento, email, senha)
        VALUES (%s, %s, %s, %s, %s)
        ''', (nome, cpf, data_nascimento, email, senha))
        conector.commit()
        return True
    except mysql.connector.IntegrityError:
        return False
    
def verificar_usuario(email, senha):
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
#profissionais por regiao
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
    #ctk.CTkLabel(master=app, text='E-mail:', image=ctk_img14,compound='left').pack(pady=5)##
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
        sucesso= cadastrar_usuario(nome.get(), cpf.get(), data_nascimento_var.get(), email_cadastrado, senha_cadastrada)
        if sucesso:
            ctk.CTkLabel(app,text="✅ Cadastro realizado com sucesso!", text_color="green").pack(pady=10)
            app.after(1000, login)
        else:
            ctk.CTkLabel(app, text="❌ Usuário já cadastrado.", text_color="red").pack(pady=10)
            app.after(1000, login)
        
        login()

    ctk.CTkButton(app, text='Salvar Cadastro', command=salvar_cadastro).pack(pady=10)
    ctk.CTkButton(app, text='Voltar ao Login', command=login).pack(pady=10)

def inicio():
    for widget in app.winfo_children():
        widget.destroy()

    img17 = Image.open("escolha.png")
    ctk_img17 = ctk.CTkImage(light_image=img17, size=(21, 21))
    ctk.CTkLabel(app,text="Bem-vindo(a)! O que deseja fazer?").pack(pady=10)
    ctk.CTkButton(app, text="Ver meu histórico de agendamentos", command=lambda: historico_agendamentos()).pack(pady=10)
    ctk.CTkButton(app,text="Iniciar sessão de agendamento de consultas", command=lambda:escolher_regiao()).pack(pady=10)
    
def escolher_regiao(): 
    for widget in app.winfo_children():
        widget.destroy()
    img4 = Image.open("regioes.png")
    ctk_img4 = ctk.CTkImage(light_image=img4, size=(21, 21))
    ctk.CTkLabel(app,text="Escolha a região desejada:", image=ctk_img4,compound='left').pack(pady=5)
    box_regiao=ctk.CTkOptionMenu(app,values=list(regioes.keys()))
    box_regiao.pack(pady=5)
    regiao=box_regiao.get()
    ctk.CTkButton(app,text="Próximo", command=lambda:escolher_cidade(regiao)).pack(pady=10)
    ctk.CTkButton(app, text="Voltar", command=lambda: inicio()).pack(pady=5)

def escolher_cidade(regiao): 
    for widget in app.winfo_children():
        widget.destroy()
    ctk.CTkLabel(app, text= f"Escolha a cidade em {regiao}:").pack(pady=5)
    cidades=regioes.get(regiao,[])
    box_cidade=ctk.CTkOptionMenu(app,values=cidades)
    box_cidade.pack(pady=5)
    cidade=box_cidade.get()
    ctk.CTkButton(app,text="Próximo", command=lambda: escolher_especialidade(regiao,cidade)).pack(pady=10)
    ctk.CTkButton(app, text="Voltar", command=lambda: escolher_regiao()).pack(pady=5)


def escolher_especialidade(regiao,cidade):
    for widget in app.winfo_children():
        widget.destroy()
    img5 = Image.open("especialidade.png")
    ctk_img5 = ctk.CTkImage(light_image=img5, size=(21, 21))
    ctk.CTkLabel(app, text="Escolha a especialidade:", image= ctk_img5, compound='left').pack(pady=5)
    if regiao=="Região Metropolitana":
        box_esp = ctk.CTkOptionMenu(app, values=list(profissionais_rmr.keys()))
        box_esp.pack(pady=5)
    elif regiao=="Agreste":
        box_esp = ctk.CTkOptionMenu(app, values=list(profissionais_agreste.keys()))
        box_esp.pack(pady=5)
    else:
       box_esp = ctk.CTkOptionMenu(app, values=list(profissionais_sertao.keys()))
       box_esp.pack(pady=5)
    especialidade=box_esp.get() 
    ctk.CTkButton(app, text="Próximo", command=lambda: escolher_profissional(regiao,cidade, especialidade)).pack(pady=10)
    ctk.CTkButton(app, text="Voltar", command=lambda: escolher_cidade(regiao)).pack(pady=5)
   

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

    ctk.CTkLabel(app, text=f"Profissionais disponíveis ({especialidade}):", image=ctk_img6, compound='left').pack(pady=5)
    if regiao=="Região Metropolitana": #condicional por regiao
        nomes = profissionais_rmr.get(especialidade, [])
        box_prof = ctk.CTkOptionMenu(app, values=nomes)
        box_prof.pack(pady=5)
    elif regiao=="Agreste": #condicional por regiao
        nomes = profissionais_agreste.get(especialidade, [])
        box_prof = ctk.CTkOptionMenu(app, values=nomes)
        box_prof.pack(pady=5)
    else: #condicional por regiao
        nomes = profissionais_sertao.get(especialidade, [])
        box_prof = ctk.CTkOptionMenu(app, values=nomes)
        box_prof.pack(pady=5)
    ctk.CTkLabel(app, text=f"Região: {regiao}").pack(pady=5)
    ctk.CTkLabel(app, text=f"Cidade: {cidade}").pack(pady=5)

    def abrir_calendario():
        janela = tk.Toplevel(app)
        janela.title("Selecionar Data")
        data_inicio=date.today()
        data_final=data_inicio+timedelta(days=30)
        calendario = Calendar(janela, date_pattern="dd/mm/yyyy", locale='pt_BR',mindate=data_inicio,maxdate=data_final)
        calendario.pack(pady=10)

        aviso_dias = ctk.CTkLabel(janela, text="", text_color="red")
        aviso_dias.pack(pady=10)

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
                escolher_horario(box_prof.get(), data_escolhida)

        ctk.CTkButton(janela, text="Confirmar Data", command=escolher).pack(pady=10)
        resultado_label = ctk.CTkLabel(app, text="")
        resultado_label.pack(pady=5)


    ctk.CTkLabel(app, text='Data da consulta:', image=ctk_img8, compound='left').pack(pady=5)
    entrada_data = ctk.CTkEntry(app, textvariable=data_var, state="readonly", placeholder_text="Clique no botão para escolher a data")
    entrada_data.pack(pady=5)
    ctk.CTkButton(app, text="Selecionar Data", command=abrir_calendario).pack(pady=5)
    
    ctk.CTkLabel(app, text="Horário disponível:", image=ctk_img7, compound='left').pack(pady=5)
    box_horario = ctk.CTkOptionMenu(app, values=["Ver horários"])
    box_horario.pack(pady=5)

    def escolher_horario(profissional,data): #nova função
        horarios_ocupados=[]
        cursor.execute("SELECT horario FROM agendamentos WHERE profissional=%s AND data=%s", (profissional, data))
        resultado=cursor.fetchall()
        for item in resultado:
            horarios_ocupados.append(item[0]) 
        
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
            resultado_label.configure(
                text=f"✅ Consulta marcada com {prof} ({especialidade})\n🗓️ {data} às {horario}",
                text_color="green"
            )
            app.after(1000, lambda:confirmar_agendamento(regiao,cidade,especialidade,prof,horario,data))

    ctk.CTkButton(app, text="Confirmar Agendamento", command=lambda: confirmar()).pack(pady=10)

    ctk.CTkButton(app, text="Voltar", command=lambda: escolher_especialidade(regiao,cidade)).pack(pady=5)


    resultado_label = ctk.CTkLabel(app, text="")
    resultado_label.pack(pady=5)


def confirmar_agendamento(regiao_escolhida,cidade_escolhida,especialidade_escolhida, profissional, horario, data):
    for widget in app.winfo_children():
        widget.destroy()
    img10 = Image.open("histórico.png")
    ctk_img10 = ctk.CTkImage(light_image=img10, size=(100, 100))
    img11 = Image.open("confirma2.png")
    ctk_img11 = ctk.CTkImage(light_image=img11, size=(100, 100))
    

    
    ctk.CTkLabel(master=app, text="Agendamento Confirmado!", image=ctk_img11, compound='left' , font=("Arial", 20, "bold")).pack(pady=10)
    cursor.execute("insert into agendamentos (regioes, cidade, especialidade, profissional, horario, data, usuario_id) values (%s,%s,%s,%s,%s,%s,%s)", (regiao_escolhida, cidade_escolhida, especialidade_escolhida, profissional, horario, data, id_usuario_logado))
    conector.commit()
    corpo1 = ctk.CTkLabel(app, text=f"Consulta marcada em {regiao_escolhida}, na cidade de {cidade_escolhida}, com {profissional}\nEspecialidade: {especialidade_escolhida}\nData: {data}\nHorário: {horario}", text_color="green")
    corpo1.pack(pady=10)
    ctk.CTkButton(app, text="Sair", command=app.quit).pack(pady=10)
    ctk.CTkButton(app, text="Ver meu histórico de agendamentos", image=ctk_img10, compound='left', command=lambda: historico_agendamentos()).pack(pady=10)

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
            corpo1_text += f"Especialidade: {agendamento[3]}, Profissional: {agendamento[4]}, Horário: {agendamento[5]}, Data: {agendamento[6]}\n"
            ctk.CTkLabel(app, text=corpo1_text).pack(pady=5)

    ctk.CTkButton(app, text="Voltar", command=inicio).pack(pady=10)

def enviar_email():
    global email_cadastrado, senha_cadastrada
    if not email_cadastrado or not senha_cadastrada:
        ctk.CTkLabel(app, text="⚠️ Preencha os campos de email e senha antes de enviar o email.", text_color="orange").pack(pady=10)
        return
    ctk.CTkButton(app, text="Enviar E-mail de Confirmação", command=enviar_email).pack(pady=10)
    host = "smtp.gmail.com" # servidor SMTP do Gmail
    port = 587  # porta para conexão TLS
    login = email_cadastrado 
    senha = senha_cadastrada

    server = smtplib.SMTP(host, port) 
    server.starttls()
    server.ehlo() 
    server.login(login, senha)


    detalhes_agendamento = corpo1_text if "corpo1_text" in globals() and corpo1_text is not None else "Detalhes do agendamento não disponíveis."
    corpo = 'Olá,\n\nSua consulta foi agendada com sucesso!\n\nDetalhes do agendamento:\n' + detalhes_agendamento + '\n\nAgradecemos por escolher nosso serviço.\n\nAtenciosamente,\nEquipe de Agendamento'
    email_msg = MIMEMultipart()
    email_msg['From'] = login
    email_msg['To'] = email_cadastrado
    email_msg['Subject'] = 'Confirmação de Agendamento'
    email_msg.attach(MIMEText(corpo, 'plain'))
    server.sendmail(login, email_cadastrado, email_msg.as_string())
    server.quit()

    ctk.CTkLabel(app, text="✅ E-mail enviado com sucesso!", text_color="green").pack(pady=10)
mostrar_login()  
app.mainloop()

