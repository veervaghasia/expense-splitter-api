from app.schemas import ExpenseCreate
from app.schemas import SplitInput

from app.services import calculate_splits

import pytest

from fastapi import HTTPException


# --------------------------------------------------
# TEST 1
# Equal split
# --------------------------------------------------

def test_equal_split():

    data = ExpenseCreate(
        amount=1000,
        paid_by=1,
        group_id=1,
        split_type="equal",
        splits=[
            SplitInput(user_id=1, value=0),
            SplitInput(user_id=2, value=0)
        ]
    )

    result = calculate_splits(data)

    assert result[0]["amount"] == 500
    assert result[1]["amount"] == 500


# --------------------------------------------------
# TEST 2
# Exact split
# --------------------------------------------------

def test_exact_split():

    data = ExpenseCreate(
        amount=1000,
        paid_by=1,
        group_id=1,
        split_type="exact",
        splits=[
            SplitInput(user_id=1, value=300),
            SplitInput(user_id=2, value=700)
        ]
    )

    result = calculate_splits(data)

    assert result[0]["amount"] == 300
    assert result[1]["amount"] == 700


# --------------------------------------------------
# TEST 3
# Percentage split
# --------------------------------------------------

def test_percentage_split():

    data = ExpenseCreate(
        amount=1000,
        paid_by=1,
        group_id=1,
        split_type="percentage",
        splits=[
            SplitInput(user_id=1, value=25),
            SplitInput(user_id=2, value=75)
        ]
    )

    result = calculate_splits(data)

    assert result[0]["amount"] == 250
    assert result[1]["amount"] == 750


# --------------------------------------------------
# TEST 4
# Invalid percentage
# --------------------------------------------------

def test_invalid_percentage():

    data = ExpenseCreate(
        amount=1000,
        paid_by=1,
        group_id=1,
        split_type="percentage",
        splits=[
            SplitInput(user_id=1, value=40),
            SplitInput(user_id=2, value=40)
        ]
    )

    with pytest.raises(HTTPException):

        calculate_splits(data)


# --------------------------------------------------
# TEST 5
# Negative Amount
# --------------------------------------------------

def test_negative_amount():

    with pytest.raises(ValueError):

        ExpenseCreate(
            amount=-100,
            paid_by=1,
            group_id=1,
            split_type="equal",
            splits=[
                SplitInput(user_id=1, value=0)
            ]
        )