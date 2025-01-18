# Weather Analysis Tool

A command-line tool for analyzing weather data from stations around the world. This tool helps weather analysts to load, process, and visualize weather data from multiple stations.

## Features

- Load weather data from remote servers without storing on disk
- Analyze data by date range and specific stations
- Filter data by specific days (e.g., Mondays only)
- Multiple calculation methods:
  - Average value
  - Minimum value
  - Median value
  - Difference from overall average
- Flexible output options:
  - CSV export
  - Bar chart visualization

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Voskov/weather_analyzer.git
cd weather_analyzer
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Command Structure

```bash
python main.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --metric [temperature|precipitation] [options]
```

### Required Arguments

- `--start-date`: Start date in YYYY-MM-DD format
- `--end-date`: End date in YYYY-MM-DD format
- `--metric`: Type of measurement (temperature or precipitation)

### Optional Arguments

- `--stations`: List of station IDs (default: all stations)
- `--filter`: Day filter (none, mondays, tuesdays, etc.)
- `--calculation`: Type of calculation (average, min, median, diff_avg)
- `--output`: Output format (csv or plot)
- `--output-file`: Output file name
 
### Examples

1. Calculate average temperature for specific stations during March 2021:
```bash
python main.py --start-date 2021-03-01 --end-date 2021-04-01 --metric temperature --stations ASN00014651 ASN00091109 US1AZPM0160 US1CAMT0046 US1DENC0028 US1IALE0008 US1NYDT0037 --calculation average --output plot
```

2. Analyze precipitation data on Mondays during March 2021:
```bash
python main.py --start-date 2021-03-01 --end-date 2021-04-01 --metric precipitation --filter mondays --calculation diff_avg --output csv
```

## Author

Ariel Voskov
