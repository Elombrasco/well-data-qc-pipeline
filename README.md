# 🛢️ Well Data Quality Control Pipeline
> **Portfolio project** 

## 🚀 Live Dashboard
👉 **[Voir le dashboard en ligne](https://volve-well-qc.streamlit.app)**

---

## 🎯 Business Problem

Equinor opère des milliers de puits à travers le monde. Les données de diagraphies collectées proviennent de sources hétérogènes — prestataires, équipes terrain, bases historiques. Des données mal qualifiées entraînent :

- Des **erreurs d'interprétation géologique** coûteuses
- Des **retards de décision** sur les projets d'exploration
- Un **travail manuel répétitif** pour les géoscientifiques

> **Impact business visé :** Réduire le temps de validation manuelle des données de puits de ~70% grâce à un pipeline automatisé de Quality Control.

---

## 🔗 Objectifs

|Ce que ce projet démontre |
|---|---|
| Inventaire & collecte des données puits | ✅ Phase PREPARE |
| Harmonisation & standardisation | ✅ Phase PROCESS |
| Contrôle qualité automatisé | ✅ QC Engine — 5 règles automatisées |
| Reporting aux équipes géosciences | ✅ Rapport PDF automatisé |
| Automatisation des workflows | ✅ Pipeline Python bout-en-bout |

---

## 🔄 Méthodologie — Google Data Analytics Framework

| Phase | Description | Livrable |
|---|---|---|
| ❓ ASK | Définition des questions business | 5 questions KPI |
| 📦 PREPARE | Téléchargement et exploration du dataset Volve | Notebook EDA |
| ⚙️ PROCESS | Nettoyage, harmonisation, déduplication | CSV propre |
| 📊 ANALYZE | Production, water cut, pression, déclin | 4 insights business |
| 📤 SHARE | Dashboard interactif + rapport PDF | Streamlit + PDF |

---

## 📊 Résultats Clés

🥇 15/9-F-12  → 4.5M Sm³ huile  | Score QC : 55/100 ❌
🥈 15/9-F-14  → 3.9M Sm³ huile  | Score QC : 50/100 ❌
⚠️  Water Cut  → F-14 = 65% eau  | Coût de traitement élevé
📉 Déclin      → Peak 2009-2010  | Déplétion naturelle confirmée
✅ 15/9-F-15D → Score QC 98/100 | Données les plus fiables

---

## 🏗️ Architecture du projet

| Dossier / Fichier | Description |
|---|---|
| `data/Volve production data.xlsx` | Dataset brut — Equinor Open Dataset |
| `data/volve_production_clean.csv` | Données nettoyées (0 doublon, 0 null) |
| `data/volve_wells.db` | Base de données SQLite structurée |
| `notebooks/01_EDA.ipynb` | Exploration + nettoyage (PREPARE & PROCESS) |
| `src/qc_engine.py` | Moteur QC automatisé — 5 règles de qualité |
| `src/db_loader.py` | Chargement des données dans SQLite |
| `src/pdf_report.py` | Génération du rapport PDF automatisé |
| `dashboard/app.py` | Dashboard Streamlit interactif |
| `reports/qc_rapport_volve.pdf` | Rapport QC généré en français |
| `requirements.txt` | Dépendances Python du projet |

---

## 🛠️ Stack Technique

`Python 3.13` · `pandas` · `plotly` · `streamlit` · `SQLite` · `SQLAlchemy` · `ReportLab` · `Git`

---

## 📦 Installation locale

```bash
# Clone le repo
git clone https://github.com/Elombrasco/well-data-qc-pipeline.git
cd well-data-qc-pipeline

# Crée l'environnement virtuel
python -m venv venv
source venv/Scripts/activate  # Windows

# Installe les dépendances
pip install -r requirements.txt

# Lance le dashboard
cd dashboard
streamlit run app.py
```

---

## 👤 Auteur

**Elom Brasco** — Ingénieur Géophysicien | Data enthousiast

Formation : CentraleSupélec Openclassrooms · Université de Bordeaux · Google Data Analytics  


[https://www.linkedin.com/in/frejus-ibatta/](#) · [obesse017@gmail.com](#)