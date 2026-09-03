---
title: Progresso - Gerador de Boletim Oficial em PDF (ReportLab)
type: module
status: draft
related:
  - modules/progresso/prototype/index.md
last_updated: "2026-09-03"
updated_by: claude
---

# 4. Gerador de Boletim Oficial em PDF (ReportLab)

Implementação da compilação do **Boletim de Desempenho Escolar em PDF** em Python puro via **ReportLab**, executando em sub-100ms sem dependências de sistema operacional ou navegadores headless.

---

## Código Fonte (`backend/app/modules/progress/pdf_generator.py`)

```python
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


class BoletimPDFGenerator:
    """Compila o relatório formal de proficiência e domínio do estudante."""

    COR_PRIMARIA_LARANJA = colors.HexColor("#F57C00")
    COR_TEXTO_ESCURO = colors.HexColor("#1A1408")
    COR_FUNDO_CABECALHO = colors.HexColor("#FFF3E0")

    @classmethod
    def gerar_boletim_bytes(
        cls,
        nome_aluno: str,
        cpf_aluno: str,
        serie_ano: str,
        theta_geral: float,
        nivel_classificacao: str,
        horas_liquidas: float,
        aulas_concluidas: int,
        scores_areas: list[dict]
    ) -> bytes:
        """
        Desenha o documento formal A4 e retorna os bytes do arquivo PDF.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm
        )

        styles = getSampleStyleSheet()

        # Estilos tipográficos customizados
        titulo_style = ParagraphStyle(
            "TituloBoletim",
            parent=styles["Heading1"],
            fontSize=22,
            leading=26,
            textColor=cls.COR_PRIMARIA_LARANJA,
            fontName="Helvetica-Bold",
            spaceAfter=4
        )
        subtitulo_style = ParagraphStyle(
            "SubtituloBoletim",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.gray,
            spaceAfter=15
        )
        h2_style = ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontSize=13,
            leading=16,
            textColor=cls.COR_TEXTO_ESCURO,
            fontName="Helvetica-Bold",
            spaceBefore=12,
            spaceAfter=8
        )
        corpo_style = ParagraphStyle(
            "Corpo",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=cls.COR_TEXTO_ESCURO
        )

        elementos = []

        # 1. Cabeçalho Institucional
        elementos.append(Paragraph("Tutor Inteligente — Matemática do 2º Grau", titulo_style))
        elementos.append(Paragraph("Boletim Oficial de Proficiência e Evolução Contínua (Coleção Gelson Iezzi)", subtitulo_style))
        elementos.append(HRFlowable(width="100%", thickness=1.5, color=cls.COR_PRIMARIA_LARANJA, spaceAfter=15))

        # 2. Dados Cadastrais do Aluno
        data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        dados_cadastrais = [
            [Paragraph("<b>Aluno:</b>", corpo_style), Paragraph(nome_aluno, corpo_style),
             Paragraph("<b>Série / Ano:</b>", corpo_style), Paragraph(serie_ano, corpo_style)],
            [Paragraph("<b>CPF:</b>", corpo_style), Paragraph(cpf_aluno, corpo_style),
             Paragraph("<b>Emissão:</b>", corpo_style), Paragraph(data_emissao, corpo_style)]
        ]
        tabela_cadastral = Table(dados_cadastrais, colWidths=[2.5 * cm, 6.5 * cm, 2.5 * cm, 5.5 * cm])
        tabela_cadastral.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        elementos.append(tabela_cadastral)
        elementos.append(Spacer(1, 15))

        # 3. Métricas Tridimensionais em Destaque
        elementos.append(Paragraph("1. Resumo Executivo de Desempenho", h2_style))
        cards_metricas = [
            [
                Paragraph("<b>Proficiência Geral (TRI &theta;)</b>", corpo_style),
                Paragraph("<b>Nível de Maestria</b>", corpo_style),
                Paragraph("<b>Tempo Líquido Ativo</b>", corpo_style),
                Paragraph("<b>Capítulos Entregues</b>", corpo_style)
            ],
            [
                Paragraph(f"<font size=14 color='#F57C00'><b>{theta_geral:+.2f}</b></font>", corpo_style),
                Paragraph(f"<font size=12><b>{nivel_classificacao}</b></font>", corpo_style),
                Paragraph(f"<font size=12>{horas_liquidas:.1f} horas</font>", corpo_style),
                Paragraph(f"<font size=12>{aulas_concluidas} capítulos</font>", corpo_style)
            ]
        ]
        tabela_resumo = Table(cards_metricas, colWidths=[4.25 * cm] * 4)
        tabela_resumo.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), cls.COR_FUNDO_CABECALHO),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#FFB74D")),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]))
        elementos.append(tabela_resumo)
        elementos.append(Spacer(1, 15))

        # 4. Desempenho por Macro-Área (TRI & Taxa Ponderada)
        elementos.append(Paragraph("2. Avaliação por Macro-Áreas da Coleção Iezzi", h2_style))
        tabela_areas_data = [
            [Paragraph("<b>Macro-Área</b>", corpo_style),
             Paragraph("<b>Diagnóstico Entrada (&theta;)</b>", corpo_style),
             Paragraph("<b>Proficiência Atual (&theta;)</b>", corpo_style),
             Paragraph("<b>Evolução</b>", corpo_style)]
        ]

        for item in scores_areas:
            delta = item["score_atual"] - item["score_entrada"]
            sinal_delta = f"+{delta:.2f}" if delta >= 0 else f"{delta:.2f}"
            cor_delta = "green" if delta >= 0 else "red"
            tabela_areas_data.append([
                Paragraph(item["area"], corpo_style),
                Paragraph(f"{item['score_entrada']:+.2f}", corpo_style),
                Paragraph(f"<b>{item['score_atual']:+.2f}</b>", corpo_style),
                Paragraph(f"<font color='{cor_delta}'><b>{sinal_delta}</b></font>", corpo_style)
            ])

        tabela_areas = Table(tabela_areas_data, colWidths=[7.0 * cm, 3.5 * cm, 3.5 * cm, 3.0 * cm])
        tabela_areas.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), cls.COR_FUNDO_CABECALHO),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        elementos.append(tabela_areas)
        elementos.append(Spacer(1, 20))

        # 5. Parecer Pedagógico Conclusivo
        elementos.append(Paragraph("3. Parecer Pedagógico do Tutor", h2_style))
        parecer_texto = (
            f"O estudante demonstra trajetória de aprendizado consistente, com proficiência estimada em "
            f"<b>&theta; = {theta_geral:+.2f}</b>. Recomenda-se manter a rotina ativa de 50 minutos diários "
            f"e priorizar as baterias de reforço dinâmico nos tópicos com taxa ponderada abaixo de 75%."
        )
        elementos.append(Paragraph(parecer_texto, corpo_style))

        # Compila o PDF
        doc.build(elementos)
        buffer.seek(0)
        return buffer.getvalue()
```
