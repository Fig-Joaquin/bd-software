python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

python scripts/load_data.py

python scripts/run.py