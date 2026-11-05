import pytest

from income_tax import refund_status, tax_due, taxable_income


@pytest.mark.parametrize(
    ("gross", "regime", "investments", "expected"),
    [
        (1_000_000, "new", 0, 925_000),
        (100_000, "new", 0, 25_000),
        (1_000_000, "old", 100_000, 850_000),
        (1_000_000, "old", 200_000, 800_000),
        (20_000, "old", 0, 0),
    ],
)
def test_taxable_income_valid_regimes_and_boundaries(
    gross, regime, investments, expected
):
    assert taxable_income(gross, regime, investments) == expected



def test_taxable_income_rejects_negative_income():
    with pytest.raises(ValueError, match="invalid income"):
        taxable_income(-1, "new", 0)


def test_taxable_income_rejects_unknown_regime():
    with pytest.raises(ValueError, match="unknown regime"):
        taxable_income(1_000_000, "middle", 0)


@pytest.mark.parametrize(
    ("taxable", "age", "expected"),
    [
        (200_000, 30, 0),
        (250_000, 30, 0),
        (500_000, 30, 12_500),
        (500_001, 30, 12_500),
        (800_000, 60, 62_500),
        (800_000, 80, 22_500),
    ],
)
def test_tax_due_exemptions_and_tax_slabs(taxable, age, expected):
    assert tax_due(taxable, age) == expected


def test_tax_due_rejects_negative_taxable_amount():
    with pytest.raises(ValueError, match="invalid amount"):
        tax_due(-1, 30)


@pytest.mark.parametrize(
    ("tax_paid", "tax_due_amount", "filed_on_time", "expected"),
    [
        (10_000, 9_000, True, "refund"),
        (10_000, 9_000, False, "refund delayed"),
        (9_000, 10_000, True, "pay balance"),
        (9_000, 10_000, False, "pay balance with penalty"),
        (10_000, 10_000, True, "settled"),
    ],
)
def test_refund_statuses(tax_paid, tax_due_amount, filed_on_time, expected):
    assert refund_status(tax_paid, tax_due_amount, filed_on_time) == expected
