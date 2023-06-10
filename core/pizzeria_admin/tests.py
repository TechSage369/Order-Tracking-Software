from django.test import TestCase

from .utils import get_min_max_year, make_new_year_range


class TestAdminUtils:
    def test_get_min_max_year(self):
        min_year, max_year = get_min_max_year()
        assert min_year == 2020
        assert max_year == 2030

    def test_make_new_year_range_default_setting(self):
        year_range = make_new_year_range()
        assert list(year_range) == [
            2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030]
