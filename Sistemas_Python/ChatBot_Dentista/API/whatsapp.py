from contextlib import asynccontextmanager
from datetime import date, datetime, time
import logging
import os
import re
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Time, create_engine, text
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker
from pathlib import Path
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

load_dotenv(Path(__file__).with_name(".env"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parent.parent / "db" / "clinica.db"
DATABASE_URL = f"sqlite:///{DB_PATH.as_posix()}"
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USER)


class Base(DeclarativeBase):
    pass


class Paciente(Base):
    __tablename__ = "pacientes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    consultas: Mapped[list["Consulta"]] = relationship(back_populates="paciente")


class Consulta(Base):
    __tablename__ = "consultas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id"), nullable=False, index=True)
    data: Mapped[date] = mapped_column(Date, nullable=False, index=True)
    horario: Mapped[time] = mapped_column(Time, nullable=False)
    lembrete_enviado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    lembrete_enviado_em: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    paciente: Mapped[Paciente] = relationship(back_populates="consultas")


class PacienteCreate(BaseModel):
    nome: str = Field(..., min_length=2)
    email: EmailStr | None = None


class ConsultaCreate(BaseModel):
    paciente_id: int
    data: date
    horario: time


class EmailTeste(BaseModel):
    email: EmailStr
    nome: str = "Paciente"
    mensagem: str | None = None


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")


def _migrar_schema_legado():
    with engine.begin() as conn:
        # ---- pacientes.email
        cols_pac = {row[1] for row in conn.execute(text("PRAGMA table_info(pacientes)")).fetchall()}
        if "email" not in cols_pac:
            conn.execute(text("ALTER TABLE pacientes ADD COLUMN email VARCHAR(255)"))

        # ---- consultas colunas novas
        cols_cons = {row[1] for row in conn.execute(text("PRAGMA table_info(consultas)")).fetchall()}

        if "data" not in cols_cons:
            conn.execute(text("ALTER TABLE consultas ADD COLUMN data DATE"))
        if "horario" not in cols_cons:
            conn.execute(text("ALTER TABLE consultas ADD COLUMN horario TIME"))
        if "lembrete_enviado" not in cols_cons:
            conn.execute(text("ALTER TABLE consultas ADD COLUMN lembrete_enviado BOOLEAN DEFAULT 0"))
        if "lembrete_enviado_em" not in cols_cons:
            conn.execute(text("ALTER TABLE consultas ADD COLUMN lembrete_enviado_em DATETIME"))

        # opcional: tenta copiar de colunas legadas, se existirem
        cols_cons = {row[1] for row in conn.execute(text("PRAGMA table_info(consultas)")).fetchall()}
        if "data_consulta" in cols_cons:
            conn.execute(text("UPDATE consultas SET data = data_consulta WHERE data IS NULL"))
        if "hora_consulta" in cols_cons:
            conn.execute(text("UPDATE consultas SET horario = hora_consulta WHERE horario IS NULL"))


def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    _migrar_schema_legado()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class EmailGateway:
    async def send_text(self, to: str, subject: str, text: str) -> dict:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = EMAIL_FROM
        msg["To"] = to
        msg.set_content(text)

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)

        return {"status": "sent", "to": to}


def email_valido(email: str | None) -> str | None:
    if not email:
        return None
    email = email.strip()
    if re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return email
    return None


def montar_mensagem(nome: str, data_consulta: date, horario: time) -> str:
    return (
        f"Olá, {nome}!\n\n"
        f"Lembrete: sua consulta é hoje.\n"
        f"Data: {data_consulta.strftime('%d/%m/%Y')}\n"
        f"Horário: {horario.strftime('%H:%M')}\n\n"
        "Clínica Odontológica"
    )

async def enviar_lembretes_do_dia() -> dict:
    db = SessionLocal()
    gateway = EmailGateway()
    try:
        hoje = date.today()
        consultas = (
            db.query(Consulta)
            .join(Paciente)
            .filter(Consulta.data == hoje, Consulta.lembrete_enviado.is_(False))
            .all()
        )

        enviados, erros = 0, 0
        detalhes_erros = []

        for consulta in consultas:
            paciente = consulta.paciente
            destino = email_valido(paciente.email)

            if not destino:
                erros += 1
                detalhes_erros.append(
                    {"paciente_id": paciente.id, "nome": paciente.nome, "motivo": "E-mail ausente ou inválido"}
                )
                continue

            try:
                mensagem = montar_mensagem(paciente.nome, consulta.data, consulta.horario)
                await gateway.send_text(destino, "Lembrete de consulta", mensagem)
                consulta.lembrete_enviado = True
                consulta.lembrete_enviado_em = datetime.now()
                db.commit()
                enviados += 1
            except Exception as exc:
                db.rollback()
                erros += 1
                detalhes_erros.append(
                    {"paciente_id": paciente.id, "nome": paciente.nome, "email": destino, "motivo": str(exc)}
                )

        return {
            "consultas_encontradas": len(consultas),
            "mensagens_enviadas": enviados,
            "erros": erros,
            "detalhes_erros": detalhes_erros,
        }
    finally:
        db.close()

# agenda diária às 08:00
@asynccontextmanager
async def lifespan(app: FastAPI):
    criar_tabelas()
    scheduler.add_job(
        enviar_lembretes_do_dia,
        CronTrigger(hour=8, minute=0),
        id="lembretes_08h",
        replace_existing=True,
    )
    scheduler.start()
    yield
    scheduler.shutdown(wait=False)


app = FastAPI(title="API Lembretes por E-mail", lifespan=lifespan)


@app.get("/")
def root():
    return {"status": "ok", "service": "lembretes-email"}


@app.post("/pacientes")
def criar_paciente(payload: PacienteCreate, db: Session = Depends(get_db)):
    email = payload.email.strip().lower() if payload.email else None
    paciente = Paciente(nome=payload.nome, email=email)
    db.add(paciente)
    db.commit()
    db.refresh(paciente)
    return paciente


@app.post("/consultas")
def criar_consulta(payload: ConsultaCreate, db: Session = Depends(get_db)):
    paciente = db.get(Paciente, payload.paciente_id)
    if not paciente:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    consulta = Consulta(
        paciente_id=payload.paciente_id,
        data=payload.data,
        horario=payload.horario,
    )
    db.add(consulta)
    db.commit()
    db.refresh(consulta)
    return consulta


@app.post("/lembretes/rodar-agora")
async def rodar_lembretes_agora():
    return await enviar_lembretes_do_dia()


@app.post("/emails/teste")
async def enviar_email_teste(payload: EmailTeste):
    gateway = EmailGateway()
    mensagem = payload.mensagem or f"Olá, {payload.nome}! Este é um e-mail de teste."
    resultado = await gateway.send_text(payload.email, "Teste de envio", mensagem)
    return {"status": "ok", "resultado": resultado}