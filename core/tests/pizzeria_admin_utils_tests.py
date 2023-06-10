import datetime
import pytest
from pizzeria_admin.utils import (
    get_present_date,
    get_present_month,
    get_present_year,
    get_week_date_range,
)

from datetime import datetime
from unittest.mock import patch


@pytest.fixture
def mock_datetime():
    return datetime(2023, 4, 26, 10, 0, 0)


class TestUtils:
    def test_get_present_date(self, mock_datetime):

        with patch('datetime.datetime') as mock_datetime_class:
            mock_datetime_class.now.return_value = mock_datetime

            result = get_present_date()

            assert result == mock_datetime

    def test_get_present_month(self, mock_datetime):

        with patch('datetime.datetime') as mock_datetime_class:
            mock_datetime_class.now.return_value = mock_datetime
            result = get_present_month()

            assert result == mock_datetime.month

    def test_get_present_year(self, mock_datetime):

        with patch('datetime.datetime') as mock_datetime_class:
            mock_datetime_class.now.return_value = mock_datetime
            result = get_present_year()

            assert result == mock_datetime.year

    def test_get_week_date_range(self, mock_datetime):

        with patch('datetime.datetime') as mock_datetime_class:
            mock_datetime_class.now.return_value = mock_datetime
            week_start_date, week_end_date = get_week_date_range()

            assert week_start_date.day == 24
            assert week_end_date.day == 26
