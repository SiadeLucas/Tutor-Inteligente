"""
Gerador de Boletim Oficial de Desempenho Escolar em PDF via ReportLab.
Em conformidade com docs-site/docs/modules/progresso/prototype/pdf-generator.md.
"""
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm


class BoletimPDFGenerator:
    """Compila o relatório formal de proficiência e domínio do estudante em PDF vetorial."""

    COR_PRIMARIA_LARANJA = colors.HexColor("#F57C00")
    COR_TEXTO_ESCURO = colors.HexColor("#1A1408")
    COR_FUNDO_CABECALHO = colors.HexColor("#FFF3E0")
    COR_BORDA_CARD = colors.HexColor("#FFB74D")

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
        scores_areas: list[dict],
    ) -> bytes:
        """
        Desenha o documento formal A4 e retorna os bytes do arquivo PDF compilado.
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=1.5 * cm,
            bottomMargin=1.5 * cm,
        )

        styles = getSampleStyleSheet()

        # Estilos tipográficos customizados
        titulo_style = ParagraphStyle(
            "TituloBoletim",
            parent=styles["Heading1"],
            fontSize=20,
            leading=24,
            textColor=cls.COR_PRIMARIA_LARANJA,
            fontName="Helvetica-Bold",
            spaceAfter=4,
        )
        subtitulo_style = ParagraphStyle(
            "SubtituloBoletim",
            parent=styles["Normal"],
            fontSize=10,
            textColor=colors.gray,
            spaceAfter=12,
        )
        h2_style = ParagraphStyle(
            "H2",
            parent=styles["Heading2"],
            fontSize=12,
            leading=15,
            textColor=cls.COR_TEXTO_ESCURO,
            fontName="Helvetica-Bold",
            spaceBefore=10,
            spaceAfter=6,
        )
        corpo_style = ParagraphStyle(
            "Corpo",
            parent=styles["Normal"],
            fontSize=9,
            leading=13,
            textColor=cls.COR_TEXTO_ESCURO,
        )
        corpo_center = ParagraphStyle(
            "CorpoCenter",
            parent=corpo_style,
            alignment=1,  # Centralizado
        )

        elementos = []

        # 1. Cabeçalho Institucional
        elementos.append(Paragraph("Tutor Inteligente — Matemática do Ensino Médio", titulo_style))
        elementos.append(
            Paragraph(
                "Boletim Oficial de Proficiência e Evolução Contínua (Coleção Gelson Iezzi)",
                subtitulo_style,
            )
        )
        elementos.append(HRFlowable(width="100%", thickness=1.5, color=cls.COR_PRIMARIA_LARANJA, spaceAfter=12))

        # 2. Dados Cadastrais do Aluno (com CPF mascarado)
        cpf_limpo = cpf_aluno.replace(".", "").replace("-", "").strip() if cpf_aluno else ""
        if len(cpf_limpo) == 11:
            cpf_mascarado = f"***.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-**"
        else:
            cpf_mascarado = "***.***.***-**"

        data_emissao = datetime.now().strftime("%d/%m/%Y às %H:%M")
        dados_cadastrais = [
            [
                Paragraph("<b>Aluno:</b>", corpo_style),
                Paragraph(nome_aluno or "Estudante", corpo_style),
                Paragraph("<b>Série / Ano:</b>", corpo_style),
                Paragraph(serie_ano or "Ensino Médio", corpo_style),
            ],
            [
                Paragraph("<b>CPF:</b>", corpo_style),
                Paragraph(cpf_mascarado, corpo_style),
                Paragraph("<b>Emissão:</b>", corpo_style),
                Paragraph(data_emissao, corpo_style),
            ],
        ]
        tabela_cadastral = Table(dados_cadastrais, colWidths=[2.2 * cm, 6.8 * cm, 2.5 * cm, 5.5 * cm])
        tabela_cadastral.setStyle(
            TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
            ])
        )
        elementos.append(tabela_cadastral)
        elementos.append(Spacer(1, 10))

        # 3. Métricas Tridimensionais em Destaque
        elementos.append(Paragraph("1. Resumo Executivo de Desempenho", h2_style))
        sinal_theta = f"{theta_geral:+.2f}"
        cards_metricas = [
            [
                Paragraph("<b>Proficiência Geral (TRI &theta;)</b>", corpo_center),
                Paragraph("<b>Nível de Maestria</b>", corpo_center),
                Paragraph("<b>Tempo Líquido Ativo</b>", corpo_center),
                Paragraph("<b>Capítulos Concluídos</b>", corpo_center),
            ],
            [
                Paragraph(f"<font size=13 color='#F57C00'><b>{sinal_theta}</b></font>", corpo_center),
                Paragraph(f"<font size=11><b>{nivel_classificacao}</b></font>", corpo_center),
                Paragraph(f"<font size=11>{horas_liquidas:.1f} horas</font>", corpo_center),
                Paragraph(f"<font size=11>{aulas_concluidas} capítulos</font>", corpo_center),
            ],
        ]
        tabela_resumo = Table(cards_metricas, colWidths=[4.25 * cm] * 4)
        tabela_resumo.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), cls.COR_FUNDO_CABECALHO),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 0.5, cls.COR_BORDA_CARD),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )
        elementos.append(tabela_resumo)
        elementos.append(Spacer(1, 12))

        # 4. Desempenho por Macro-Área (TRI & Taxa Ponderada)
        elementos.append(Paragraph("2. Avaliação por Macro-Áreas da Coleção Iezzi", h2_style))
        tabela_areas_data = [
            [
                Paragraph("<b>Macro-Área</b>", corpo_style),
                Paragraph("<b>Diagnóstico Entrada (&theta;)</b>", corpo_center),
                Paragraph("<b>Proficiência Atual (&theta;)</b>", corpo_center),
                Paragraph("<b>Evolução (&Delta;)</b>", corpo_center),
            ]
        ]

        for item in scores_areas:
            score_ent = float(item.get("score_entrada", 0.0))
            score_at = float(item.get("score_atual", 0.0))
            delta = score_at - score_ent
            sinal_delta = f"+{delta:.2f}" if delta >= 0 else f"{delta:.2f}"
            cor_delta = "green" if delta >= 0 else "red"
            tabela_areas_data.append([
                Paragraph(item.get("area", "Área"), corpo_style),
                Paragraph(f"{score_ent:+.2f}", corpo_center),
                Paragraph(f"<b>{score_at:+.2f}</b>", corpo_center),
                Paragraph(f"<font color='{cor_delta}'><b>{sinal_delta}</b></font>", corpo_center),
            ])

        tabela_areas = Table(tabela_areas_data, colWidths=[6.8 * cm, 3.4 * cm, 3.4 * cm, 3.4 * cm])
        tabela_areas.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), cls.COR_FUNDO_CABECALHO),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ])
        )
        elementos.append(tabela_areas)
        elementos.append(Spacer(1, 14))

        # 5. Parecer Pedagógico Conclusivo
        elementos.append(Paragraph("3. Parecer Pedagógico do Tutor", h2_style))
        parecer_texto = (
            f"O estudante demonstra trajetória de aprendizado estruturada, com nível psicométrico calibrado em "
            f"<b>&theta; = {sinal_theta}</b> (Classificação: <b>{nivel_classificacao}</b>). "
            f"Recomenda-se manter a rotina diária de 50 minutos de estudo ativo e priorizar as baterias "
            f"de reforço imediato e questões gêmeas nos tópicos com taxa de acerto ponderada inferior a 75%."
        )
        elementos.append(Paragraph(parecer_texto, corpo_style))

        # Compila o PDF
        doc.build(elementos)
        buffer.seek(0)
        return buffer.getvalue()
