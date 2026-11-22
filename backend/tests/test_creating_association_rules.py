import pandas as pd
import pytest
from app.modules.data_mining.analysis_calender.association_rule_learning.creating_association_rules import creating_association_rules

@pytest.fixture
def dummy_freq_itemsets():
    # Support Kopi = 4/5 = 0.8
    # Support Rokok = 4/5 = 0.8
    # Support Kopi & Rokok = 3/5 = 0.6
    data = {
        'support': [0.8, 0.8, 0.6],
        'itemsets': [
            frozenset({'Kopi'}), 
            frozenset({'Rokok'}), 
            frozenset({'Kopi', 'Rokok'})
        ],
        'length': [1, 1, 2],
        'absolute_count': [4, 4, 3]
    }
    return pd.DataFrame(data)

def test_association_rules_confidence_and_redundancy(dummy_freq_itemsets):
    print("\n" + "="*65)
    print(" [TEST START] Menguji Modul: Creating Association Rules")
    print("="*65)
    
    df_rules = creating_association_rules(dummy_freq_itemsets, min_confidence=0.5)
    
    assert not df_rules.empty, "DataFrame rules kosong!"
    print("-> [CHECK 1] DataFrame Association Rules berhasil dibuat dan tidak kosong.")
    
    # Validasi PEMBERSIHAN REDUNDANSI
    assert len(df_rules) == 1, "Fungsi drop_duplicates bolak-balik gagal bekerja!"
    print("-> [CHECK 2] Redundansi aturan bolak-balik berhasil dibersihkan (Sisa 1 rule unik).")
    
    row_data = df_rules.iloc[0]
    
    # Validasi Confidence = 0.6 / 0.8 = 0.75
    assert row_data['confidence'] == pytest.approx(0.75, abs=1e-5), f"Error: Confidence salah! Diharapkan 0.75, tapi dapat {row_data['confidence']}"
    print(f"-> [CHECK 3] Nilai Confidence Valid: {row_data['confidence']} (Diharapkan ~0.75)")
    
    # Validasi manipulasi string pada Rule Name
    assert "{" in row_data['rule_name'] and "}" in row_data['rule_name']
    print(f"-> [CHECK 4] Format Rule Name Valid: {row_data['rule_name']}")
    
    # Validasi rename column
    assert 'antecedent_support' in df_rules.columns
    assert 'consequent_support' in df_rules.columns
    print("-> [CHECK 5] Kolom antecedent_support & consequent_support berhasil di-rename.")
    
    print("="*65)
    print(" [TEST PASSED] Modul Association Rules Lolos Pengujian White Box!")
    print("="*65 + "\n")