from src.etl.validator import Validator


def test_validator():

    Validator().run()

    assert True