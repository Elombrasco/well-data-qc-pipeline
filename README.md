# 🛢️ Well Data Quality Control Pipeline
> **Portfolio project** 

## 🚀 Live Dashboard
👉 **[Voir le dashboard en ligne](https://volve-well-qc.streamlit.app)**

---

## 🎯 Business Problem

x enterprise opère des milliers de puits à travers le monde. Les données de diagraphies collectées proviennent de sources hétérogènes — prestataires, équipes terrain, bases historiques. Des données mal qualifiées entraînent :

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

well-data-qc-pipeline/
│
├── 📁 data/
|   |
│   ├── Volve production data.xlsx    ← dataset brut
|  |
│   ├── volve_production_clean.csv    ← données nettoyées
|  |
│   └── volve_wells.db                ← base SQLite
│
|
├── 📁 notebooks/
|   |
│   └── 01_EDA.ipynb                  ← exploration + nettoyage
│
|
├── 📁 src/
|   |
│   ├── qc_engine.py                  ← moteur QC automatisé
|   |
│   ├── db_loader.py                  ← chargement SQLite
|   |
│   └── pdf_report.py                 ← rapport PDF automatisé
|
│
├── 📁 dashboard/
|   |
│   └── app.py                        ← dashboard Streamlit
│
|
├── 📁 reports/
|   |
│   └── qc_rapport_volve.pdf          ← rapport QC généré
|
│
└── requirements.txt

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