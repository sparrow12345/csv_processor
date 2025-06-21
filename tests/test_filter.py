from processor import compare

def test_compare_numeric():
    assert not compare("10", ">", "10")
    assert not compare("10", "<", "10")
    assert not compare("10", "=", "5")
    assert compare("10", "=", "10")


def test_compare_string():
    assert compare("apple", "=", "apple") is True
    assert compare("apple", "=", "banana") is False
