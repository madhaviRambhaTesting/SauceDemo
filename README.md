# 🧪 TC-96 — Forgot Password Link is Visible on the Login Page

> **Repository:** `madhaviRambhaTesting/SauceDemo`  
> **Branch:** `qtestidscript`  
> **QTest ID:** `11194308`  
> **Priority:** 🔴 High  
> **URL Under Test:** [https://www.saucedemo.com/](https://www.saucedemo.com/)

---

## 📋 Test Case Summary

| Field | Value |
|---|---|
| **Test Case ID** | TC-96 |
| **QTest ID** | 11194308 |
| **Title** | Forgot Password Link is Visible on the Login Page |
| **Priority** | High 🔴 |
| **Status** | ❌ FAIL (expected — feature not implemented) |
| **Pass Rate** | 0% |
| **Duration** | ~2.34s |

---

## 🔴 Root Cause

> **`https://www.saucedemo.com/` does NOT implement a 'Forgot Password' feature.**  
> The login page DOM contains only:
> - `#user-name` — Username input
> - `#password` — Password input
> - `#login-button` — Login submit button
>
> No anchor tag, button, or any element related to password recovery exists anywhere  
> in the DOM (confirmed via exhaustive DOM inspection).

---

## 🏗️ Project Structure

```
project_root/
├── pages/
│   ├── __init__.py
│   ├── base_page.py          → BasePage — reusable Selenium interactions
│   └── login_page.py         → LoginPage(BasePage) — TC-96 locators & methods
├── tests/
│   ├── __init__.py
│   ├── base_test.py          → BaseTest — setup/teardown/screenshot on fail
│   └── test_tc96_forgot_password.py → TestForgotPasswordLink(BaseTest)
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py     → DriverFactory — Chrome/Firefox WebDriver init
│   ├── config.py             → BASE_URL, timeouts, paths, env overrides
│   └── logger.py             → TestLogger — console + rotating-file logging
├── reports/
│   ├── pytest_script.html    → HTML report (generated at runtime)
│   └── screenshots/
│       ├── .gitkeep
│       └── TC96_forgot_password_FAIL.png  → captured on test failure
├── logs/
│   └── test_execution.log    → full debug log (generated at runtime)
├── conftest.py               → fixtures: driver, login_page, auto_screenshot
├── pytest.ini                → test discovery, markers, HTML report config
├── requirements.txt          → all Python dependencies
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### 1. Clone & install dependencies

```bash
git clone https://github.com/madhaviRambhaTesting/SauceDemo.git
cd SauceDemo
git checkout qtestidscript

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run TC-96

```bash
# Default — Chrome headless, generates HTML report
pytest tests/test_tc96_forgot_password.py -v

# Specific test only
pytest tests/test_tc96_forgot_password.py::TestForgotPasswordLink::test_forgot_password_link_visible -v

# Firefox
pytest tests/test_tc96_forgot_password.py --browser=firefox -v

# Non-headless (visible browser window)
HEADLESS=false pytest tests/test_tc96_forgot_password.py -v

# All TC-96 markers
pytest -m tc96 -v
```

### 3. View the HTML report

```bash
open reports/pytest_script.html        # macOS
xdg-open reports/pytest_script.html   # Linux
start reports/pytest_script.html      # Windows
```

---

## 📊 Step-by-Step Results

| # | Step | POM Method | Expected | Actual | Status |
|---|------|-----------|----------|--------|--------|
| 1 | Navigate to login page | `LoginPage.is_loaded()` | Login page displayed | ✅ Title: *Swag Labs*, URL confirmed | ✅ PASS |
| 2 | Look for 'Forgot Password' link | `LoginPage.is_forgot_password_visible()` | Link clearly visible | ❌ No link found — DOM has 0 `<a>` tags | ❌ FAIL |
| 3 | Click 'Forgot Password' link | `LoginPage.click_forgot_password()` | Navigate to reset page | ⚠️ `NoSuchElementException` raised | ⚠️ SKIP |

---

## 🔢 Assertion

```python
assert login_page.is_forgot_password_visible() == True
# Expected : True
# Received : False
# Message  : 'Forgot Password' link should be visible on the login page
```

---

## 📸 Screenshot Handling

- Screenshots are **automatically captured** on test failure.
- Saved to: `reports/screenshots/TC96_forgot_password_FAIL.png`
- The `conftest.py` `driver` fixture and `BaseTest.setup_driver` both include screenshot-on-failure logic.

---

## 📈 Reports

| Report Type | Location | Notes |
|---|---|---|
| **pytest-HTML** | `reports/pytest_script.html` | Self-contained, no external assets |
| **Allure** | `allure-results/` → `allure-report/` | Run `allure serve allure-results/` |
| **Execution log** | `logs/test_execution.log` | Rotating, DEBUG level |

---

## ⚙️ Environment Variables

| Variable | Default | Description |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com/` | Application URL |
| `BROWSER` | `chrome` | `chrome` or `firefox` |
| `HEADLESS` | `true` | Run headless (`true`/`false`) |
| `DEFAULT_TIMEOUT` | `10` | Explicit wait timeout (seconds) |
| `LOG_LEVEL` | `INFO` | Logging verbosity |

---

## 🤝 Contributing

1. Create a feature branch from `qtestidscript`
2. Follow the existing POM structure
3. Ensure all new tests inherit from `BaseTest`
4. Run the full suite before opening a PR

---

*Generated for TC-96 | QTest ID: 11194308 | SauceDemo Automation Project*
