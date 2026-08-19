import main
def test_root():
    assert main.root() == {"message": "Hello World"}

def test_convert():
    assert main.convert("PA", "Pittsburgh") == {"lat": 40.4416, "long": -79.9959}