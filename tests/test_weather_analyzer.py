import argparse
import pytest
import pytest_asyncio

from weather_analysis.weather_analyzer import WeatherAnalyzer

BASE_URL = "https://storage.googleapis.com/spotnix-app-resources/weather_data"
METADATA_FILE_NAME = "2021_weather_stations.csv"

@pytest_asyncio.fixture
async def weather_analyzer():
    analyzer = WeatherAnalyzer()
    yield analyzer
    await analyzer.async_loader.close()

class TestWeatherAnalyzer:

        @pytest.mark.asyncio
        async def test_analyze_weather(self, weather_analyzer):
            args = argparse.Namespace(
                start_date='2021-11-10',
                end_date='2021-11-11',
                stations=[],
                metric='temperature',
                calculation='mean',
                output='csv',
                output_file=None
            )
            await weather_analyzer.analyze_weather(args)
            assert True