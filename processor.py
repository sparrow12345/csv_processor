import csv
from typing import List, Dict, Optional, Any
from utils import parse_aggregate, parse_filter, is_numeric_column

def read_csv(file_path: str) -> List[Dict[str, str]]:
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))


def process_csv(file_path: str, filter_expr: Optional[str] = None, aggregate_expr: Optional[str] = None, order_by: Optional[str] = None) -> List[Dict[str, Any]]:
    rows = read_csv(file_path)

    # Apply filter
    if filter_expr:
        col, op, val = parse_filter(filter_expr)
        if col not in rows[0]:
            raise ValueError(f"Column '{col}' not found in CSV.")
        if is_numeric_column(rows, col):
            try:
                float(val)  # Try casting filter value to float
            except ValueError:
                raise ValueError(f"Invalid filter: Column '{col}' is numeric but value '{val}' is not.")
        else:
            # Optional: add string-only check, e.g., if operator is < or > on strings
            if op in ("<", ">"):
                raise ValueError(f"Invalid filter: Cannot apply '{op}' on non-numeric column '{col}'.")

        rows = [row for row in rows if compare(row[col], op, val)]

    if order_by:
        try:
            col, direction = order_by.split("=")
        except ValueError:
            raise ValueError(f"Invalid order-by format: '{order_by}'. Expected format 'column:asc' or 'column:desc'.")

        direction = direction.lower()
        if direction not in ("asc", "desc"):
            raise ValueError(f"Invalid sort direction: '{direction}'. Only 'asc' or 'desc' are allowed.")

        if col not in rows[0]:
            raise ValueError(f"Column '{col}' not found in CSV.")

        reverse = direction == "desc"
        try:
            # Try numeric sort
            rows.sort(key=lambda row: float(row[col]), reverse=reverse)
        except ValueError:
            # Fall back to string sort
            rows.sort(key=lambda row: row[col], reverse=reverse)

    # Apply aggregation
    if aggregate_expr:
        agg_func, col = parse_aggregate(aggregate_expr)
        values = [float(row[col]) for row in rows]
        result = {f"{agg_func.__name__}({col})": round(agg_func(values), 2)}
        return [result]

    return rows


def compare(a: str, op: str, b: str) -> bool:
    try:
        a_val = float(a)
        b_val = float(b)
    except ValueError:
        a_val = a
        b_val = b
    
    if op == "=":
        return a_val == b_val
    elif op == ">":
        return a_val > b_val
    elif op == "<":
        return a_val < b_val
    else:
        raise ValueError(f"Unsupported operator: {op}")
