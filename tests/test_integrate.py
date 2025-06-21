import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processor import process_csv

# Path to the sample CSV in the root folder
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'products.csv'))

# --- Filter-only tests ---

def test_filter_equal_brand():
    result = process_csv(CSV_PATH, "brand=apple", None)
    assert len(result) == 4
    assert all(row["brand"] == "apple" for row in result)

def test_filter_price_greater():
    result = process_csv(CSV_PATH, "price>1000", None)
    assert len(result) == 1
    assert result[0]["name"] == "galaxy s23 ultra"

# --- Aggregate-only tests ---

def test_aggregate_mean_price():
    result = process_csv(CSV_PATH, None, "price=avg")
    key = "mean(price)"
    expected = round(602, 2) ## precalculated
    assert key in result[0]
    assert result[0][key] == expected

def test_aggregate_max_rating():
    result = process_csv(CSV_PATH, None, "rating=max")
    assert result[0]["max(rating)"] == 4.9

def test_aggregate_min_price():
    result = process_csv(CSV_PATH, None, "price=min")
    assert result[0]["min(price)"] == 149

def test_aggregate_median_price():
    result = process_csv(CSV_PATH, None, "price=median")
    # Sorted prices: [149, 199, 299, 349, 429, 599, 799, 999, 999, 1199]
    # Median = (429 + 599) / 2 = 514.0
    assert result[0]["median(price)"] == 514.0

# --- Combined filter + aggregation tests ---

def test_filter_and_aggregate_mean_price_xiaomi():
    result = process_csv(CSV_PATH, "brand=xiaomi", "price=avg")
    # Xiaomi prices: [199, 299, 149] => mean = 215.67
    assert result[0]["mean(price)"] == round(647 / 3, 2)

def test_filter_and_aggregate_max_rating_samsung():
    result = process_csv(CSV_PATH, "brand=samsung", "rating=max")
    # Samsung ratings: [4.8, 4.2, 4.6]
    assert result[0]["max(rating)"] == 4.8

def test_filter_and_aggregate_median_price_apple():
    
    result = process_csv(CSV_PATH, "brand=apple", "price=median")
    # Apple prices: [999, 799, 429, 599] => sorted: [429, 599, 799, 999]
    # Median = (599 + 799)/2 = 699.0
    assert result[0]["median(price)"] == 699.0
