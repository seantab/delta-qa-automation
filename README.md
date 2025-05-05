# ✈️ Delta Airlines QA Automation Challenge

## Overview
This project demonstrates the QA automation of Delta.com’s “Book a Flight” feature as part of the Delta Airlines QA Automation Challenge. It includes manual test design, detailed test scripts, and automated test execution using Playwright (Python).

---

## Deliverables

| Component               | Description                                           |
|------------------------|-------------------------------------------------------|
| ✔️ Test Scenarios       | 21 scenarios covering core, edge, and alternate flows |
| ✔️ Manual Test Scripts  | TS1 (Happy Path), TS6 (Negative Input Validation)     |
| ✔️ Automation (TS6)     | CSV-driven Playwright test with error validation      |
| ✔️ HTML Report          | Auto-generated via Pytest                            |
| ✔️ Documentation        | This README                                           |

---

## How to Run the Automation
### Setup
Install dependencies:
pip install -r requirements.txt

## How to Run the test with HTML report:
pytest tests/test_missing_destination.py --html=report.html


### 📁 Folder Structure

delta-flight-qa-automation/

├── pages/

→→→→└── booking_page.py

├── tests/

→→→→└── test_missing_destination.py

├── testdata/

→→→→└── testdata.csv

├── pytest.ini

├── requirements.txt

└── README.md

