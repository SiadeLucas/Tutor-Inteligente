"""
Script assíncrono para semear usuários iniciais de teste (Estudante e Professor).
Execute com: python -m app.db.seed
"""
import asyncio
from datetime import date
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import hash_senha
from app.models.user import Usuario


async def seed():
    print("🌱 Iniciando inserção de dados de seed...")
    async with AsyncSessionLocal() as db:
        # 1. Aluno de Teste
        res_aluno = await db.execute(select(Usuario).where(Usuario.email == "aluno@tutorinteligente.com.br"))
        if not res_aluno.scalar_one_or_none():
            aluno = Usuario(
                cpf="11122233344",
                email="aluno@tutorinteligente.com.br",
                senha_hash=hash_senha("SenhaSegura123!"),
                nome_completo="Aluno Teste",
                data_nascimento=date(2008, 5, 15),
                idade_anos=16,
                eh_menor_idade=True,
                dados_responsavel={
                    "nome": "Responsável Teste",
                    "cpf": "99988877766",
                    "telefone": "11999998888",
                    "email": "responsavel@teste.com"
                },
                uf="SP",
                cidade="São Paulo",
                bairro="Pinheiros",
                cep="05400000",
                escola_tipo="publica",
                nome_escola="E.E. Cecília Meireles",
                serie_ano="2_ano",
                role="student",
                ativo=True
            )
            db.add(aluno)
            print("  ✅ Estudante inserido: aluno@tutorinteligente.com.br / SenhaSegura123!")
        else:
            print("  ℹ️ Estudante já existente.")

        # 2. Professor de Teste
        res_prof = await db.execute(select(Usuario).where(Usuario.email == "professor@tutorinteligente.com.br"))
        if not res_prof.scalar_one_or_none():
            professor = Usuario(
                cpf="22233344455",
                email="professor@tutorinteligente.com.br",
                senha_hash=hash_senha("SenhaSegura123!"),
                nome_completo="Professor Teste",
                data_nascimento=date(1985, 10, 20),
                idade_anos=39,
                eh_menor_idade=False,
                dados_responsavel=None,
                uf="SP",
                cidade="São Paulo",
                bairro="Bela Vista",
                cep="01310000",
                escola_tipo="outro",
                nome_escola="Plataforma Tutor Inteligente",
                serie_ano="todos",
                role="teacher",
                ativo=True
            )
            db.add(professor)
            print("  ✅ Professor inserido: professor@tutorinteligente.com.br / SenhaSegura123!")
        else:
            print("  ℹ️ Professor já existente.")

        await db.commit()
    print("🌱 Seed finalizado com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed())
