# TC-83 — Successful Login with Valid Username and Password

## Overview
Automated pytest suite for **TC-83** using Selenium WebDriver + Page Object Model (POM).

- **URL**: https://www.saucedemo.com/
- **Test Data**: `validdata.xlsx` → `standard_user / secret_sauce`
- **Linked Requirement**: SAUC-3
- **Priority**: High
- **Type**: End-to-End UI Automation (Selenium + Pytest)

---

## 📁 Project Structure

```
pytest_script/
├── pages/
│   ├── __init__.py
│   ├── base_page.py          # BasePage: reusable Selenium interactions
│   ├── login_page.py         # LoginPage POM
│   └── inventory_page.py     # InventoryPage POM
├── tests/
│   ├── __init__.py
│   ├── base_test.py          # BaseTest: setup/teardown, screenshot on fail
│   └── test_tc83_login.py    # TC-83 test cases (step-by-step + E2E)
├── utils/
│   ├── __init__.py
│   ├── config.py             # Configuration constants (BASE_URL, BROWSER, etc.)
│   ├── driver_factory.py     # WebDriver factory (Chrome / Firefox)
│   ├── logger.py             # Centralized logging (console + file)
│   └── wait_helper.py        # Explicit wait utilities
├── reports/
│   ├── pytest_script.html    # HTML test report (auto-generated)
│   └── screenshots/          # Auto-captured on test failures
├── conftest.py               # Pytest hooks & report directory setup
├── pytest.ini                # Pytest configuration
├── main.py                   # Entry point to run the test suite
└── requirements.txt          # Python dependencies
```

---

## ⚙️ Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables (optional overrides)
| Variable         | Default                        | Description                    |
|------------------|--------------------------------|--------------------------------|
| `BASE_URL`       | `https://www.saucedemo.com/`   | Application URL                |
| `BROWSER`        | `chrome`                       | Browser: `chrome` or `firefox` |
| `HEADLESS`       | `false`                        | Run headless: `true` or `false`|
| `IMPLICIT_WAIT`  | `10`                           | Implicit wait in seconds       |
| `EXPLICIT_WAIT`  | `15`                           | Explicit wait in seconds       |

---

## 🚀 Run Tests

### Option 1 — Using pytest directly
```bash
pytest tests/test_tc83_login.py -v --html=reports/pytest_script.html --self-contained-html
```

### Option 2 — Using the entry point
```bash
python main.py
```

### Option 3 — Headless mode (CI/CD)
```bash
HEADLESS=true pytest tests/test_tc83_login.py -v --html=reports/pytest_script.html --self-contained-html
```

---

## 🧪 Test Cases in `test_tc83_login.py`

| Test Method                                  | Description                                              |
|----------------------------------------------|----------------------------------------------------------|
| `test_step1_login_page_displayed`            | Verifies login page UI elements are visible              |
| `test_step2_enter_valid_username`            | Enters a valid username and confirms value               |
| `test_step3_enter_valid_password_and_verify_masking` | Enters password and verifies masking (type=password) |
| `test_step4_click_login_redirects_to_dashboard` | Full login + redirect to inventory dashboard          |
| `test_tc83_full_e2e_successful_login`        | Combined E2E test covering all 4 steps in one flow       |

---

## 📊 Reporting

- **HTML Report**: Auto-generated at `reports/pytest_script.html` after each run.
- **Log File**: Appended to `reports/test_run.log` for persistent logs.
- **Screenshots**: Captured automatically on test failure and saved to `reports/screenshots/`.

---

## ✅ TC-83 Execution Summary

| # | Step | Action | Expected Result | Status |
|---|------|---------|-----------------|--------|
| 1 | Navigate to login page | `GET https://www.saucedemo.com/` | Username, password fields + Login button visible | ✅ PASS |
| 2 | Enter valid username | Type `standard_user` in `#user-name` | Username entered successfully | ✅ PASS |
| 3 | Enter valid password | Type `secret_sauce` in `#password` | Password masked & entered | ✅ PASS |
| 4 | Click Login button | Click `#login-button` | Redirect to dashboard (`inventory.html`) | ✅ PASS |

---

## 📦 Test Data

| Source          | Username        | Password      | Row   |
|-----------------|-----------------|---------------|-------|
| `validdata.xlsx`| `standard_user` | `secret_sauce`| Row 1 |
