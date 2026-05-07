#!/bin/bash

echo "🧪 Running NoteVault Test Suite"
echo "================================"

# Go to project root
cd "$(dirname "$0")/.."

# Parse arguments
HEAL_MODE=false
BREAK_MODE=false

for arg in "$@"; do
  case $arg in
    --break) BREAK_MODE=true ;;
    --heal)  HEAL_MODE=true ;;
  esac
done

# Start app via Docker Compose
echo "🐳 Starting app..."
docker compose up -d

# Wait for app to be ready via health endpoint
echo ""
echo "⏳ Waiting for app to start..."
for i in {1..15}; do
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/health)
  if [ "$STATUS" = "200" ]; then
    echo "✅ App is healthy (HTTP 200)"
    break
  fi
  echo "   Attempt $i/15 — status: $STATUS, retrying..."
  sleep 2
done

# Create reports directory
mkdir -p reports

# Register test user
echo ""
echo "👤 Registering test user..."
python tests/setup_test_user.py

# Break locator if --break flag passed
if [ "$BREAK_MODE" = true ]; then
  echo ""
  echo "💥 Breaking locator to simulate UI change..."
  sed -i 's/By.ID, "identifier"/By.ID, "user-input"/g' tests/test_notes_app.py
  echo "✅ Locator broken: 'identifier' → 'user-input'"
  echo ""
fi

# Run tests
echo ""
echo "🔍 Running Selenium tests..."
pytest tests/test_notes_app.py -v \
  --html=reports/report.html \
  --self-contained-html \
  --alluredir=reports/allure-results \
  --no-header

EXIT_CODE=$?

# Run healing agent if --heal flag passed and tests failed
if [ "$HEAL_MODE" = true ] && [ $EXIT_CODE -ne 0 ]; then
  echo ""
  echo "🔧 Tests failed. Running self-healing agent..."
  python healing_agent/agent.py

  # Rerun tests after healing
  echo ""
  echo "🔄 Rerunning tests after healing..."
  pytest tests/test_notes_app.py -v \
    --html=reports/report.html \
    --self-contained-html \
    --alluredir=reports/allure-results \
    --no-header

  EXIT_CODE=$?
fi

# Stop app
echo ""
echo "🛑 Stopping app..."
docker compose down

# Report result
if [ $EXIT_CODE -eq 0 ]; then
  echo ""
  echo "✅ All tests passed!"
  echo "📊 HTML report:    reports/report.html"
  echo "📊 Allure results: reports/allure-results"
  echo "📸 Screenshots:    reports/screenshots/"
else
  echo ""
  echo "❌ Some tests failed. Check reports for details."
  exit 1
fi
