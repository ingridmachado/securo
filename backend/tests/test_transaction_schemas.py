"""Regression tests for TransactionUpdate schema.

Ensures the Pydantic field-name/type-name collision for `date: Optional[date]`
does not resurface. See: Pydantic V2 metaclass resolves the `date` type annotation
to NoneType when the field name is also `date` and the type is Optional.
"""

from datetime import date
from decimal import Decimal

import pytest
from pydantic import ValidationError

from app.schemas.transaction import TransactionCreate, TransactionUpdate


class TestTransactionUpdateDateField:
    """Verify the `date` field on TransactionUpdate accepts valid date strings."""

    def test_accepts_iso_date_string(self):
        data = TransactionUpdate.model_validate({"date": "2026-02-25"})
        assert data.date == date(2026, 2, 25)

    def test_accepts_none(self):
        data = TransactionUpdate.model_validate({"date": None})
        assert data.date is None

    def test_unset_date_excluded(self):
        data = TransactionUpdate.model_validate({"description": "test"})
        dumped = data.model_dump(exclude_unset=True)
        assert "date" not in dumped

    def test_set_date_included(self):
        data = TransactionUpdate.model_validate({"date": "2026-03-15"})
        dumped = data.model_dump(exclude_unset=True)
        assert dumped["date"] == date(2026, 3, 15)

    def test_rejects_invalid_date_string(self):
        with pytest.raises(ValidationError):
            TransactionUpdate.model_validate({"date": "not-a-date"})


class TestTransactionUpdateAllFields:
    """Verify TransactionUpdate accepts all editable fields together."""

    def test_all_fields_accepted(self):
        data = TransactionUpdate.model_validate({
            "description": "Updated description",
            "amount": "250.00",
            "date": "2026-06-01",
            "type": "credit",
            "currency": "USD",
            "category_id": "11111111-1111-1111-1111-111111111111",
        })
        assert data.description == "Updated description"
        assert data.amount == Decimal("250.00")
        assert data.date == date(2026, 6, 1)
        assert data.type == "credit"
        assert data.currency == "USD"
        assert str(data.category_id) == "11111111-1111-1111-1111-111111111111"

    def test_partial_update_only_type(self):
        data = TransactionUpdate.model_validate({"type": "credit"})
        dumped = data.model_dump(exclude_unset=True)
        assert dumped == {"type": "credit"}

    def test_partial_update_amount_and_currency(self):
        data = TransactionUpdate.model_validate({"amount": "99.99", "currency": "EUR"})
        dumped = data.model_dump(exclude_unset=True)
        assert dumped == {"amount": Decimal("99.99"), "currency": "EUR"}


class TestTransactionCreateDateField:
    """Ensure TransactionCreate also handles the date field correctly."""

    def test_accepts_iso_date_string(self):
        data = TransactionCreate.model_validate({
            "description": "Test",
            "amount": "10.00",
            "date": "2026-02-25",
            "type": "debit",
            "account_id": "11111111-1111-1111-1111-111111111111",
        })
        assert data.date == date(2026, 2, 25)
