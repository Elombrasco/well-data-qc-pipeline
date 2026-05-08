import os
import pandas as pd
from datetime import datetime

# ============================================
# QC ENGINE — Règles de qualité automatisées
# ============================================

# Plages physiques acceptables par colonne
PHYSICAL_RANGES = {
    'AVG_DOWNHOLE_PRESSURE':     (0, 500),
    'AVG_DOWNHOLE_TEMPERATURE':  (0, 200),
    'AVG_ANNULUS_PRESS':         (0, 500),
    'AVG_WHP_P':                 (0, 300),
    'AVG_WHT_P':                 (0, 150),
    'BORE_OIL_VOL':              (0, 50000),
    'BORE_GAS_VOL':              (0, 5000000),
    'BORE_WAT_VOL':              (0, 50000),
    'ON_STREAM_HRS':             (0, 24),
    'WATER_CUT':                 (0, 100)
}

def run_qc(df):
    """
    Exécute toutes les règles QC sur le dataframe.
    Retourne un rapport détaillé par puits.
    """
    results = []

    for well in df['NPD_WELL_BORE_NAME'].unique():
        df_well = df[df['NPD_WELL_BORE_NAME'] == well].copy()
        issues = []
        score = 100

        # RÈGLE 1 — Valeurs manquantes
        null_pct = df_well.isnull().sum() / len(df_well) * 100
        for col, pct in null_pct.items():
            if pct > 10:
                issues.append({
                    'rule': 'Valeurs manquantes',
                    'column': col,
                    'detail': f'{pct:.1f}% de valeurs manquantes',
                    'severity': 'HIGH' if pct > 30 else 'MEDIUM'
                })
                score -= 5 if pct > 30 else 2

        # RÈGLE 2 — Plages physiques impossibles
        for col, (min_val, max_val) in PHYSICAL_RANGES.items():
            if col in df_well.columns:
                out = df_well[
                    (df_well[col] < min_val) |
                    (df_well[col] > max_val)
                ]
                if len(out) > 0:
                    issues.append({
                        'rule': 'Plage physique',
                        'column': col,
                        'detail': f'{len(out)} valeurs hors plage [{min_val}-{max_val}]',
                        'severity': 'HIGH'
                    })
                    score -= 10

        # RÈGLE 3 — Cohérence temporelle
        dates = df_well['DATEPRD'].sort_values()
        gaps = dates.diff().dt.days
        large_gaps = gaps[gaps > 30]
        if len(large_gaps) > 0:
            issues.append({
                'rule': 'Continuité temporelle',
                'column': 'DATEPRD',
                'detail': f'{len(large_gaps)} gaps > 30 jours détectés',
                'severity': 'MEDIUM'
            })
            score -= 5

        # RÈGLE 4 — Production négative impossible
        for col in ['BORE_OIL_VOL', 'BORE_GAS_VOL', 'BORE_WAT_VOL']:
            if col in df_well.columns:
                neg = df_well[df_well[col] < 0]
                if len(neg) > 0:
                    issues.append({
                        'rule': 'Valeurs négatives',
                        'column': col,
                        'detail': f'{len(neg)} valeurs négatives impossibles',
                        'severity': 'HIGH'
                    })
                    score -= 15

        # RÈGLE 5 — Water Cut > 100%
        if 'WATER_CUT' in df_well.columns:
            wc_issues = df_well[df_well['WATER_CUT'] > 100]
            if len(wc_issues) > 0:
                issues.append({
                    'rule': 'Water Cut impossible',
                    'column': 'WATER_CUT',
                    'detail': f'{len(wc_issues)} valeurs > 100%',
                    'severity': 'HIGH'
                })
                score -= 10

        # Score final entre 0 et 100
        score = max(0, score)

        results.append({
            'well':         well,
            'score':        score,
            'status':       '✅ PASS' if score >= 80 else '⚠️ WARNING' if score >= 60 else '❌ FAIL',
            'total_issues': len(issues),
            'high_issues':  sum(1 for i in issues if i['severity'] == 'HIGH'),
            'medium_issues':sum(1 for i in issues if i['severity'] == 'MEDIUM'),
            'issues':       issues,
            'records':      len(df_well),
            'period_start': df_well['DATEPRD'].min().strftime('%Y-%m-%d'),
            'period_end':   df_well['DATEPRD'].max().strftime('%Y-%m-%d'),
            'run_date':     datetime.now().strftime('%Y-%m-%d %H:%M')
        })

    return pd.DataFrame(results)


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    df = pd.read_csv(os.path.join(BASE_DIR, 'data', 'volve_production_clean.csv'),
                 parse_dates=['DATEPRD'])
    df['WATER_CUT'] = (
        df['BORE_WAT_VOL'] /
        (df['BORE_OIL_VOL'] + df['BORE_WAT_VOL'])
    ) * 100

    report = run_qc(df)

    print("\n=== RAPPORT QC — CHAMP VOLVE ===\n")
    for _, row in report.iterrows():
        print(f"{row['status']} {row['well']}")
        print(f"   Score     : {row['score']}/100")
        print(f"   Issues    : {row['total_issues']} ({row['high_issues']} HIGH, {row['medium_issues']} MEDIUM)")
        print(f"   Période   : {row['period_start']} → {row['period_end']}")
        print(f"   Records   : {row['records']}")
        print()