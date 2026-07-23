import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "db" / "clinica.db"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


def buscar_pacientes_agenda():
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome FROM pacientes ORDER BY nome")
    dados = cursor.fetchall()
    conexao.close()
    return dados


def inserir_consulta(paciente_id, data_consulta, horario, status="PENDENTE"):
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute(
        """
        INSERT INTO consultas (paciente_id, data_consulta, horario, status)
        VALUES (?, ?, ?, ?)
        """,
        (paciente_id, data_consulta, horario, status),
    )
    conexao.commit()
    conexao.close()


def buscar_consultas_do_mes(ano, mes):
    ensure_schema(_get_db_path())
    conexao = sqlite3.connect(_get_db_path())
    cursor = conexao.cursor()
    cursor.execute(
        """
        SELECT c.data_consulta, c.horario, c.status, p.nome
        FROM consultas c
        JOIN pacientes p ON p.id = c.paciente_id
        WHERE strftime('%Y', c.data_consulta) = ?
          AND strftime('%m', c.data_consulta) = ?
        ORDER BY c.data_consulta, c.horario
        """,
        (str(ano), f"{mes:02d}"),
    )
    dados = cursor.fetchall()
    conexao.close()
    return dados


def _get_db_path() -> Path:
    return DB_PATH


def ensure_schema(db_path: Path | None = None):
    caminho_db = Path(db_path) if db_path is not None else DB_PATH
    ensure_schema(caminho_db)


def ensure_schema(db_path: Path):
    db_path.parent.mkdir(parents=True, exist_ok=True)

    conexao = sqlite3.connect(db_path)
    cursor = conexao.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS pacientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT NOT NULL,
            data_nascimento TEXT NOT NULL,
            telefone TEXT NOT NULL,
            email TEXT,
            endereco TEXT NOT NULL,
            cidade TEXT NOT NULL,
            observacoes_medicas TEXT NOT NULL,
            cep TEXT NOT NULL,
            numero TEXT NOT NULL,
            uf TEXT NOT NULL,
            data_cadastro TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute("PRAGMA table_info(pacientes)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "email" not in colunas:
        cursor.execute("ALTER TABLE pacientes ADD COLUMN email TEXT")

    conexao.commit()
    conexao.close()


if __name__ == "__main__":
    ensure_schema()
    print("Banco criado com sucesso!")