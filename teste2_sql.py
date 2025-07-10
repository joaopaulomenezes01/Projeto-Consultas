import sqlite3
import random
from datetime import date,timedelta

#banco_consultas=sqlite3.connect('teste_banco_consultas.db')
banco_consultas = sqlite3.connect(r'C:\Users\Acer\Desktop\projeto rodrigo\teste_banco_consultas.db')

cursor=banco_consultas.cursor ()

cursor.execute("create table if not exists Regioes (id Integer primary key autoincrement, nome text )")

cursor.execute("create table if not exists Cidades (id Integer primary key autoincrement, nome text, id_regiao Integer, foreign key (id_regiao) references Regioes(id) )") 

cursor.execute("create table if not exists Especialidades (id Integer primary key autoincrement, nome text)"); #tabela de especialidades

cursor.execute ("create table if not exists Profissionais(id Integer primary key autoincrement, nome Text, id_especialidade Integer, foreign key (id_especialidade) references Especialidades(id))")

cursor.execute("create table if not exists Profissional_na_cidade (id_profissional Integer, id_cidade Integer, foreign key(id_profissional) references Profissionais(id), foreign key(id_cidade) references Cidades(id))")

cursor.execute("create table if not exists Disponibilidade (id Integer primary key autoincrement, id_profissional Integer, data text, hora text, disponivel boolean not null, foreign key(id_profissional) references Profissionais(id))")

Regioes_de_cobertura= ["Região Metropolitana", "Agreste", "Sertão"]

Regioes= [("Região Metropolitana", "Recife"),
          ("Região Metropolitana", "Paulista"),
          ("Região Metropolitana", "Olinda"),
          
          ("Agreste", "Garanhuns"),
          ("Agreste","Caruaru" ),
          ("Agreste", "Vitória de Santo Antão"),
          ("Agreste", "Bezerros"),
          ("Agreste", "Gravatá"),
          
          ("Sertão", "Petrolina"),
          ("Sertão", "Floresta"),
          ("Sertão", "Serra Talhada"),
          ("Sertão", "Arcoverde"),
          ("Sertão", "Salgueiro") ]

