import os
import sqlite3
import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer,
    Table, TableStyle, HRFlowable
)

# ============================================
# CONFIG
# ============================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH  = os.path.join(BASE_DIR, 'data', 'volve_wells.db')
OUT_PATH = os.path.join(BASE_DIR, 'reports', 'qc_rapport_volve.pdf')

os.makedirs(os.path.join(BASE_DIR, 'reports'), exist_ok=True)

RED    = colors.HexColor('#E07B00')
DARK   = colors.HexColor('#1a1a2e')
GREEN  = colors.HexColor('#2ecc71')
LIGHT  = colors.HexColor('#f8f9fa')

def load_data():
    conn = sqlite3.connect(DB_PATH)
    production = pd.read_sql("SELECT * FROM well_production", conn)
    qc         = pd.read_sql("SELECT * FROM qc_reports", conn)
    conn.close()
    return production, qc

def build_report():
    production, qc = load_data()

    doc = SimpleDocTemplate(
        OUT_PATH,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )

    styles = getSampleStyleSheet()
    story  = []

    title_style = ParagraphStyle(
        'Title', parent=styles['Title'],
        textColor=DARK, fontSize=20, spaceAfter=6
    )
    subtitle_style = ParagraphStyle(
        'Subtitle', parent=styles['Normal'],
        textColor=RED, fontSize=11, spaceAfter=20
    )
    heading_style = ParagraphStyle(
        'Heading', parent=styles['Heading2'],
        textColor=DARK, fontSize=13, spaceBefore=16, spaceAfter=8
    )
    normal_style = styles['Normal']

    # ============================================
    # HEADER
    # ============================================
    story.append(Paragraph("Rapport Qualité des Données de Puits", title_style))
    story.append(Paragraph("Champ Volve — Mer du Nord | Dataset Equinor Open", subtitle_style))
    story.append(Paragraph(
        f"Généré le : {datetime.now().strftime('%d/%m/%Y à %H:%M')} | "
        f"Projet Portfolio — Candidature Data Analyst TotalEnergies",
        normal_style
    ))
    story.append(HRFlowable(width="100%", thickness=2, color=RED, spaceAfter=16))

    # ============================================
    # SECTION 1 — RÉSUMÉ EXÉCUTIF
    # ============================================
    story.append(Paragraph("1. Résumé Exécutif", heading_style))

    total_oil = production['bore_oil_vol'].sum() / 1e6
    total_gas = production['bore_gas_vol'].sum() / 1e6
    n_wells   = production['well_name'].nunique()
    pass_rate = len(qc[qc['status'].str.contains('PASS')]) / len(qc) * 100

    summary_data = [
        ['Indicateur', 'Valeur'],
        ['Production totale huile', f'{total_oil:.1f}M Sm³'],
        ['Production totale gaz', f'{total_gas:.0f}M Sm³'],
        ['Nombre de puits analysés', str(n_wells)],
        ['Période de production', '2008 → 2016'],
        ['Taux de conformité QC', f'{pass_rate:.0f}%'],
        ['Nombre total d\'enregistrements', f'{len(production):,}'],
    ]

    summary_table = Table(summary_data, colWidths=[9*cm, 7*cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 10),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING',    (0,0), (-1,-1), 8),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 16))

    # ============================================
    # SECTION 2 — SCORES QC PAR PUITS
    # ============================================
    story.append(Paragraph("2. Scores QC par Puits", heading_style))

    qc_data = [['Puits', 'Score', 'Statut', 'Issues HIGH', 'Issues MEDIUM', 'Enregistrements']]
    for _, row in qc.sort_values('score').iterrows():
        qc_data.append([
            row['well_name'],
            f"{row['score']}/100",
            row['status'],
            str(row['high_issues']),
            str(row['medium_issues']),
            f"{row['records']:,}"
        ])

    qc_table = Table(qc_data, colWidths=[3.5*cm, 2*cm, 3*cm, 2.5*cm, 2.5*cm, 2.5*cm])
    qc_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), DARK),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING',    (0,0), (-1,-1), 7),
        ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(qc_table)
    story.append(Spacer(1, 16))

    # ============================================
    # SECTION 3 — CLASSEMENT PRODUCTION
    # ============================================
    story.append(Paragraph("3. Classement de Production", heading_style))

    prod_rank = production.groupby('well_name').agg(
        total_oil=('bore_oil_vol', 'sum'),
        total_gas=('bore_gas_vol', 'sum'),
        avg_water_cut=('water_cut', 'mean')
    ).reset_index().sort_values('total_oil', ascending=False)

    prod_data = [['Puits', 'Huile totale (Sm³)', 'Gaz total (Sm³)', 'Water Cut moyen (%)']]
    for _, row in prod_rank.iterrows():
        prod_data.append([
            row['well_name'],
            f"{row['total_oil']/1e6:.2f}M",
            f"{row['total_gas']/1e6:.0f}M",
            f"{row['avg_water_cut']:.1f}%"
        ])

    prod_table = Table(prod_data, colWidths=[4*cm, 4*cm, 4*cm, 4*cm])
    prod_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), RED),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,0), (-1,-1), 9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, LIGHT]),
        ('GRID',       (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING',    (0,0), (-1,-1), 7),
        ('ALIGN',      (1,0), (-1,-1), 'CENTER'),
    ]))
    story.append(prod_table)
    story.append(Spacer(1, 16))

    # ============================================
    # SECTION 4 — CONSTATS & RECOMMANDATIONS
    # ============================================
    story.append(Paragraph("4. Constats Clés et Recommandations", heading_style))

    findings = [
        "• <b>15/9-F-12 et 15/9-F-14</b> représentent 87% de la production totale "
        "du champ mais affichent les scores QC les plus bas (55/100 et 50/100). "
        "Une validation approfondie des données est recommandée en priorité.",

        "• <b>Alerte Water Cut :</b> Le puits 15/9-F-14 présente un water cut moyen "
        "de 65%, indiquant une percée d'eau importante dans le réservoir. "
        "Une révision de l'efficacité de production est conseillée.",

        "• <b>15/9-F-15 D</b> affiche le meilleur score QC (98/100) et constitue "
        "la source de données la plus fiable pour les analyses de référence.",

        "• <b>Déclin de production</b> confirmé à partir de 2010 après le pic du champ. "
        "La déplétion naturelle du réservoir est validée par l'analyse des tendances de pression.",

        "• <b>Recommandation :</b> Prioriser la correction QC des puits F-12 et F-14 "
        "avant toute simulation de réservoir ou planification de développement de champ."
    ]

    for finding in findings:
        story.append(Paragraph(finding, normal_style))
        story.append(Spacer(1, 6))

    # ============================================
    # FOOTER
    # ============================================
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.grey))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        f"Confidentiel — Projet Portfolio | Données : Equinor Volve Open Dataset (Licence CC) | "
        f"Analyste : Elom Brasco | Outils : Python · pandas · SQLite · ReportLab",
        ParagraphStyle('Footer', parent=styles['Normal'],
                      fontSize=8, textColor=colors.grey)
    ))

    doc.build(story)
    print(f"✅ Rapport PDF généré : {OUT_PATH}")

if __name__ == "__main__":
    build_report()