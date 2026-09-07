"""
Configuração de fixtures para testes com pytest e pytest-asyncio.
Utiliza NullPool para garantir isolamento de conexões assíncronas por event loop.
"""
import pytest
import pytest_asyncio
from datetime import date
from httpx import AsyncClient, ASGITransport
from sqlalchemy import select, delete
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.core.config import settings
from app.core.database import get_db
from app.core.security import hash_senha
from app.models.user import Usuario, SessaoAtiva, TokenRecuperacaoSenha

# Engine de teste com NullPool para evitar conflito de event loops entre testes assíncronos
test_engine = create_async_engine(
    settings.DATABASE_URL,
    poolclass=NullPool
)
TestSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def override_get_db():
    """Substitui get_db nas rotas FastAPI durante os testes."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture
async def async_client():
    """Cliente HTTP assíncrono para testar endpoints FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest_asyncio.fixture
async def db_session():
    """Sessão direta de banco de dados para os testes com NullPool."""
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def usuario_teste(db_session):
    """Cria e retorna um usuário estudante de teste isolado."""
    email_teste = "aluno_teste_unitario@tutorinteligente.com.br"
    cpf_teste = "98765432100"
    senha_plana = "SenhaForte123@"

    # Limpeza prévia
    stmt_busca = select(Usuario).where(Usuario.email == email_teste)
    existente = (await db_session.execute(stmt_busca)).scalar_one_or_none()
    if existente:
        await db_session.delete(existente)
        await db_session.commit()

    # Criação
    usuario = Usuario(
        cpf=cpf_teste,
        email=email_teste,
        senha_hash=hash_senha(senha_plana),
        nome_completo="Aluno Teste Unitário",
        data_nascimento=date(2007, 3, 10),
        idade_anos=17,
        eh_menor_idade=True,
        dados_responsavel={"nome": "Responsável", "cpf": "00011122233"},
        uf="SP",
        cidade="São Paulo",
        cep="01001000",
        escola_tipo="publica",
        serie_ano="3_ano",
        role="student",
        ativo=True
    )
    db_session.add(usuario)
    await db_session.commit()
    await db_session.refresh(usuario)

    yield {
        "id": usuario.id,
        "email": email_teste,
        "cpf": cpf_teste,
        "senha_plana": senha_plana,
        "role": "student",
        "usuario_obj": usuario
    }

    # Limpeza pós-teste
    await db_session.execute(delete(SessaoAtiva).where(SessaoAtiva.usuario_id == usuario.id))
    await db_session.execute(delete(TokenRecuperacaoSenha).where(TokenRecuperacaoSenha.usuario_id == usuario.id))
    await db_session.execute(delete(Usuario).where(Usuario.id == usuario.id))
    await db_session.commit()
