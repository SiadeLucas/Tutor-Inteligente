"""
Script assíncrono para semear usuários iniciais de teste (Estudante e Professor).
Execute com: python -m app.db.seed
"""
import asyncio
from datetime import date, datetime, timedelta, timezone
from sqlalchemy import select

from app.core.database import AsyncSessionLocal
from app.core.security import hash_senha
from app.models.user import Usuario
from app.models.payment import MatriculaPagamento


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
        professor = res_prof.scalar_one_or_none()
        if not professor:
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

        # 3. Administrador de Teste com Acesso Completo Irrestrito
        res_admin = await db.execute(select(Usuario).where(Usuario.email == "admin@tutorinteligente.com.br"))
        admin = res_admin.scalar_one_or_none()
        if not admin:
            admin = Usuario(
                cpf="11144477735",
                email="admin@tutorinteligente.com.br",
                senha_hash=hash_senha("SenhaSegura123!"),
                nome_completo="Administrador Tutor",
                data_nascimento=date(1990, 1, 1),
                idade_anos=34,
                eh_menor_idade=False,
                dados_responsavel=None,
                uf="SP",
                cidade="São Paulo",
                bairro="Centro",
                cep="01001000",
                escola_tipo="outro",
                nome_escola="Administração Tutor Inteligente",
                serie_ano="todos",
                role="admin",
                ativo=True
            )
            db.add(admin)
            await db.flush()
            print("  ✅ Administrador inserido: admin@tutorinteligente.com.br / SenhaSegura123!")
        else:
            admin.role = "admin"
            print("  ℹ️ Administrador já existente.")

        await db.flush()

        # 4. Conceder Matrícula Passe Global para Admin e Professor (10 anos de vigência)
        for u in [admin, professor]:
            if u:
                res_mat = await db.execute(
                    select(MatriculaPagamento).where(
                        MatriculaPagamento.usuario_id == u.id,
                        MatriculaPagamento.tipo_produto == "passe_global",
                        MatriculaPagamento.status == "active",
                    )
                )
                if not res_mat.scalar_one_or_none():
                    matricula_admin = MatriculaPagamento(
                        usuario_id=u.id,
                        tipo_produto="passe_global",
                        referencia_produto_id=None,
                        data_inicio=datetime.now(timezone.utc),
                        data_expiracao=datetime.now(timezone.utc) + timedelta(days=3650),
                        status="active",
                        valor_pago=0.00,
                        metodo_pagamento="sistema_admin",
                        transacao_gateway_id="admin_bypass_master",
                    )
                    db.add(matricula_admin)
                    print(f"  👑 Passe Global concedido para {u.email} (acesso 100% irrestrito).")

        # Também concede passe global para o usuário Lucas Siade se presente
        res_siade = await db.execute(select(Usuario).where(Usuario.email == "siadereak@gmail.com"))
        siade_user = res_siade.scalar_one_or_none()
        if siade_user:
            res_mat_s = await db.execute(
                select(MatriculaPagamento).where(
                    MatriculaPagamento.usuario_id == siade_user.id,
                    MatriculaPagamento.tipo_produto == "passe_global",
                    MatriculaPagamento.status == "active",
                )
            )
            if not res_mat_s.scalar_one_or_none():
                matricula_siade = MatriculaPagamento(
                    usuario_id=siade_user.id,
                    tipo_produto="passe_global",
                    referencia_produto_id=None,
                    data_inicio=datetime.now(timezone.utc),
                    data_expiracao=datetime.now(timezone.utc) + timedelta(days=3650),
                    status="active",
                    valor_pago=0.00,
                    metodo_pagamento="sistema_admin",
                    transacao_gateway_id="dev_bypass_master",
                )
                db.add(matricula_siade)
                print(f"  👑 Passe Global concedido para {siade_user.email}.")

        await db.commit()
    print("🌱 Seed finalizado com sucesso!")


if __name__ == "__main__":
    asyncio.run(seed())
