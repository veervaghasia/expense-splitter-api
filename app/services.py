# Contians our core logic for our application.

# Import Database models (tables)
from app.models import Expense, ExpenseSplit

# Import schema (input validation structure)
from app.schemas import ExpenseCreate

# Import session type
from sqlmodel import Session, select

# Instead of a stack trace, can return a clean error message with HTTP status code
from fastapi import HTTPException



# ------------------------------
# SPLIT CALCULATION LOGIC FOR A GIVEN EXPENSE
# ------------------------------

def calculate_splits(data: ExpenseCreate):
    """
    This function calculates how much each user owes.

    Input: ExpenseCreate (validated input data for creating an expense)
    Output: list of dictionaries:
    [
        {
            "user_id": 1,
            "amount": 10.0
        },
        {
            "user_id": 2,
            "amount": 20.0
        }
    ]
    """

    # We will store our final result in this list
    splits_results = []

    amount = data.amount
    split_type = data.split_type

    # -------------------------
    # EQUAL SPLIT
    # -------------------------
    if split_type == "equal":

        # extract user ids from splits (we assume user list is passed)
        users = [s.user_id for s in data.splits]

        n = len(users)

        # divide total amount equally
        share = amount / n

        for user_id in users:
            splits_results.append({
                "user_id": user_id,
                "amount": share
            })

    # -------------------------
    # EQUAL SPLIT
    # -------------------------
    elif split_type == "exact":

        total = sum(split.value for split in data.splits)
        if total - amount > 0.01:  # Allow small floating point errors
            raise HTTPException(
                status_code=400,
                detail="Total of splits must equal total expense amount"
            )
            
            

        # values are already given as exact numbers
        for s in data.splits:
            splits_results.append({
                "user_id": s.user_id,
                "amount": s.value
            })

    # -------------------------
    # PERCENTAGE SPLIT
    # -------------------------
    elif split_type == "percentage":

        total_percentage = sum(split.value for split in data.splits)
        if 100 - total_percentage > 0.01:  # Allow small floating point errors
            raise HTTPException(
                status_code=400,
                detail="Percentages must add up to 100"
            )

        for s in data.splits:

            # Convert percentage -> actual amount
            user_amount = (s.value / 100) * amount

            splits_results.append({
                "user_id": s.user_id,
                "amount": user_amount
            })

    return splits_results


# ------------------------------
# CREATE EXPENSE + STORE IN DB
# ------------------------------

def create_expense(data: ExpenseCreate, session: Session):
    """
    This function:
    - creates expense row
    - calculates splits
    - stores ExpenseSplit in rows
    """

    # -------------------------
    # CREATE EXPENSE
    # -------------------------

    expense = Expense(
        amount=data.amount,
        paid_by=data.paid_by,
        group_id=data.group_id,
        split_type=data.split_type
    )

    # Add to Database
    session.add(expense)

    # Save changes
    session.commit()

    # Refresh to get auto-generated ID
    session.refresh(expense)

    # -------------------------
    # CALCULATE SPLITS
    # --------------
    
    splits = calculate_splits(data)

    # -------------------------
    # STORE SPLITS
    # -------------------------

    for s in splits:
        split_row = ExpenseSplit(
            expense_id=expense.id,
            user_id=s["user_id"],
            amount_owed=s["amount"] 
        )

        session.add(split_row)
    
    # Save all split rows
    session.commit()

    return expense 


# ------------------------------
# Calculate Balances
# ------------------------------

def calculate_balances(group_id: int, session:Session):
    """
    For a given group:
    - calculate how much each user paid
    - calculate how much each user owes
    - return net balance
    """

    balances = {} # user_id -> net balance

    # -------------------------
    # GET ALL EXPENSES
    # -------------------------

    statement = select(Expense).where(Expense.group_id == group_id)
    expenses = session.exec(statement).all()

    if not expenses:
        raise HTTPException(
            status_code=404, 
            detail="Group not found or no expenses in group"
        )

    # -------------------------
    # PROCESS PAYMENTS
    # -------------------------

    for exp in expenses: 
        paid_by = exp.paid_by
        amount = exp.amount

        # Initialize if not present
        if paid_by not in balances:
            balances[paid_by] = 0

        balances[paid_by] += amount
    
    # -------------------------
    # GET ALL SPLITS
    # -------------------------

    statement = select(ExpenseSplit).where(
        ExpenseSplit.expense_id.in_([exp.id for exp in expenses])
    )

    splits = session.exec(statement).all()

    # -------------------------
    # PROCESS OWED AMOUNTS
    # -------------------------

    for s in splits:
        user_id = s.user_id
        amount = s.amount_owed

        if user_id not in balances:
            balances[user_id] = 0

        balances[user_id] -= amount

    return balances