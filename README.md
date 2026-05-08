# well-data-qc-pipeline
Automated QC pipeline for well log data (LAS)


# 🛢️ Well Data Quality Control Pipeline

## 🎯 Business Problem

TotalEnergies operates thousands of wells worldwide. Well log data (LAS format) comes from heterogeneous sources — contractors, field teams, and historical databases. Poor quality or inconsistent data leads to :

- Costly **geological misinterpretations**
- **Delayed decisions** on exploration projects
- **Repetitive manual work** for geoscientists

> **Business Impact :** Reduce manual well data validation time by ~70% through an automated Quality Control pipeline.

---

## 🔗 Direct link to the target 

 What this project demonstrates |
|---|---|
| Data inventory & collection | ✅ PREPARE phase |
| Harmonization & standardization | ✅ PROCESS phase |
| Automated quality control | ✅ ANALYZE phase |
| Reporting to geoscience teams | ✅ SHARE phase |
| Workflow automation | ✅ Pipeline architecture |

---

## 🔄 Methodology — Google Data Analytics Framework

### ❓ ASK
Key business questions this project answers :
- Which wells have immediately usable data ?
- Which log curves are missing or corrupted ?
- Are naming conventions consistent across wells ?
- Are there physical inconsistencies in the measurements ?
- What is the overall quality score of the well portfolio ?

**Success KPIs :**
- Anomaly detection rate > 95%
- Processing time < 5 seconds per well
- Operational dashboard usable without Python knowledge

---

### 📦 PREPARE
Dataset    : Volve Field Open Dataset — Equinor (2018)
Type       : LAS files (Log ASCII Standard)
Volume     : 22 wells | 15+ curves per well | depths 1500–4500m
Source     : North Sea, Norway — real production data
License    : Open data — Creative Commons

Key curves analyzed : GR · RHOB · NPHI · DT · CALI

---

### ⚙️ PROCESS
Pipeline steps :
1. Automatic parsing of all LAS files
2. Null value detection (-9999.25 = industry standard)
3. Physical range validation per curve
4. Curve name harmonization (e.g. GAMMA_RAY → GR)
5. Depth monotonicity check
6. Quality score calculation per well (0–100)
7. Storage in structured SQLite database

---

### 📊 ANALYZE
- Well ranking by quality score
- Most problematic curves identification
- Anomaly distribution by type
- Cross-well comparison on same formations
- Detection of wells requiring re-acquisition

---

### 📤 SHARE
| Deliverable | Description |
|---|---|
| Interactive Dashboard | Streamlit app — portfolio view + per-well detail |
| Automated QC Report | PDF per well — ready to send to geoscience teams |
| GitHub Repository | Documented code + professional README in English |

---

## 🛠️ Stack
`Python` · `lasio` · `pandas` · `plotly` · `streamlit` · `SQLite` · `SQLAlchemy`

---

## 👤 Author
Frejus IBATTA — Geophysical Engineer | Data Analyst  
https://www.linkedin.com/in/frejus-ibatta/ · obesse017@gmail.com
