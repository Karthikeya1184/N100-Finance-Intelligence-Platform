# N100 Finance Intelligence Platform

## Overview

The N100 Finance Intelligence Platform is a financial analytics solution developed during the Bluestock Fintech Internship. It processes financial datasets, stores them in SQLite, calculates key financial metrics, exposes them through a FastAPI backend, and generates professional PDF reports.

---

## Features

- ETL pipeline for financial datasets
- SQLite database
- Financial KPI engine
- FastAPI REST API
- Company PDF tearsheets
- Automated unit tests
- Data quality validation

---

## Tech Stack

- Python 3.12
- SQLite
- Pandas
- NumPy
- FastAPI
- ReportLab
- Pytest
- Black
- Ruff

---

## Installation

```bash
git clone <repository-url>

cd N100-Finance-Intelligence-Platform

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt
```

---

## Run ETL

```bash
python src/etl/database_loader.py
```

---

## Run FastAPI

```bash
uvicorn src.api.main:app --reload
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## Generate PDF Reports

```bash
python src/reports/tearsheet.py
```

Batch generation:

```bash
python src/reports/batch_tearsheet.py
```

---

## Run Tests

```bash
pytest tests/
```

---

## Code Quality

```bash
black src tests
```

```bash
ruff check src tests
```

---

## Project Structure

```
src/
tests/
docs/
db/
output/
reports/
```

---

## License

Educational / Internship Project