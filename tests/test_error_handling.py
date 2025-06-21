import pytest
import os
from processor import process_csv, compare
from utils import parse_aggregate, parse_filter

CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'products.csv'))


# --- parse_aggregate() error tests ---

def test_parse_aggregate_missing_equalsign():
    with pytest.raises(ValueError, match="Aggregation should be in format column=func"):
        parse_aggregate("pricemedian")

def test_parse_aggregate_unsupported_aggregation():
    with pytest.raises(ValueError, match="Unsupported aggregation:"):
        parse_aggregate("price=range")


# --- parse_filter() error tests ---

def test_parse_filter_invalid_operator():
    with pytest.raises(ValueError, match="Invalid filter expression: No supported operator found"):
        parse_filter("price@1000")
    with pytest.raises(ValueError, match="Invalid filter expression: Multiple operators found"):
        parse_filter("price><1000")


# --- compare() error tests ---

def test_compare_invalid_operator():
    with pytest.raises(ValueError, match="Unsupported operator"):
        compare("10", "**", "5")


# --- process_csv() error-handling tests ---

def test_process_csv_invalid_numeric_filter_value():
    with pytest.raises(ValueError, match="is numeric but value 'abc' is not"):
        process_csv(CSV_PATH, "price>abc")

def test_process_csv_invalid_operator_on_string_column():
    with pytest.raises(ValueError, match="Cannot apply '>' on non-numeric column"):
        process_csv(CSV_PATH, "brand>apple")  # 'brand' is assumed to be non-numeric

def test_process_csv_nonexistent_column_in_filter():
    with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
        process_csv(CSV_PATH, "nonexistent=foo")

def test_process_csv_invalid_order_by_format():
    with pytest.raises(ValueError, match="Invalid order-by format"):
        process_csv(CSV_PATH, order_by="priceasc")

def test_process_csv_invalid_sort_direction():
    with pytest.raises(ValueError, match="Invalid sort direction"):
        process_csv(CSV_PATH, order_by="price=ascending")

def test_process_csv_nonexistent_column_in_order():
    with pytest.raises(ValueError, match="Column 'nonexistent' not found"):
        process_csv(CSV_PATH, order_by="nonexistent=asc")

def test_process_csv_invalid_aggregate_format():
    with pytest.raises(ValueError, match="Unsupported aggregation:"):
        process_csv(CSV_PATH, aggregate_expr="price=sum")

def test_process_csv_aggregate_on_missing_column():
    with pytest.raises(KeyError, match="could not find column:"):
        process_csv(CSV_PATH, aggregate_expr="nonexistent=min")


# Optional sanity checks that still test edge behavior
def test_compare_numeric_with_string_fallback():
    assert not compare("abc", "=", "10")  # Treated as string comparison

def test_compare_valid_numeric_comparison():
    assert compare("100", ">", "50")

def test_compare_valid_string_comparison():
    assert compare("apple", "=", "apple")
