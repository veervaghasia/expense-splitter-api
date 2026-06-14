# Expense Splitter API

## Project Overview

### What is this?

Expense Splitter API is a backend service built using FastAPI that helps groups track shared expenses and calculate balances between participants.

### Why was it built?

Managing shared expenses during trips, apartment sharing, outings, or group activities can quickly become difficult. People often lose track of who paid for what and how much each participant owes.

This project provides a simple backend system to:

* Record expenses
* Support multiple expense splitting methods
* Track participants in each expense
* Calculate outstanding balances for a group

The goal was to gain hands-on experience with backend development using FastAPI, Pydantic, SQLModel, SQLite, and automated testing while implementing a real-world use case.

---

## Key Concepts Demonstrated

* FastAPI
* REST APIs
* Pydantic Validation
* SQLModel ORM
* SQLite
* Dependency Injection
* Layered Architecture
* Unit Testing

---

## Features

### Create Expense

Create an expense by specifying:

* Total amount
* Group ID
* User who paid
* Split type
* Participants involved in the expense

### Equal Split

Automatically divides an expense equally among all specified participants.

### Exact Split

Allows specifying the exact amount owed by each participant.

### Percentage Split

Allows specifying what percentage of the expense each participant should pay. The system calculates the final amount automatically.

### Calculate Balances

Computes the net balance for each participant within a group based on all recorded expenses.

### Input Validation

Validation is performed using Pydantic and service-layer checks.

Examples:

* Expense amount must be greater than zero
* Exact split totals must equal the expense amount
* Percentage splits must add up to 100%
* Invalid request structures and types are rejected

### Automated Testing

Business logic is covered by automated tests using Pytest.

---

## Architecture

Request
 ↓
Pydantic Schema Validation
 ↓
Route Layer
 ↓
Service Layer
 ↓
Database Session
 ↓
SQLite Database
 ↓
Response Schema
 ↓
Response

The project follows a layered architecture where routes handle HTTP concerns, services contain business logic, and models manage database persistence. This separation improves maintainability, testability, and extensibility.

---

## Tech Stack

### FastAPI

Used to build REST APIs, define routes, handle dependency injection, and automatically generate Swagger/OpenAPI documentation.

### Pydantic

Used to define request and response schemas, validate incoming data, and enforce input constraints before data reaches the business logic layer.

### SQLModel

Provides ORM functionality by combining SQLAlchemy and Pydantic, allowing database tables to be defined as Python classes.

### SQLite

Lightweight relational database used for data persistence during development.

### Pytest

Used to automate testing of business logic and validation rules.

---

## Project Structure

```text
expense-splitter-api/
│
├── app/
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── services.py
│
├── tests/
│   └── test_services.py
│
├── .gitignore
├── database.db
├── README.md
└── requirements.txt
```

### app/db.py

Database engine, session management, and table creation.

### app/models.py

Database table definitions using SQLModel.

### app/schemas.py

Pydantic request and response schemas with validation logic.

### app/routes.py

API endpoint definitions and request handling.

### app/services.py

Business logic for expense splitting and balance calculations.

### tests/test_services.py

Automated tests for core business logic.

---

## API Endpoints

### POST /expenses

Creates a new expense and stores the corresponding split records.

### GET /balances/{group_id}

Returns the net balance for each participant in the specified group.

---

## Data Model

### Expense

| Field      | Description                |
| ---------- | -------------------------- |
| id         | Expense ID                 |
| amount     | Total expense amount       |
| paid_by    | User who paid              |
| group_id   | Associated group           |
| split_type | equal / exact / percentage |

### ExpenseSplit

| Field       | Description                |
| ----------- | -------------------------- |
| id          | Split ID                   |
| expense_id  | Linked expense             |
| user_id     | Participant                |
| amount_owed | Amount owed by participant |

Relationship:

```text
Expense (1)
    |
    └── ExpenseSplit (many)
```

---

## Setup Instructions

### Clone Repository

```bash
git clone <repo-url>
cd expense-splitter-api
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
uvicorn app.main:app --reload
```

Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Testing

Run all tests:

```bash
python -m pytest
```

Pytest automatically discovers functions whose names start with `test_`, executes them, and reports pass/fail status.

Current test coverage includes:

* Equal split calculations
* Exact split calculations
* Percentage split calculations
* Invalid percentage validation
* Negative amount validation

Example output:

```text
======================= 5 passed in 1.77s ========================
```

---

## Design Decisions

### Why separate Expense and ExpenseSplit?

An expense can involve multiple participants, creating a one-to-many relationship.

Separating expenses and splits follows database normalization principles, avoids duplicated information, and simplifies querying and future extensions.

### Why use a Service Layer?

Business logic is separated from API routes to improve maintainability and testability.

Routes handle HTTP concerns, while services implement expense-splitting and balance-calculation logic.

### Why validate using Pydantic?

Validation is performed as early as possible to prevent invalid data from reaching the business layer and to provide clear feedback to API consumers.

### Why calculate balances dynamically?

Balances are derived data that can always be computed from expenses and splits.

Storing balances separately would introduce synchronization and consistency challenges whenever expenses are created, modified, or deleted.

---

## Limitations and Future Improvements

The current implementation focuses on core expense-splitting functionality.

Potential future enhancements include:

* User management
* Group membership management
* Authentication and authorization
* Expense editing and deletion
* Expense settlement workflow
* User-to-user balance breakdowns
* PostgreSQL support
* Docker containerization
* API route integration tests
* CI/CD pipeline integration
* Caching and performance optimizations

```
```
