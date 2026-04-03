"""
conftest.py
-----------
Root-level pytest configuration file.
Provides:
  - pytest_runtest_makereport hook: attaches test result to request.node
    so BaseTest can detect failures and trigger auto-screenshots.
  - --headless command-line option for CI/headless execution.

TC-96 | QTest ID: 11194308
Test Case: Forgot Password Link is Visible on the Login Page
"""

import pytest


# ── CLI Options ───────────────────────────────────────────────────────────────

def pytest_addoption(parser):
    """Registers custom command-line options for pytest."""
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode (no GUI). Useful for CI/CD pipelines.",
    )


# ── Report Hook ───────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Attaches the test result (rep_call) to the test node so that
    BaseTest.setup_teardown can inspect whether the test PASSED or FAILED
    and trigger an automatic screenshot on failure.
    """
    outcome = yield
    rep = outcome.get_result()

    # Attach the call-phase result to the node
    setattr(item, f"rep_{rep.when}", rep)
