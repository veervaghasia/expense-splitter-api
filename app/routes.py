# The route layer should do very little:
# - accept request
# - validate request
# - call service
# - return response
# There should be no business logic here (like calculating splits, etc)

# APIRouter lets us group endpoints together
from fastapi import APIRouter

# Used to inject DB session automatically
from fastapi import Depends

# SQLModel session type
from sqlmodel import Session

# Database dependency
from app.db import get_session

# Pydantic schemas 
from app.schemas import ExpenseCreate
from app.schemas import BalanceResponse

# Business logic
from app.services import create_expense
from app.services import calculate_balances


# ------------------------------
# CREATE API ROUTER
# ------------------------------

# Can think of router as a mini FastAPI app
# It contains related endpoints
router = APIRouter()


# ------------------------------
# CREATE EXPENSE ENDPOINT
# ------------------------------

@router.post(
    "/expenses",
    status_code=201  # This tells FastAPI to return 201 Created status code
)
def add_expense(
    data: ExpenseCreate,
    session: Session = Depends(get_session)  # This injects a DB session
):
    """
    POST /expenses
    
    data:
        validated request body
    
    session: 
        DB session injected automatically
    """

    expense = create_expense(
        data=data,
        session=session
    )

    return {
        "message": "Expense created successfully",
        "expense_id": expense.id
    }


# ------------------------------
# GET BALANCES ENDPOINT
# ------------------------------
@router.get(
    "/balances/{group_id}",
    response_model=BalanceResponse  # This tells FastAPI to validate and serialize response using BalanceResponse schema
)
def get_balances(
    group_id: int,
    session: Session = Depends(get_session)
):
    """
    GET /balances/1
    
    group_id:
        extracted from URL
    """

    balances = calculate_balances(
        group_id=group_id,
        session=session
    )

    return BalanceResponse(
        balances=balances
    )