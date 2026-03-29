# TC-83 — Pytest Automation Suite: Successful Login with Valid Username and Password

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
