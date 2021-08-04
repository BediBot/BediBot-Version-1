import unittest
from commands import _email, _dateFunctions

class helper_functions_Test(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_key_generation(self):
        key = _email.get_unique_key()
        assert len(key) == 10
    
    def test_valid_birthday(self):
        valid_year = str(2002)
        valid_month = str(10)
        valid_day = str(16)
        invalid_month = str(-13)
        invalid_day = str(-888)
        invalid_year = str(-123123)


        result = _dateFunctions.check_for_errors_in_date(valid_year, valid_month, valid_day)
        assert result == 0

        
        result = _dateFunctions.check_for_errors_in_date(valid_year, valid_month, invalid_day)
        assert result != 0

        
        result = _dateFunctions.check_for_errors_in_date(valid_year, invalid_month, valid_day)
        assert result != 0

        result = _dateFunctions.check_for_errors_in_date(invalid_year, valid_month, valid_day)
        assert result != 0
