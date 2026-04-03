# TC-96 — Forgot Password Link is Visible on the Login Page

| Field | Details |
|---|---|
| **Test Case ID** | TC-96 |
| **QTest ID** | 11194308 |
| **Priority** | 🔴 High |
| **URL** | https://www.saucedemo.com/ |
| **Linked Requirement** | SAUC-7 — Allow Users to Reset Their Password |

---

## 🏗️ Project Structure

```
project_root/
├── pages/
│   ├── __init__.py
│   ├── base_page.py          ← Reusable: find, click, screenshot, is_present
│   └── login_page.py         ← LoginPage POM: 10+ locators, 13-strategy forgot detector
├── tests/
│   ├── __init__.py
│   ├── base_test.py          ← BaseTest: setup/teardown, auto-screenshot on fail
│   └── test_tc96_forgot_password.py  ← 4 test methods covering all 3 TC steps
├── utils/
│   ├── __init__.py
│   ├── driver_factory.py     ← Chrome driver, maximize, headless support
│   ├── logger.py             ← File + console logging
│   └── wait_helper.py        ← Explicit WebDriverWait strategies
├── conftest.py               ← pytest_runtest_makereport + auto-screenshot hook
├── pytest.ini                ← HTML report, markers, test discovery, logging
├── requirements.txt          ← selenium, pytest, pytest-html, webdriver-manager
└── reports/
    ├── pytest_script.html    ← 📄 Generated HTML test report
    └── screenshots/          ← Auto-captured failure screenshots
```

---

## 🧪 Test Cases

| # | Test Name | Step | Expected | Status |
|---|---|---|---|---|
| 1 | `test_step1_login_page_is_displayed` | Step 1 | Login page loads | ✅ PASS |
| 2 | `test_step2_forgot_password_link_visible` | Step 2 | Link visible | ❌ FAIL |
| 3 | `test_step3_forgot_password_click_navigates` | Step 3 | Navigate to reset | ❌ FAIL |
| 4 | `test_tc96_forgot_password_link_full_flow` | Full Flow | All 3 steps pass | ❌ FAIL |

---

## 🔴 Root Cause

> **`SauceDemo` does NOT implement a "Forgot Password" feature.**
> The DOM contains **0 anchor tags** and **no elements** matching any of **13 exhaustive
> selector strategies**.
> **Requirement SAUC-7 — Allow Users to Reset Their Password — is NOT SATISFIED.**

---

## 🚀 Running the Tests

### Prerequisites

```bash
pip install -r requirements.txt
```

### Run all TC-96 tests (headed browser)

```bash
pytest tests/test_tc96_forgot_password.py -v
```

### Run in headless mode (CI/CD)

```bash
pytest tests/test_tc96_forgot_password.py -v --headless
```

### Run a specific step

```bash
# Step 1 only
pytest tests/test_tc96_forgot_password.py -v -m step1

# Step 2 only
pytest tests/test_tc96_forgot_password.py -v -m step2

# Full flow only
pytest tests/test_tc96_forgot_password.py -v -m full_flow
```

### Generate HTML report

The `pytest.ini` already configures `--html=reports/pytest_script.html`.
The report is auto-generated on every run at `reports/pytest_script.html`.

---

## 📊 Execution Results

```
PASSED  tests/test_tc96_forgot_password.py::TestTC96ForgotPassword::test_step1_login_page_is_displayed    (0.42s)
FAILED  tests/test_tc96_forgot_password.py::TestTC96ForgotPassword::test_step2_forgot_password_link_visible (0.61s)
FAILED  tests/test_tc96_forgot_password.py::TestTC96ForgotPassword::test_step3_forgot_password_click_navigates (0.58s)
FAILED  tests/test_tc96_forgot_password.py::TestTC96ForgotPassword::test_tc96_forgot_password_link_full_flow   (0.79s)

4 passed=1 failed=3 | Pass Rate: 25%
```

---

## 📸 Screenshot on Failure

Auto-captured via `conftest.py → pytest_runtest_makereport` hook → `BasePage.take_screenshot()`.

**Path:** `reports/screenshots/test_tc96_forgot_password_link_full_flow_FAIL_<timestamp>.png`

---

## 🔗 Requirement Traceability

| Requirement | Description | Status |
|---|---|---|
| SAUC-7 | Allow Users to Reset Their Password | ❌ NOT IMPLEMENTED |
