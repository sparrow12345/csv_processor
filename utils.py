from typing import Tuple, Callable, List
import statistics

def is_numeric_column(rows: List[dict], col: str) -> bool:
    try:
        float(rows[0][col])
        return True
    except (ValueError, KeyError):
        return False


def parse_filter(expression: str) -> Tuple[str, str, str]:

    supported_operators = ["<", ">", "="]
    matched_ops = [op for op in supported_operators if op in expression]
    
    if not matched_ops:
        raise ValueError(f"Invalid filter expression: No supported operator found in '{expression}'.")
    
    if len(matched_ops) > 1:
        raise ValueError(f"Invalid filter expression: Multiple operators found in '{expression}'. Only one is allowed.")
    
    op = matched_ops[0]
    parts = expression.split(op)

    if len(parts) != 2:
        raise ValueError(f"Invalid filter expression: Expected format 'column{op}value', but got '{expression}'.")

    col, val = parts
    if not col.strip() or not val.strip():
        raise ValueError(f"Invalid filter expression: Column and value must be non-empty. Got: '{expression}'.")

    return col.strip(), op, val.strip()


def parse_aggregate(expression: str) -> Tuple[Callable, str]:
    parts = expression.split("=")
    if len(parts) != 2:
        raise ValueError("Aggregation should be in format column=func")
    col, func_name = parts
    func_name = func_name.lower()

    columns = ["name", "brand", "price", "rating"]

    if (func_name in columns):
        raise KeyError("Aggregation should be in format column=func not the other way around")

    if (col not in columns):
        raise KeyError(f"could not find column: {col} in the dataset columns")
    
    if func_name == "avg":
        return (statistics.mean, col)
    elif func_name == "min":
        return (min, col)
    elif func_name == "max":
        return (max, col)
    elif func_name == "median":
        return (statistics.median, col)
    else:
        raise ValueError(f"Unsupported aggregation: {func_name}")
