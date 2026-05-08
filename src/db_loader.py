import os
import sqlite3
import pandas as pd
from qc_engine import run_qc

# ============================================
# DATABASE LOADER — Stockage SQLite
# ============================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'volve_wells.db')
CSV_PATH = os.path.join(BASE_DIR, 'data', 'volve_production_clean.csv')

def create_database():
    """Crée la base de données et les tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table 1 — Données de production
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS well_production (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            dateprd         TEXT,
            well_name       TEXT,
            on_stream_hrs   REAL,
            bore_oil_vol    REAL,
            bore_gas_vol    REAL,
            bore_wat_vol    REAL,
            water_cut       REAL,
            avg_downhole_pressure REAL,
            avg_downhole_temperature REAL,
            avg_whp_p       REAL,
            avg_wht_p       REAL,
            flow_kind       TEXT,
            well_type       TEXT
        )
    """)

    # Table 2 — Rapports QC
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qc_reports (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            well_name       TEXT,
            score           INTEGER,
            status          TEXT,
            total_issues    INTEGER,
            high_issues     INTEGER,
            medium_issues   INTEGER,
            records         INTEGER,
            period_start    TEXT,
            period_end      TEXT,
            run_date        TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Base de données créée")

def load_production_data():
    """Charge les données de production dans SQLite."""
    df = pd.read_csv(CSV_PATH, parse_dates=['DATEPRD'])
    df['WATER_CUT'] = (
        df['BORE_WAT_VOL'] /
        (df['BORE_OIL_VOL'] + df['BORE_WAT_VOL'])
    ) * 100

    df_to_load = df[[
        'DATEPRD', 'NPD_WELL_BORE_NAME', 'ON_STREAM_HRS',
        'BORE_OIL_VOL', 'BORE_GAS_VOL', 'BORE_WAT_VOL',
        'WATER_CUT', 'AVG_DOWNHOLE_PRESSURE',
        'AVG_DOWNHOLE_TEMPERATURE', 'AVG_WHP_P',
        'AVG_WHT_P', 'FLOW_KIND', 'WELL_TYPE'
    ]].copy()

    df_to_load.columns = [
        'dateprd', 'well_name', 'on_stream_hrs',
        'bore_oil_vol', 'bore_gas_vol', 'bore_wat_vol',
        'water_cut', 'avg_downhole_pressure',
        'avg_downhole_temperature', 'avg_whp_p',
        'avg_wht_p', 'flow_kind', 'well_type'
    ]

    df_to_load['dateprd'] = df_to_load['dateprd'].astype(str)

    conn = sqlite3.connect(DB_PATH)
    df_to_load.to_sql('well_production', conn,
                      if_exists='replace', index=False)
    conn.close()
    print(f"{len(df_to_load)} enregistrements chargés dans well_production")

def load_qc_report():
    """Exécute le QC et stocke les résultats dans SQLite."""
    df = pd.read_csv(CSV_PATH, parse_dates=['DATEPRD'])
    df['WATER_CUT'] = (
        df['BORE_WAT_VOL'] /
        (df['BORE_OIL_VOL'] + df['BORE_WAT_VOL'])
    ) * 100

    report = run_qc(df)

    report_to_load = report[[
        'well', 'score', 'status', 'total_issues',
        'high_issues', 'medium_issues', 'records',
        'period_start', 'period_end', 'run_date'
    ]].copy()

    report_to_load.columns = [
        'well_name', 'score', 'status', 'total_issues',
        'high_issues', 'medium_issues', 'records',
        'period_start', 'period_end', 'run_date'
    ]

    conn = sqlite3.connect(DB_PATH)
    report_to_load.to_sql('qc_reports', conn,
                          if_exists='replace', index=False)
    conn.close()
    print(f"Rapport QC chargé pour {len(report_to_load)} puits")

def query_database(sql):
    """Requête SQL sur la base."""
    conn = sqlite3.connect(DB_PATH)
    result = pd.read_sql(sql, conn)
    conn.close()
    return result

if __name__ == "__main__":
    # 1. Créer la base
    create_database()

    # 2. Charger les données
    load_production_data()

    # 3. Charger le rapport QC
    load_qc_report()

    # 4. Exemples de requêtes SQL
    print("\n=== REQUÊTES SQL ===\n")

    print("Top producteurs :")
    print(query_database("""
        SELECT well_name,
               ROUND(SUM(bore_oil_vol)/1000000, 2) as total_oil_Msm3
        FROM well_production
        GROUP BY well_name
        ORDER BY total_oil_Msm3 DESC
    """))

    print("\nScores QC par puits :")
    print(query_database("""
        SELECT well_name, score, status, high_issues
        FROM qc_reports
        ORDER BY score ASC
    """))