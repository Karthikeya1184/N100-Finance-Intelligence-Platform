from src.etl.loader import load_all_files


def test_load_all_files():
    datasets = load_all_files()

    assert "companies" in datasets
    assert len(datasets) == 12