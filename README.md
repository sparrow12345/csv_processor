# CSV Processor 📊

A simple Python-based command-line tool to filter, aggregate, and sort CSV files.

---

## 📁 Project Structure

$ ./tree-md .
# Project Structure

my-app/
├─ processor.py
├─ products.csv
├─ main.py
├─ utils.py
├─ __init__.py
├─ tests/
├─ requirements.txt
├─ README.md


## 🚀 Setup Instructions

1. Clone the Repository

```
git clone https://github.com/your-username/csv_processor.git
```

2. Create and Activate a Virtual Environment

```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install Dependencies

```
pip install -r requirements.txt
```

4. 🧪 Running Tests
This project uses pytest for testing. To run all tests:

```
pytest
```

If you want a detailed report with coverage:

```
pytest --cov=.
```

5. 🛠️ Usage (Command-Line Interface)
Run the CLI using main.py:

```
python main.py product.csv [--where FILTER] [--aggregate AGGREGATE] [--order-by ORDER]
```

6. 🔤 Arguments
| Argument	| Description |
|-----------|-------------|
|--where	| Filter rows. Format: column/operator/value (e.g. price>500)|
|--aggregate| Apply aggregation. Format: func=column (e.g. avg=price)|
|--order-by	| Sort the rows. Format: column=asc or column=desc (e.g. rating=desc)|

6. 🧾 Examples
Filter phones with price > 500, calculate the average price across all rows, or order rows by rating.

```
python main.py products.csv --where price>500

python main.py products.csv --aggregate avg=price

python main.py products.csv --order-by rating=desc
```