Especialidades_oferecidas = [
    "Cardiologia", "Clínica Geral", "Endocrinologia", "Ginecologia",
    "Nutrição", "Odontologia", "Oftalmologia", "Ortopedia",
    "Pediatria", "Psiquiatria"
]
dados_profissionais = [
    ("Cardiologia", "Dr.Vinícius Gomes"),
    ("Cardiologia", "Dr.Gabriel de Souza"),
    ("Cardiologia", "Drª Bárbara Vitória"),
    ("Cardiologia", "Dr.Bruno Carvalho"),
    ("Cardiologia", "Dr.Manoella Silva"),
    ("Cardiologia", "Drª Dandara Cruz"),
    ("Cardiologia", "Dr.Celso da Luz"),
    
    ("Clínica Geral", "Dr.Marcos André"),
    ("Clínica Geral", "Dr.Wallace Bernardo"),
    ("Clínica Geral", "Drª Beatriz Dias"),
    ("Clínica Geral", "Drª Brenda Maria"),
    ("Clínica Geral", "Dr.Breno Campos"),
    ("Clínica Geral", "Dr.Bernardo Maia"),
    ("Clínica Geral", "Drª Luíza Rebecca"),
    ("Clínica Geral", "Drª Laíza Santos"),
    
    ("Endocrinologia", "Dr.José Gonçalves"),
    ("Endocrinologia", "Drª Mirella Alves"),
    ("Endocrinologia", "Dr.Thiago Ribeiro"),
    ("Endocrinologia", "Dr.João Victor"),
    ("Endocrinologia", "Dr.Arthur Rebouças"),
    ("Endocrinologia", "Dr.Cleiton Pereira"),
    ("Endocrinologia", "Drª Danielle Larissa"),
    ("Endocrinologia", "Drª Diana Cavallazi"),
    
    ("Ginecologia", "Dr.Pedro Alves"),
    ("Ginecologia", "Drª Ana Maria"),
    ("Ginecologia", "Drª Bruna Rodrigues"),
    ("Ginecologia", "Drª Luana Maria"),
    ("Ginecologia", "Drª Luna Ribeiro"),
    ("Ginecologia", "Dr.Alessandro Victor"),
    ("Ginecologia", "Dr.Miguel da Costa"),
    
    ("Nutrição", "Dr.João Paulo"),
    ("Nutrição", "Drª Maria Alice"),
    ("Nutrição", "Drª Kayllane Letícia"),
    ("Nutrição", "Drª Victória Almeida"),
    ("Nutrição", "Dr. Alex de Teixeira"),
    ("Nutrição", "Dr. Kléber Eduardo"),
    ("Nutrição", "Dr. Kleyton Paulo"),
    
    ("Odontologia", "Drª Letícia Dias"),
    ("Odontologia", "Dr.Matheus Souza"),
    ("Odontologia", "Dr.Rhuan Barros"),
    ("Odontologia", "Drª Gleice Batista,"),
    ("Odontologia", "Drª Jennifer Barbosa"),
    ("Odontologia", "Dr.Pablo Arruda"),
    ("Odontologia", "Drª Esther Silva"),
    ("Odontologia", "Dr.Samuel Queiroz"),
    
    ("Oftalmologia", "Dr.Felipe Cunha"),
    ("Oftalmologia", "Dr.Leandro Moura"),
    ("Oftalmologia", "Drª Laura Campos"),
    ("Oftalmologia", "Drª Victória Borges"),
    ("Oftalmologia", "Drª Laura Campos"),
    ("Oftalmologia", "Drª Selma Morais"),
    ("Oftalmologia", "Drª Maura Fontes"),
    ("Oftalmologia", "Dr.Jonas do Nascimento"),
    
    ("Ortopedia", "Drª Marcela Andrade"),
    ("Ortopedia", "Drª Carolina Oliveira"),
    ("Ortopedia", "Drª Suellen Ferreira"),
    ("Ortopedia", "Dr.Carlos Silva"),
    ("Ortopedia", "Dr.Rennan Nunes"),
    ("Ortopedia", "Dr.Christiano Fernando"),
    ("Ortopedia", "Dr.Luciano Neves"),
    ("Ortopedia", "Drª Fernanda Ramos"),
    
    ("Pediatria", "Drª Alexandra Barros"),
    ("Pediatria", "Drª Camila Ramos"),
    ("Pediatria", "Dr.Diego dos Reis"),
    ("Pediatria", "Dr.Jorge Montes"),
    ("Pediatria", "Drª Lucinda da Rocha"),
    ("Pediatria", "Drª Priscilla Fontes"),
    ("Pediatria", "Dr. Ronaldo Santana"),
    
    ("Psiquiatria", "Dr.Rodrigo Pontes"),
    ("Psiquiatria", "Drª Juliana Cunha"),
    ("Psiquiatria", "Drª Eliana Teixeira"),
    ("Psiquiatria", "Dr.Davi Soares"),
    ("Psiquiatria", "Dr. Enzo Vieira"),
    ("Psiquiatria", "Drª Valentina Eduarda")]


ids_profissionais=[]
for linha in cursor.execute("select id from Profissionais"):
    ids_profissionais.append(linha[0])

ids_cidades=[]
for linha in cursor.execute("select id from Cidades"):
    ids_cidades.append(linha[0])

horarios=["08:00", "09:00", "10:00", "14:00", "15:00", "16:00"]

data=date.today()
dias_de_semana=[]
while len(dias_de_semana) <30: 
    if data.weekday()<5:
        dias_de_semana.append(data)
        data+=timedelta(days=1)
Disponibilidade_profissionais=[]


for regiao in Regioes_de_cobertura:
    cursor.execute("insert into Regioes (nome) VALUES (?)", (regiao,))

for regiao, cidade in Regioes:
    cursor.execute("insert into Cidades (nome, id_regiao) values (?, (select id from Regioes where nome= ? ))", (cidade,regiao))

for especialidade in Especialidades_oferecidas:
    cursor.execute("insert into Especialidades(nome) values (?)", (especialidade,))

for especialidade, nome in dados_profissionais:
    cursor.execute("insert into Profissionais (nome, id_especialidade) values (?,(select id from Especialidades where nome= ?))",(nome,especialidade))

for id_profissional in ids_profissionais:
    cidades_de_atendimento=random.sample(ids_cidades, 2)
    for cidade in cidades_de_atendimento:
        cursor.execute("insert into Profissional_na_cidade(id_profissional, id_cidade) values (?,?)", (id_profissional, cidade))

for id_profissional in ids_profissionais:
    for data in dias_de_semana:
        data_str=data.strftime("%Y-%m-%d")
        for hora in horarios:
            Disponibilidade_profissionais.append((id_profissional,data_str,hora,1))
cursor.executemany("insert into Disponibilidade (id_profissional, data,hora,disponivel) values (?,?,?,?)", Disponibilidade_profissionais)

banco_consultas.commit()
