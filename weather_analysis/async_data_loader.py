from io import StringIO

import asyncio
import logging
from datetime import datetime
from typing import Dict, List
import aiohttp
import pandas as pd

STATIONS_CSV = "2021_weather_stations.csv"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncDataLoader:
    """Asynchronously loads weather data and station metadata from remote sources."""
    def __init__(self, base_url: str):
        assert base_url, "Base URL is required."
        self.base_url = base_url.rstrip("/")
        self.session = None

    async def _get_file(self, filename: str) -> str:
        """Fetch a single file and return as DataFrame."""
        if self.session is None:
            self.session = aiohttp.ClientSession()

        url = f"{self.base_url}/{filename}"
        try:
            async with self.session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return ""

    async def load_metadata(self, stations_file_name: str = STATIONS_CSV) -> Dict[str, str]:
        """Load station metadata."""
        try:
            raw_metadata = await self._get_file(stations_file_name)
            df = pd.read_csv(StringIO(raw_metadata), usecols=['id', 'name'])
            return dict(zip(df['id'], df['name']))
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return {}

    async def load_weather_data(self, dates: List[datetime]) -> pd.DataFrame:
        """Load weather data for all dates concurrently."""
        async def fetch_date(date: datetime) -> pd.DataFrame:
            filename = f"weather_data_{date.strftime('%Y-%m-%d')}.csv"
            raw_weather_data = await self._get_file(filename)
            return pd.read_csv(StringIO(raw_weather_data))

        # Create tasks for all dates
        tasks = [fetch_date(date) for date in dates]
        dataframes = await asyncio.gather(*tasks)

        if not dataframes:
            raise ValueError("No dataframes found for requested dates.")

        # Combine all dataframes
        return pd.concat(dataframes)

    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.close()
