from datetime import datetime
import argparse

from helper_types import METRICS, WEEKDAYS, CalculationType


class InputValidator:
    @classmethod
    def validate_input(cls, args: argparse.Namespace) -> None:
        try:
            cls._validate_dates(args.start_date, args.end_date)
            cls._validate_metric(args.metric)
            cls._validate_filter(args.filter)
            cls._validate_calculation(args.calculation)
            cls._validate_output(args.output)
        except AssertionError as e:
            raise ValueError(e)

    @classmethod
    def _validate_dates(cls, start_date, end_date) -> None:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")

        if start_date > end_date:
            raise ValueError("Start date must be before end date")
        if start_date > datetime.now():
            raise ValueError("Start date must be in the past")

    @classmethod
    def _validate_metric(cls, metric: str) -> None:
        assert metric in METRICS, f"Invalid metric. Choose between {', '.join(METRICS)}"

    @classmethod
    def _validate_filter(cls, weekday_filter: str) -> None:
        assert weekday_filter in WEEKDAYS, f"Invalid filter. Choose between {', '.join(WEEKDAYS)}"

    @classmethod
    def _validate_calculation(cls, calculation: str) -> None:
        assert calculation in [c.value for c in CalculationType], (f"Invalid calculation. Choose between"
                                                                   f" {', '.join([c.value for c in CalculationType])}")

    @classmethod
    def _validate_output(cls, output: str) -> None:
        assert output in ['csv', 'plot'], "Invalid output method. Choose between csv or plot"
