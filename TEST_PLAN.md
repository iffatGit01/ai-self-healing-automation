AI-Powered Self-Healing Automation Framework — Test Plan
1. Objective

The objective is to develop an automated testing framework for the Banking Application using Playwright + pytest, with an AI-powered self-healing mechanism capable of detecting locator failures, identifying replacement elements, validating the replacement, and recovering the test execution.

2. Scope

The automation will cover:

Login
Invalid login
Dashboard
Account balance
Deposit
Withdrawal
Transaction history
Logout
UI validation
Negative scenarios
Locator failure detection
Self-healing scenarios
AI-based failure analysis
3. Major Test Cases
TC ID	Test Scenario	Expected Result	Priority
TC-001	Login with valid credentials	User successfully logs in and dashboard is displayed	High
TC-002	Login with invalid username	Appropriate login error is displayed	High
TC-003	Login with invalid password	Appropriate login error is displayed	High
TC-004	Login with empty credentials	Validation/error message is displayed	Medium
TC-005	Verify dashboard after login	Dashboard, account information and balance are displayed	High
TC-006	Verify initial account balance	Correct initial balance is displayed	High
TC-007	Deposit valid amount	Balance increases correctly	High
TC-008	Deposit zero/negative amount	Deposit is rejected	High
TC-009	Deposit amount exceeding limit	Deposit is rejected with appropriate message	Medium
TC-010	Withdraw valid amount	Balance decreases correctly	High
TC-011	Withdraw amount greater than balance	Withdrawal is rejected	High
TC-012	Withdraw zero/negative amount	Withdrawal is rejected	Medium
TC-013	Withdraw amount exceeding limit	Withdrawal is rejected	Medium
TC-014	Verify transaction history after deposit	Deposit transaction is recorded correctly	High
TC-015	Verify transaction history after withdrawal	Withdrawal transaction is recorded correctly	High
TC-016	Logout	User returns to login screen	High
TC-017	Verify UI elements	Required fields/buttons/sections are displayed correctly	Medium
TC-018	Locator failure detection	Framework detects failed locator	Critical
TC-019	Self-heal changed locator	Framework identifies and uses replacement locator	Critical
TC-020	Validate healed locator	Replacement locator successfully performs intended action	Critical
TC-021	AI confidence evaluation	Framework calculates confidence for healing candidate	Critical
TC-022	Low-confidence healing	Framework does not blindly heal and reports failure	Critical
TC-023	AI failure classification	Framework identifies non-locator failures correctly	High
TC-024	Healing report generation	Healing details are included in automation report	High
4. Self-Healing Scenarios

These are the most important tests for our project.

SH-001 — ID Change

Original:

<button id="login-btn">Login</button>

Changed:

<button id="signin-btn">Login</button>

Expected:

Original locator fails
        ↓
Framework detects failure
        ↓
Finds replacement
        ↓
Validates replacement
        ↓
Test passes
SH-002 — Text Change

Original:

Login

Changed:

Sign In

Expected:

AI understands semantic similarity
        ↓
Identifies Sign In as intended element
        ↓
Validates
        ↓
Test passes
SH-003 — Attribute Change

Example:

<input id="username">

changed to:

<input id="user-name" placeholder="Username">

Expected:

AI identifies the intended username field
SH-004 — DOM Structure Change

The element's surrounding HTML structure changes while its business purpose remains the same.

Expected:

AI analyzes DOM context
        ↓
Identifies intended element
        ↓
Heals locator
SH-005 — Genuine Application Failure

Example:

Deposit $100
Expected balance: $1100
Actual balance: $1000

Expected:

AI identifies this as a business/application failure
NOT a locator failure
        ↓
Do NOT self-heal
        ↓
Generate failure analysis

This test is particularly important because our framework must not hide genuine defects.

5. Automation Strategy

We'll implement the automation in this order:

1. Application setup
       ↓
2. Playwright configuration
       ↓
3. Page Object Model
       ↓
4. pytest fixtures
       ↓
5. Basic functional tests
       ↓
6. Failure detection
       ↓
7. DOM analysis
       ↓
8. Candidate locator generation
       ↓
9. AI analysis
       ↓
10. Confidence scoring
       ↓
11. Locator validation
       ↓
12. Self-healing
       ↓
13. AI failure analysis
       ↓
14. Allure reporting
       ↓
15. Docker
       ↓
16. GitHub Actions

We will not jump to AI immediately. First we need a reliable baseline automation suite.

Your immediate task

For Step 1 only, create:

TEST_PLAN.md

and paste the test plan above.

Your project should now look like:

AI-SELF-HEALING-AUTOMATION
│
├── .venv
├── .gitignore
├── requirements.txt
└── TEST_PLAN.md

Once you've created that file, tell me "done".

Then I'll give you Step 2 only: how to put your banking application into this project and run it locally.