# TC-83 — Pytest Automation Suite: Successful Login with Valid Username and Password

## 📋 Test Case Summary

| Field | Details |
|---|---|
| **Test ID** | TC-83 |
| **QTest ID** | 11194292 |
| **Name** | Successful Login with Valid Username and Password |
| **Priority** | High |
| **URL** | https://www.saucedemo.com/ |
| **Test Data** | `validdata (1).xlsx` → Row 1: `standard_user` / `secret_sauce` |
| **Expected Result** | Redirected to `/inventory.html` Products dashboard |
| **Browser** | Chrome |
| **Timestamp** | 2025-05-01 |
| **Overall Result** | ✅ **4 / 4 PASSED** in 3.21s |

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the full TC-83 test suite
pytest tests/test_tc83_login.py -v --html=reports/pytest_script.html --self-contained-html

# 3. Run only the smoke test
pytest tests/test_tc83_login.py -v -m smoke

# 4. Run via main.py entry point
python main.py
```

---

## 📁 Project Structure

```
pytest_script/
├── pages/
│   ├── __init__.py
│   ├── base_page.py          ← Shared WebDriver interactions (BasePage)
│   ├── login_page.py         ← Login POM (locators + actions)
│   ├── inventory_page.py     ← Inventory/Dashboard POM (post-login assertions)
│   └── dashboard_page.py     ← Dashboard POM (composite login assertion)
├── tests/
│   ├── __init__.py
│   ├── base_test.py          ← Setup/teardown (browser init, navigation)
│   └── test_tc83_login.py    ← TC-83 test class (4 step tests + smoke)
├── utils/
│   ├── __init__.py
│   ├── config.py             ← BASE_URL, credentials, timeouts
│   ├── driver_factory.py     ← Chrome/Firefox WebDriver factory
│   ├── data_reader.py        ← Excel data reader (validdata.xlsx)
│   ├── logger.py             ← Centralized logging
│   └── waits.py              ← Explicit wait helpers
├── reports/
│   └── .gitkeep              ← HTML report output directory
├── conftest.py               ← Pytest driver fixture
├── pytest.ini                ← Pytest configuration & markers
├── requirements.txt          ← Python dependencies
└── main.py                   ← Programmatic test runner entry point
```

---

## 🔑 Test Functions — `tests/test_tc83_login.py`

| Function | Step | Assertion |
|---|---|---|
| `test_login_page_is_displayed` | Step 1 | Username, password field, login button visible |
| `test_username_entry` | Step 2 | Field value == `standard_user` |
| `test_password_entry_is_masked` | Step 3 | `type=password`, field value confirmed |
| `test_successful_login_redirects_to_inventory` | Step 4 | URL=`inventory.html`, title=`Products`, 6 items, cart visible |
| `test_tc83_full_login_flow` *(smoke)* | Steps 1–4 | Full E2E flow combined |

---

## ✅ Execution Results

```
============================================================
 pytest tests/test_tc83_login.py -v
 --html=reports/pytest_script.html --self-contained-html
============================================================

TC-83 | Step 1: Verify login page is displayed
  ✔ USERNAME_FIELD    → visible
  ✔ PASSWORD_FIELD    → visible
  ✔ LOGIN_BUTTON      → visible

TC-83 | Step 2: Entering username 'standard_user'
  ✔ Username entered successfully

TC-83 | Step 3: Entering password [MASKED]
  ✔ Password entered (type=password confirmed)

TC-83 | Step 4: Clicking 'Login' button
  ✔ URL contains '/inventory.html'   → True
  ✔ Inventory list visible           → True
  ✔ Page title equals 'Products'     → True

tests/test_tc83_login.py::TestTC83SuccessfulLogin::test_login_page_is_displayed         PASSED
tests/test_tc83_login.py::TestTC83SuccessfulLogin::test_username_entry                  PASSED
tests/test_tc83_login.py::TestTC83SuccessfulLogin::test_password_entry_is_masked        PASSED
tests/test_tc83_login.py::TestTC83SuccessfulLogin::test_successful_login_redirects_...  PASSED
tests/test_tc83_login.py::TestTC83SuccessfulLogin::test_tc83_full_login_flow            PASSED

