# This file defines the database tables' structure for our expense sharing app.

# SQLModel is built on top of SQLAlchemy + Pydantic
# It lets us define database tables using Python classes

from sqlmodel import SQLModel, Field


# -----------------------------
# USER TABLE
# -----------------------------
class User(SQLModel, table=True):
    """
    This class represents a table in the database.
    Each attribute is a column in the table. 
    This table represents a user. 
    """

    # default = None, means DB will auto-generate it
    id: int | None = Field(default=None, primary_key=True)
    name: str


# -----------------------------
# GROUP TABLE
# -----------------------------
class Group(SQLModel, table=True):
    """
    Table to represent a group.
    (e.g., roommates sharing expenses)
    """

    id: int | None = Field(default=None, primary_key=True)
    name: str


# -----------------------------
# EXPENSE TABLE
# -----------------------------
class Expense(SQLModel, table=True):
    """
    Table to represent one expense entry.
    """

    id: int | None = Field(default=None, primary_key=True)

    # Total amount of the expense
    amount: float  

    # User id of the person who paid
    # this means it references User table
    paid_by: int = Field(foreign_key="user.id")

    # Group id of the group to which this expense belongs
    # this means it references Group table
    group_id: int = Field(foreign_key="group.id")

    split_type: str


# -----------------------------
# EXPENSE SPLIT TABLE
# -----------------------------
class ExpenseSplit(SQLModel, table=True):
    """
    This says how much does each user owes for a given expense.
    So, one expense can have multiple rows in this table.
    """

    id: int | None = Field(default=None, primary_key=True)
    expense_id: int = Field(foreign_key="expense.id")
    user_id: int
    amount_owed: float