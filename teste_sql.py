import sqlite3

#banco_consultas=sqlite3.connect('teste_banco_consultas.db')


cursor=banco_consultas.cursor ()#através dele dá pra digitar os comandos, criar tabela, inserir registros...

cursor.execute("create table if not exists Profissionais (id Integer primary key autoincrement, Especialidade text, Nome text, Cidade text )"); #dados p criação da tabela

dados_profissionais= [
    ("Cardiologia", "Dr.Vinícius Gomes", "Recife"),
    ("Cardiologia", "Dr.Gabriel de Souza","Paulista" ),

    ("Clínica Geral", "Dr.Marcos André", "Olinda"),
    
    ("Endocrinologia", "Dr.José Gonçalves", "Olinda"),

    ("Ginecologia", "Dr.Pedro Alves", "Paulista"),
    ("Ginecologia", "Drª Ana Maria", "Olinda"),
    
    ("Nutrição", "Dr.João Paulo", "Recife"),
    ("Nutrição", "Drª Maria Alice", "Paulista"),

    ("Odontologia", "Drª Letícia Dias", "Olinda"),
    ("Odontologia", "Dr.Matheus Souza", "Paulista"),

    ("Oftalmologia", "Dr.Felipe Cunha", "Olinda"),

    ("Ortopedia", "Drª Marcela Andrade", "Recife"),
    ("Ortopedia", "Dr.Carlos Silva", "Paulista"),

    ("Pediatria", "Drª Alexandra Barros", "Recife"),

    ("Psiquiatria", "Dr.Rodrigo Pontes", "Recife")
]

#cursor.execute("create table Profissionais ( Especialidade text, Nome text primary key, Cidade text )"); #dados p criação da tabela

cursor.executemany ("insert into Profissionais (especialidade, nome, cidade) values(?,?,? )", dados_profissionais) # os "?" sao placeholders

banco_consultas.commit()

tabela=cursor.execute ("select * from Profissionais") #O select * pega tudo
tabela=cursor.fetchall() #o fetchall pega todas as linhas, e o fetchone pega so uma linha
for linha in tabela: 
    print (linha)

cursor.execute("select especialidade from profissionais")
especialidades=cursor.fetchall()
for especialidade in especialidades:
    print(especialidade) #mostra as especialidades

cursor.execute("select nome from profissionais")
nomes=cursor.fetchall()
for nome in nomes:
    print(nome) #mostra todos os nomes e sobrenomes dos profissionais

cursor.execute("select cidade from profissionais")
cidades=cursor.fetchall()
for cidade in cidades:
    print(cidade) # mostra as cidades disponíves para os atendimentos