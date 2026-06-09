import sqlite3

conexao = sqlite3.connect("ChatBot_Dentista/db/clinica.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT UNIQUE NOT NULL,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS consultas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    paciente_id INTEGER,
    data_consulta TEXT NOT NULL,
    horario TEXT NOT NULL,
    status TEXT DEFAULT 'PENDENTE',
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
)
""")

conexao.commit()
conexao.close()

print("Banco criado com sucesso!")