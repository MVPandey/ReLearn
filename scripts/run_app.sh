set -e

cd "$(dirname "$0")/.."

if [ ! -d "venv" ]; then
  echo "Creating virtual environment..."
  python -m venv venv
fi

source venv/bin/activate

echo "Installing requirements..."
if [ -f "requirements.txt" ]; then
  pip install -r requirements.txt
else
  echo "Warning: requirements.txt not found. Skipping installation."
fi

echo "Starting ReLearn API"
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload 