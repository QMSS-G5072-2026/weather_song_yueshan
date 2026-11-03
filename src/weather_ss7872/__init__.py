# read version from installed package
from importlib.metadata import version
__version__ = version("weather_ss7872")

from .weather_ss7872 import celsius_to_fahrenheit
from .weather_ss7872 import summarize_temperatures
from .weather_ss7872 import clean_readings