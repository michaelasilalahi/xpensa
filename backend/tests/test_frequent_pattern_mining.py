import pandas as pd
import pytest
from app.modules.data_mining.analysis_calender.association_rule_learning.frequent_pattern_mining import frequent_pattern_mining


@pytest.fixture
def dummy_encoded_data():
    # Transaksi 1: Kopi, Rokok
    # Transaksi 2: Kopi, Nasi Goreng
    # Transaksi 3: Kopi, Rokok, Mie Ayam
    # Transaksi 4: Nasi Goreng, Rokok
    # Transaksi 5: Kopi, Rokok
    data = {
        'Tanggal': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'Kopi': [True, True, True, False, True],
        'Rokok': [True, False, True, True, True],
        'Nasi Goreng': [False, True, False, True, False],
        'Mie Ayam': [False, False, True, False, False]
    }
    return pd.DataFrame(data)

def test_fp_growth_logic_and_support(dummy_encoded_data):
    print("\n" + "="*65)
    print(" [TEST START] Menguji Modul: Frequent Pattern Mining (FP-Growth)")
    print("="*65)
    
    df_result = frequent_pattern_mining(dummy_encoded_data, min_support=0.2)
    
    assert not df_result.empty, "DataFrame hasil FP-Growth kosong!"
    print("-> [CHECK 1] DataFrame hasil FP-Growth berhasil digenerate.")

    assert 'Tanggal' not in df_result.columns
    print("-> [CHECK 2] Kolom 'Tanggal' berhasil diabaikan/dihapus dari proses mining.")
    
    # Cari baris yang berisi kombinasi {Kopi, Rokok}
    target_itemset = frozenset({'Kopi', 'Rokok'})
    kopi_rokok_row = df_result[df_result['itemsets'] == target_itemset]
    
    assert len(kopi_rokok_row) == 1, "Kombinasi Kopi dan Rokok tidak ditemukan!"
    print("-> [CHECK 3] Itemset kombinasi {Kopi, Rokok} ditemukan.")
    
    row_data = kopi_rokok_row.iloc[0]
    
    # Validasi Support = 3/5 = 0.60
    assert row_data['support'] == 0.60, f"Error: Support salah! Diharapkan 0.60, tapi dapat {row_data['support']}"
    print(f"-> [CHECK 4] Nilai Support Valid: {row_data['support']} (Diharapkan 0.60 atau 60%)")
    
    assert row_data['absolute_count'] == 3
    assert row_data['length'] == 2
    print(f"-> [CHECK 5] Absolute Count: {row_data['absolute_count']} transaksi, Length Itemset: {row_data['length']} item.")
    
    print("="*65)
    print(" [TEST PASSED] Modul FP-Growth Lolos Pengujian White Box!")
    print("="*65 + "\n")