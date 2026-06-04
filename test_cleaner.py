import pandas as pd
from cleaner import snake, clean


def test_snake():
    assert snake(" First Name ") == "first_name"
    assert snake("LastName") == "last_name"


def test_clean_dedupes_and_types():
    df = pd.read_csv("sample_messy.csv")
    out = clean(df)
    # one exact-duplicate Alice row removed, one all-empty row removed
    assert len(out) == 3
    assert "first_name" in out.columns
    assert str(out["spend"].dtype).startswith(("float", "int"))
