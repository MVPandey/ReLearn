
set -e


cd "$(dirname "$0")/.."

echo "Checking for required packages..."
python -m pip install pytest pytest-cov

echo "Running tests with coverage..."


python -m pytest tests/ \
  --cov=app \
  --cov-report=term \
  --cov-report=html:coverage_html \
  --cov-report=xml:coverage.xml \
  -v

echo "Tests completed successfully!" 