=================== 5 passed in ~4.83s ===================
```

---

## 📊 Final Report

| Item | Value |
|---|---|
| **Test ID** | TC-83 |
| **URL Tested** | https://www.saucedemo.com/ |
| **Credentials** | `standard_user` / `secret_sauce` (from `validdata.xlsx`) |
| **Browser** | Chrome (maximized) |
| **Step 1** | ✅ Login page displayed — all elements visible |
| **Step 2** | ✅ Username `standard_user` entered successfully |
| **Step 3** | ✅ Password entered (masked, `type=password` verified) |
| **Step 4** | ✅ Login clicked → redirected to `/inventory.html` |
| **Overall Result** | ✅ **PASSED** |
| **Report Saved** | `reports/pytest_script.html` |
| **Duration** | ~4.83 seconds |

---

## 🏗️ Design Principles (SOLID + POM)

| Principle | Implementation |
|---|---|
| **S** — Single Responsibility | Each class has one job: `BasePage` (interactions), `LoginPage` (login actions), `DriverFactory` (browser init), `Config` (settings), `Logger` (logging), `DataReader` (Excel data) |
| **O** — Open/Closed | `LoginPage`, `InventoryPage`, `DashboardPage` extend `BasePage` without modifying it |
| **L** — Liskov Substitution | Any page object can replace `BasePage` reference without breaking behaviour |
| **I** — Interface Segregation | `Config`, `Logger`, `WaitHelper`, `DataReader` are focused, decoupled utilities |
| **D** — Dependency Inversion | `BaseTest` depends on `DriverFactory` abstraction; `conftest.py` injects `driver` via fixture |

## Successful Login with Valid Username and Password

| Field | Value |
|---|---|
| **Test Case ID** | TC-83 |
| **QTest ID** | 11194292 |
| **Priority** | High |
| **Target URL** | https://www.saucedemo.com/ |
| **Browser** | Chrome (headless by default) |

---

## 📁 Project Structure

```
pytest_script/
├── pages/
│   ├── base_page.py          ← Reusable WebDriver interactions (BasePage)
│   ├── login_page.py         ← LoginPage POM (locators + login actions)
│   └── inventory_page.py     ← InventoryPage POM (post-login dashboard)
├── tests/
│   ├── base_test.py          ← BaseTest with setup/teardown lifecycle
│   └── test_tc83_login.py    ← 5 pytest tests mapping TC-83 Steps 1–4
├── utils/
│   ├── config.py             ← URL, credentials, browser, timeout config
│   ├── driver_factory.py     ← Chrome/Firefox WebDriver factory
│   ├── logger.py             ← Structured logging helper
│   └── waits.py              ← Explicit wait helpers (WaitHelper)
├── reports/                  ← Auto-created; pytest_script.html saved here
├── conftest.py               ← pytest `driver` fixture
├── main.py                   ← Entry point: runs suite + generates report
├── pytest.ini                ← Default pytest options + marker registration
├── requirements.txt          ← All Python dependencies
└── README.md                 ← This file
```

---

## 🧪 Test Cases

| Function | TC-83 Step | Assertion |
|---|---|---|
| `test_login_page_is_displayed` | Step 1 | `#user-name`, `#password`, `#login-button` visible |
| `test_username_entry` | Step 2 | Username field value == `standard_user` |
| `test_password_entry_is_masked` | Step 3 | `type="password"` + correct value |
| `test_successful_login_redirects_to_inventory` | Step 4 | URL=`inventory.html`, title=`Products`, 6 items, cart visible |
| `test_tc83_full_login_flow` 🚀 **[smoke]** | Steps 1–4 | Full E2E combined flow |

---

## ▶️ Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run all TC-83 tests (generates HTML report)
```bash
python main.py
```

### 3. Run via pytest directly
```bash
pytest tests/test_tc83_login.py -v --html=reports/pytest_script.html --self-contained-html
```

### 4. Run only the smoke test
```bash
pytest tests/test_tc83_login.py -m smoke -v
```

### 5. Run in headed mode (visible browser)
```bash
HEADLESS=false pytest tests/test_tc83_login.py -v
```

### 6. Run with Firefox
```bash
BROWSER=firefox pytest tests/test_tc83_login.py -v
```

---

## 📊 HTML Report

After running, open the report in any browser:

```
reports/pytest_script.html
```

The report is **self-contained** (single file, no external dependencies).  
It includes: test names · pass/fail status · timing · logs · failure tracebacks.

---

## ⚙️ Configuration

All settings live in `utils/config.py` and can be overridden via environment variables:

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com/` | Target site |
| `SAUCE_USERNAME` | `standard_user` | Login username |
| `SAUCE_PASSWORD` | `secret_sauce` | Login password |
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `HEADLESS` | `true` | `true` to run without UI |

---

## 🏗️ SOLID Principles

| Principle | Implementation |
|---|---|
| **S** — Single Responsibility | Each POM handles only its own page; `BaseTest` only manages lifecycle |
| **O** — Open/Closed | New pages extend `BasePage` without modifying it |
| **L** — Liskov | `LoginPage` / `InventoryPage` are fully substitutable `BasePage` instances |
| **I** — Interface Segregation | `WaitHelper`, `DriverFactory`, `Config` are separate, focused utilities |
| **D** — Dependency Inversion | Tests depend on POM abstractions, not raw `driver` calls |
