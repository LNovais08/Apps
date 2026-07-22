import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "clinica.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def ensure_schema(db_path: str | Path | None = None):
    caminho_db = Path(db_path) if db_path is not None else DB_PATH
    conexao = sqlite3.connect(caminho_db)
    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT,
            data_nascimento TEXT,
            telefone TEXT,
            endereco TEXT,
            cidade TEXT,
            observacoes_medicas TEXT,
            cep TEXT,
            numero TEXT,
            uf TEXT,
            data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS consultas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            paciente_id INTEGER,
            data_consulta TEXT NOT NULL,
            horario TEXT NOT NULL,
            status TEXT DEFAULT 'PENDENTE',
            FOREIGN KEY (paciente_id) REFERENCES pacientes(id)
        )
        """
    )

    colunas_pacientes = {linha[1] for linha in cursor.execute("PRAGMA table_info(pacientes)").fetchall()}
    if "primeira_consulta" in colunas_pacientes:
        cursor.execute(
            """
            CREATE TABLE pacientes_novo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT,
                data_nascimento TEXT,
                telefone TEXT,
                endereco TEXT,
                cidade TEXT,
                observacoes_medicas TEXT,
                cep TEXT,
                numero TEXT,
                uf TEXT,
                data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO pacientes_novo (id, nome, cpf, data_nascimento, telefone, endereco, cidade, observacoes_medicas, cep, numero, uf, data_cadastro)
            SELECT id, nome, cpf, data_nascimento, telefone, endereco, cidade, observacoes_medicas, cep, numero, uf, data_cadastro
            FROM pacientes
            """
        )
        cursor.execute("DROP TABLE pacientes")
        cursor.execute("ALTER TABLE pacientes_novo RENAME TO pacientes")
        colunas_pacientes = {linha[1] for linha in cursor.execute("PRAGMA table_info(pacientes)").fetchall()}

    colunas_esperadas = {
        "cpf": "TEXT",
        "data_nascimento": "TEXT",
        "telefone": "TEXT",
        "endereco": "TEXT",
        "cidade": "TEXT",
        "observacoes_medicas": "TEXT",
        "cep": "TEXT",
        "numero": "TEXT",
        "uf": "TEXT",
        "data_cadastro": "DATETIME DEFAULT CURRENT_TIMESTAMP",
    }

    for coluna, definicao in colunas_esperadas.items():
        if coluna not in colunas_pacientes:
            cursor.execute(f"ALTER TABLE pacientes ADD COLUMN {coluna} {definicao}")

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    ensure_schema()
    print("Banco criado com sucesso!")