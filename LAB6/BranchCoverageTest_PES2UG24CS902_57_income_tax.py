import pytest

from income_tax import refund_status, tax_due, taxable_income


@pytest.mark.parametrize(
    ("gross", "regime", "investments", "expected"),
    [
        (1_000_000, "new", 0, 925_000),
        (1_000_000, "old", 100_000, 850_000),
        (1_000_000, "old", 200_000, 800_000),
        (20_000, "old", 0, 0),
    ],
)
def test_taxable_income_regime_and_deduction_branches(
    gross, regime, investments, expected
):
    """Cover both regimes, the investment cap, and taxable-income outcomes."""
    assert taxable_income(gross, regime, investments) == expected


@pytest.mark.parametrize(
    ("gross", "regime", "message"),
    [
        (-1, "new", "invalid income"),
        (1_000_000, "unsupported", "unknown regime"),
    ],
)
def test_taxable_income_error_branches(gross, regime, message):
    with pytest.raises(ValueError, match=message):
        taxable_income(gross, regime, 0)


@pytest.mark.parametrize(
    ("taxable", "age", "expected"),
    [
        (200_000, 30, 0),
        (500_000, 30, 12_500),
        (800_000, 30, 72_500),
        (800_000, 60, 62_500),
        (800_000, 80, 22_500),
    ],
)
def test_tax_due_age_exemption_and_slab_branches(taxable, age, expected):
    """Cover all age groups, exemption equality, and both tax slabs."""
    assert tax_due(taxable, age) == expected


def test_tax_due_error_branch():
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
def test_refund_status_difference_and_filing_branches(
    tax_paid, tax_due_amount, filed_on_time, expected
):
    """Cover positive, negative, and zero differences with both filing outcomes."""
    assert refund_status(tax_paid, tax_due_amount, filed_on_time) == expected
