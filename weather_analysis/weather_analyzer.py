import argparse
import asyncio

import dateparser
import matplotlib.pyplot as plt
import pandas as pd
from async_data_loader import AsyncDataLoader
from helper_types import METRICS, WEEKDAYS, CalculationType
from input_validator import InputValidator
from loguru import logger

logger.add('weather_analysis.log', rotation='10 MB')



class WeatherAnalyzer:
    BASE_URL = "https://storage.googleapis.com/spotnix-app-resources/weather_data"

    def __init__(self):
        self.async_loader = AsyncDataLoader(self.BASE_URL)
        logger.info('WeatherAnalyzer initialized with BASE_URL: {}', self.BASE_URL)


    async def analyze_weather(self, args):
        logger.info(f'Starting weather analysis with arguments: {args}')
        start_date = dateparser.parse(args.start_date)
        end_date = dateparser.parse(args.end_date)
        station_ids = args.stations
        metric = METRICS.get(args.metric)
        calculation = CalculationType(args.calculation)
        weekdays_filter = WEEKDAYS.get(args.filter)
        output = args.output
        output_file = args.output_file

        logger.debug(f'Parsed dates: start_date={start_date}, end_date={end_date}')
        logger.debug(f'Metric: {metric}, Calculation: {calculation}, Weekdays filter: {weekdays_filter}')

        try:
            station_metadata = await self.async_loader.load_metadata()
            logger.info('Loaded station metadata')

            date_range = pd.date_range(start_date, end_date)
            if weekdays_filter != WEEKDAYS['none']:
                date_range = date_range[date_range.weekday == weekdays_filter]
            weather_data = await self.async_loader.load_weather_data(date_range)
            if station_ids:
                weather_data = weather_data[weather_data['station_id'].isin(station_ids)]
            weather_data = weather_data[weather_data['metric'] == metric]
            logger.info('Loaded weather data for date range')

            result = self.calculate(weather_data, metric, calculation)
            logger.info('Calculated result using {}', calculation)

            result.index = result.index.map(station_metadata)

            self.handle_output(result, output, output_file, args.metric, calculation)
        except Exception as e:
            logger.error(f'An error occurred: {e}')
            return
        finally:
            await self.async_loader.close()
        logger.info(f'Fetching data from {start_date} to {end_date}')

    @staticmethod
    def calculate(weather_data, metric, calculation_type):
        if metric == METRICS['temperature']:
            weather_data['value'] = weather_data['value'] / 10
        match calculation_type:
            case CalculationType.AVERAGE:
                return weather_data.groupby('station_id')['value'].mean()
            case CalculationType.MIN:
                return weather_data.groupby('station_id')['value'].min()
            case CalculationType.MEDIAN:
                return weather_data.groupby('station_id')['value'].median()
            case CalculationType.DIFF_AVG:
                overall_avg = weather_data['value'].mean()
                station_avg = weather_data.groupby('station_id')['value'].mean()
                return station_avg - overall_avg
            case _:
                logger.error('Invalid calculation type. Choose between average, min, median, diff_avg')


    @staticmethod
    def handle_output(result, output, output_file, metric_name, calculation):
        match output:
            case 'csv':
                if not output_file:
                    output_file = f'{metric_name}_{calculation.value}.csv'
                result.to_frame('value').to_csv(output_file)
                logger.info(f'Data saved to {output_file}')
            case 'plot':
                plt.figure(figsize=(24, 12))
                result.plot(kind='bar')
                plt.title(f'{calculation.value.title()} {metric_name} by Station')
                plt.xlabel('Station')
                plt.ylabel(f'{metric_name} {'(mm)' if metric_name == 'precipitation' else '(°C/10)'}')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.show()
            case _:
                logger.error('Invalid output method. Choose between csv or plot''')

async def main():
    logger.info('Starting Weather Analysis Tool')
    parser = argparse.ArgumentParser(description='Weather Analysis Tool')
    parser.add_argument('--start_date', type=str, help='Start date in format YYYY-MM-DD')
    parser.add_argument('--end_date', type=str, help='End date in format YYYY-MM-DD')
    parser.add_argument('--metric', type=str, choices=METRICS, help='Metric to analyze: precipitation or temperature')
    parser.add_argument('--stations', type=str, nargs='*', help='List of station ids (optional), or all stations if not provided')
    parser.add_argument('--filter', type=str, choices=WEEKDAYS, default='none', help='Filter ')
    parser.add_argument('--calculation', type=str,
                        choices=[calculation.value for calculation in CalculationType],
                        help=f'Type of calculation: {", ".join([calculation.value for calculation in CalculationType])}')
    parser.add_argument('--output', type=str, choices=['csv', 'plot'], help='Output method: csv or plot')
    parser.add_argument('--output_file', type=str, help='File path to save the output if output method is csv')

    args = parser.parse_args()


    weather_analyzer = WeatherAnalyzer()
    InputValidator().validate_input(args)

    await weather_analyzer.analyze_weather(args)

if __name__ == '__main__':
    asyncio.run(main())
