from enum import Enum
from typing import Dict, Optional


class CalculationType(Enum):
    AVERAGE = 'average'
    MIN = 'min'
    MEDIAN = 'median'
    DIFF_AVG = 'diff_avg'

METRICS: Dict[str, str] = {
    'precipitation': 'PRCP',
    'temperature': 'TAVG'
}

WEEKDAYS: Dict[str, Optional[int]] = {
    'none': None,
    'mondays': 0,
    'tuesdays': 1,
    'wednesdays': 2,
    'thursdays': 3,
    'fridays': 4,
    'saturdays': 5,
    'sundays': 6,
}
