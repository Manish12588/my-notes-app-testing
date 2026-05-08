# 🧪 NoteVault — Selenium Test Suite

Automated end-to-end tests for the NoteVault Flask application. Built with **Pytest + Selenium** — tests run headlessly against a live instance of the app and generate both HTML and Allure reports.

---

## 📁 Folder structure

```
tests/
├── conftest.py           # Pytest fixtures (driver setup, session login, screenshot hook)
├── test_notes_app.py     # 13 test cases (auth + notes CRUD)
├── setup_test_user.py    # One-time script to register a test user
├── run_tests.sh          # Test runner script (supports --break and --heal flags)
├── requirements.txt      # Test dependencies
└── README.md             # This file
```

---

## ⚙️ Prerequisites

- Python 3.10+
- Google Chrome installed
- NoteVault app running (via Docker Compose or directly)
- Virtual environment set up with dependencies installed

```bash
pip install -r tests/requirements.txt
```

---

## 🚀 Running Tests

### Option 1 — Shell script (recommended)

Run from project root:

```bash
# Normal run — start app, register user, run tests, stop app
./tests/run_tests.sh

# Break a locator to simulate a UI change, then run tests
./tests/run_tests.sh --break

# Full self-healing demo — break + run + heal + rerun
./tests/run_tests.sh --break --heal
```

The script handles everything automatically:
- Starts the app via Docker Compose
- Waits for the `/health` endpoint to return 200
- Registers the test user
- Runs the full test suite
- Stops the app when done

### Option 2 — Run pytest directly

Start the app first, then:

```bash
# Register test user once
python tests/setup_test_user.py

# Run tests with both reporters
pytest tests/test_notes_app.py -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --no-header
```

---

## 🗂️ Test Coverage

### `TestAuth` — Authentication

| Test | Description |
|---|---|
| `test_register_page_loads` | Register page renders with all fields |
| `test_register_new_user` | New user can register successfully |
| `test_login_page_loads` | Login page renders correctly |
| `test_successful_login` | Valid credentials redirect to dashboard |
| `test_invalid_login` | Wrong credentials show error message |

### `TestNotes` — Notes CRUD

| Test | Description |
|---|---|
| `test_dashboard_loads` | Dashboard loads with New Note button |
| `test_add_note_page_loads` | Add note page renders with title and content fields |
| `test_create_note` | Note can be created and saved |
| `test_search_note` | Search returns matching notes |
| `test_view_note` | Note detail page loads correctly |
| `test_edit_note` | Note title can be updated |
| `test_sidebar_all_notes_link` | Sidebar navigation link is visible |
| `test_logout` | Logout redirects to login page |

---

## 📊 Reports

Reports are generated at project root level — not inside the `tests/` folder.

| Report | Location | How to open |
|---|---|---|
| HTML report | `reports/report.html` | Open in any browser |
| Allure results | `reports/allure-results/` | `allure serve reports/allure-results` |
| Screenshots | `reports/screenshots/` | Auto-captured on test failure |

---

## 📸 Screenshots on Failure

The `conftest.py` hook automatically captures a screenshot when any test fails:

- Saved to `reports/screenshots/<test_name>_<timestamp>.png`
- Attached to the Allure report under the failed test
- Attached to the HTML report inline

No changes needed in test files — the hook fires automatically.

---

## 🔧 Configuration

Test credentials and base URL are defined in `conftest.py`:

```python
BASE_URL   = "http://localhost:5000"
TEST_USER  = f"testuser_{int(time.time())}"   # unique per run
TEST_EMAIL = f"testuser_{int(time.time())}@test.com"
TEST_PASS  = "testpass123"
```

The test user is generated with a timestamp suffix on every run — no conflicts between runs, no need to clean up the database manually.

To test against a deployed instance, change `BASE_URL`:

```python
BASE_URL = "http://<your-ec2-ip>:5000"
```

---

## 🧠 Design Decisions

**Why `scope="session"` for the driver fixture?**
One browser instance shared across all tests — faster execution, no repeated Chrome startup.

**Why explicit `WebDriverWait` instead of `implicitly_wait`?**
`implicitly_wait` is unreliable in headless mode. Explicit waits target specific conditions, making tests stable.

**Why logout before auth tests?**
Flask redirects authenticated users away from `/login`. Each auth test explicitly logs out first to ensure clean state.

**Why unique test users per run?**
Avoids database conflicts between runs without needing cleanup scripts.

---

## 📦 Dependencies

```
selenium          # Browser automation
pytest            # Test runner
pytest-html       # HTML report generation
allure-pytest     # Allure report integration
webdriver-manager # Auto-downloads matching ChromeDriver
requests          # Used by setup_test_user.py
```