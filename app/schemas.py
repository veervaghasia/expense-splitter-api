# This file will store API contracts and its validation.

# BaseModel comes from Pydantic
# It is used for validating API input/output
from pydantic import BaseModel, field_validator
from typing import List, Literal


# -----------------------------
# USER CREATE SCHEMA
# -----------------------------
class UserCreate(BaseModel):
    """
    This defines what data is required when creating a user via API.
    """
    name: str


# -----------------------------
# GROUP CREATE SCHEMA
# -----------------------------
class GroupCreate(BaseModel):
    """
    This defines what data is required when creating a group via API.
    """
    name: str


# -----------------------------
# SPLIT INPUT STRUCTURE
# -----------------------------
class SplitInput(BaseModel):
    """
    This represents how a single user's share is defined.
    Used inside ExpenseCreate.
    """
    user_id: int

    # Used for:
    # - exact split -> amount
    # - percentage split -> percentage value
    value: float


# -----------------------------
# EXPENSE CREATE SCHEMA
# -----------------------------
class ExpenseCreate(BaseModel):
    """
    This represents input schema for creating an expense.
    """
    amount: float
    paid_by: int 
    group_id: int

    # Literal restricts values to only these options
    split_type: Literal["equal", "exact", "percentage"]
    
    # List of splits (used for exact / percentage splits)
    splits: List[SplitInput] | None = None


    # -----------------------------
    # VALIDATION: amount > 0
    # -----------------------------
    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, value):
        """
        Runs automatically whenever amount is provided.
        """
        if value <= 0:
            raise ValueError("Amount must be greater than 0")
        return value
    

    # -----------------------------
    # VALIDATION: split rules
    # -----------------------------
    @field_validator("split_type")
    @classmethod
    def validate_split_type(cls, value):

        allowed = {
            "equal",
            "exact",
            "percentage"
        }

        if value not in allowed:
            raise ValueError(
                f"split_type must be one of {allowed}"
            )

        return value


    @field_validator("splits")
    @classmethod
    def validate_splits_exist(cls, value):

        if len(value) == 0:
            raise ValueError(
                "At least one split is required"
            )

        return value
    

# -----------------------------
# RESPONSE SCHEMA (BALANCES)
# -----------------------------
class BalanceResponse(BaseModel):
    """
    Response format for balance API.
    """

    balances: dict[int, float]