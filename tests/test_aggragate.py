from utils import parse_aggregate

def test_avg():
    func, col = parse_aggregate("price=avg")
    assert func([100, 200, 300]) == 200.0

def test_median():
    func, col = parse_aggregate("price=median")
    assert func([1, 3, 5]) == 3.0
    assert func([1, 3, 5, 7]) == 4.0  # average of 3 and 5

def test_min_max():
    assert parse_aggregate("rating=min")[0]([3.0, 4.0, 5.0]) == 3.0
    assert parse_aggregate("rating=max")[0]([3.0, 4.0, 5.0]) == 5.0
