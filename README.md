# 🧪 NoteVault — AI-Enabled Test Automation

[![Selenium Tests](https://github.com/Manish12588/my-notes-app-testing/actions/workflows/selenium-tests.yml/badge.svg)](https://github.com/Manish12588/my-notes-app-testing/actions/workflows/selenium-tests.yml)
[![Allure Report](https://img.shields.io/badge/Allure-Report-orange)](https://manish12588.github.io/my-notes-app-testing/)

An end-to-end AI-powered test automation framework for the [NoteVault](https://github.com/Manish12588/my-notes-app) Flask application — featuring **self-healing tests**, **automated reporting**, and **CI/CD with GitHub Actions**.

> 📊 **[View Live Allure Report](https://manish12588.github.io/my-notes-app-testing/)**

---

## 🌟 What makes this project unique?

Most test suites break when the UI changes and require manual fixes. This framework fixes itself.

| Traditional Testing | This Framework |
|---|---|
| Tests break when locators change | Agent detects and fixes broken locators automatically |
| Manual debugging required | LLM analyzes the DOM and patches the test file |
| Static reports | Live Allure dashboard published to GitHub Pages |
| Tests run manually | Fully automated via GitHub Actions on every push |

---

## 🏗️ Architecture

```
Push to main
    └── GitHub Actions
            ├── Job 1: Start App      → Docker Compose + health check
            ├── Job 2: Setup Env      → Python venv + dependencies
            ├── Job 3: Run Tests      → Pytest + Selenium (13 tests)
            │           └── If fail  → Self-Healing Agent triggers
            │                           ├── Captures page DOM
            │                           ├── LLM finds correct locator
            │                           ├── Patches test file
            │                           └── Reruns tests
            └── Job 4: Publish Report → Allure → GitHub Pages
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Application | Flask (NoteVault notes app) |
| Containerization | Docker + Docker Compose |
| Test Framework | Pytest + Selenium |
| AI / LLM | Ollama (qwen2.5:3b) + LangChain |
| DOM Parsing | BeautifulSoup4 |
| Reporting | Allure + pytest-html |
| CI/CD | GitHub Actions (self-hosted runner) |
| Report Hosting | GitHub Pages |

---

## 📁 Project Structure

```
my-notes-app-testing/
├── .github/
│   └── workflows/
│       └── selenium-tests.yml    # CI/CD pipeline
├── app/                          # Flask NoteVault application
├── docker/                       # Dockerfile
├── healing_agent/
│   ├── agent.py                  # Self-healing agent
│   ├── tools.py                  # DOM capture + file patch utilities
│   ├── requirements.txt
│   └── README.md
├── tests/
│   ├── conftest.py               # Pytest fixtures + screenshot hook
│   ├── test_notes_app.py         # 13 Selenium test cases
│   ├── setup_test_user.py        # One-time test user registration
│   ├── run_tests.sh              # Local test runner script
│   ├── requirements.txt
│   └── README.md
├── docker-compose.yml
└── README.md
```

---

## ⚙️ Prerequisites

- Python 3.10+
- Docker + Docker Compose
- Google Chrome
- Ollama — [download here](https://ollama.com/download)
- GitHub Actions self-hosted runner (for CI)

Pull the LLM model:

```bash
ollama pull qwen2.5:3b
```

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/Manish12588/my-notes-app-testing.git
cd my-notes-app-testing

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install all dependencies
pip install -r app/requirements.txt
pip install -r tests/requirements.txt
pip install -r healing_agent/requirements.txt
```

---

## 🧪 Running Tests Locally

The `run_tests.sh` script handles everything — app startup, test user registration, test execution, and reporting.

```bash
# Normal run — just run the tests
./tests/run_tests.sh

# Break a locator to simulate a UI change, then run tests
./tests/run_tests.sh --break

# Full demo — break locator + run tests + heal + rerun
./tests/run_tests.sh --break --heal
```

**Expected output with `--break --heal`:**

```
🐳 Starting app...
✅ App is healthy (HTTP 200)
👤 Registering test user...
💥 Breaking locator to simulate UI change...
🔍 Running Selenium tests...

3 failed, 10 passed

🔧 Tests failed — triggering self-healing agent...
🌐 Capturing DOM from http://localhost:5000/login...
🤖 LLM suggests: By.ID, "identifier"
✅ Patched 6 occurrence(s)

🔄 Rerunning tests after healing...
13 passed ✅

🎉 All tests passing! Self-healing complete.
```

---

## 🤖 Self-Healing Agent

When a test fails due to a locator change, the agent:

1. Runs pytest and detects which locators are broken
2. Opens a headless Chrome browser and captures the page DOM
3. Sends the broken locator + DOM to an LLM (qwen2.5:3b via Ollama)
4. LLM identifies the correct locator from the actual page elements
5. Patches `test_notes_app.py` with the fix
6. Reruns the tests to verify

**Key design principle:** The LLM does ONE task — identify the correct locator. Everything else is plain Python. This makes the agent reliable on small local models.

---

## 🗂️ Test Coverage

### Authentication (5 tests)
- Register page loads correctly
- New user registers successfully
- Login page loads correctly
- Valid credentials login successfully
- Invalid credentials show error message

### Notes CRUD (8 tests)
- Dashboard loads with navigation
- Add note page loads with form fields
- Create a new note successfully
- Search returns matching notes
- View note detail page
- Edit note title
- Sidebar navigation works
- Logout redirects to login

---

## 📊 Reports

**Allure Report (live):**
🔗 [https://manish12588.github.io/my-notes-app-testing/](https://manish12588.github.io/my-notes-app-testing/)

**HTML Report:** Downloaded as artifact from GitHub Actions after each run.

**Screenshots:** Automatically captured on test failure and attached to both reports.

---

## 🔄 CI/CD Pipeline

The GitHub Actions workflow triggers on every push to `main`:

```
Job 1 — Start App
    └── Cleanup previous containers
    └── Docker Compose up
    └── Health check via /health endpoint

Job 2 — Setup Environment
    └── Create Python venv
    └── Install all dependencies (cached)

Job 3 — Run Tests
    └── Register test user
    └── Run 13 Selenium tests
    └── On failure → Self-healing agent
    └── Upload HTML + Allure artifacts

Job 4 — Publish Report
    └── Download Allure results
    └── Generate Allure report with history
    └── Publish to GitHub Pages
```

---

## 📦 Dependencies

**Tests:**
```
selenium          # Browser automation
pytest            # Test runner
pytest-html       # HTML report generation
allure-pytest     # Allure report integration
webdriver-manager # Auto ChromeDriver management
requests          # Test user registration
```

**Healing Agent:**
```
langchain-ollama  # LLM integration
langchain         # Agent framework
langchain-core    # Tool decorator, messages
langgraph         # ReAct execution engine
beautifulsoup4    # DOM parsing
```

---