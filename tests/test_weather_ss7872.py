import weather_ss7872

import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from weather_ss7872 import (
    celsius_to_fahrenheit,
    clean_readings,
    summarize_temperatures,
)

# =============================================================================
# PART 1: UNIT TESTS
# =============================================================================


@pytest.mark.parametrize(
    "celsius, expected",
    [
        (0, 32.0),
        (100, 212.0),
        (-40, -40.0),
        (37, 98.6),
        (-273.15, -459.67),
    ],
)
def test_celsius_to_fahrenheit(celsius, expected):
    """Check temperature conversion for five known values."""
    assert celsius_to_fahrenheit(celsius) == pytest.approx(expected)


@pytest.mark.parametrize(
    "bad_input, expected_error",
    [
        ("warm", TypeError),
        (None, TypeError),
        (True, TypeError),
        (-273.16, ValueError),
    ],
)
def test_celsius_to_fahrenheit_invalid(bad_input, expected_error):
    """Check that invalid inputs raise the expected errors."""
    with pytest.raises(expected_error):
        celsius_to_fahrenheit(bad_input)


def test_summarize_temperatures():
    """Check that the summary ignores NaN and counts missing values."""
    # Arrange
    temps = [10.0, float("nan"), 20.0]

    # Act
    result = summarize_temperatures(temps)

    # Assert
    assert result["mean"] == pytest.approx(15.0)
    assert result["min"] == 10.0
    assert result["max"] == 20.0
    assert result["n_missing"] == 1


# =============================================================================
# PART 2: FIXTURES
# =============================================================================


@pytest.fixture
def raw_readings():
    """Provide unsorted readings with one missing and one implausible value."""
    return pd.DataFrame({
        "station": ["JFK", "CPK", "JFK", "CPK", "LGA"],
        "date": [
            "2026-07-02",
            "2026-07-01",
            "2026-07-01",
            "2026-07-02",
            "2026-07-01",
        ],
        "temp_c": [30.0, 25.0, float("nan"), 999.0, 28.0],
    })


def test_raw_readings_fixture(raw_readings):
    """Check the fixture's columns, row count, and missing values."""
    assert list(raw_readings.columns) == ["station", "date", "temp_c"]
    assert len(raw_readings) == 5
    assert raw_readings["temp_c"].isna().sum() == 1
    assert raw_readings.isna().sum().sum() == 1


# =============================================================================
# PART 3: TESTING DATAFRAMES
# =============================================================================


def test_clean_readings(raw_readings):
    """Check that cleaning removes invalid rows, sorts, and adds Fahrenheit."""
    # Arrange
    expected = pd.DataFrame({
        "station": ["CPK", "JFK", "LGA"],
        "date": ["2026-07-01", "2026-07-02", "2026-07-01"],
        "temp_c": [25.0, 30.0, 28.0],
        "temp_f": [77.0, 86.0, 82.4],
    })

    # Act
    result = clean_readings(raw_readings)

    # Assert
    assert_frame_equal(result, expected)

def test_version_is_defined():
    assert isinstance(weather_ss7872.__version__, str)
