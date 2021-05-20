"""PayPal API Client."""  # noqa: WPS226
# -*- coding: utf-8 -*-

import logging
from typing import Callable, List, Generator
from tap_buildwith.cleaners import CLEANERS
from dateutil.rrule import DAILY, rrule
from datetime import date, datetime, timedelta

API_SCHEME: str = 'https://'
API_BASE_URL: str = 'api.builtwith.com'
API_TRENDS: str = '/trends/v6/api.json?'
API_KEY: str = '?KEY=:key:'
API_TECH: str = '?TECH=:tech:'
API_DATE: str = '?DATE=:date:'


class Buildwith(object):  # noqa: WPS230
    """Postmark API Client."""

    def __init__(
        self,
        api_key: str,
    ) -> None:  # noqa: DAR101
        """Initialize client.

        Arguments:
            api_key {str} -- Buildwith API key
        """
        self.api_key: str = api_key

    def trends(
        self,
        **kwargs: dict,
    ) -> Generator[dict, None, None]:
        """Get all trends from a technology from date.

        Raises:
                ValueError: When the parameter start_date is missing

        Yields:
                Generator[dict] --  Cleaned Trends Data
        """
        # Validate the start_date value exists
        start_date_input: str = str(kwargs.get('start_date', ''))

        if not start_date_input:
            raise ValueError('The parameter start_date is required.')

        cleaner: Callable = CLEANERS.get('postmark_stats_outbound_bounces', {})

        self._set_api_key()

        for date_day in self._start_days_till_now(start_date_input):

            # Replace placeholder in reports path
            from_to_date: str = API_DATE.replace(
                ':date:',
                date_day,
            )
            # Replace placeholder in reports path
            tech: str = API_TECH.replace(
                ':tech:',
                date_day,
            )
            url: str = (
                f'{API_SCHEME}{API_BASE_URL}{API_TRENDS}'
                f'{from_to_date}{tech}{self.api_key_url}'
            )
            

    def _set_api_key(
        self,
    ) -> None:
        # Replace apikey placeholder in API path
        api_key_url: str = API_KEY.replace(
            ':key:',
            self.api_key,
        )
        self.api_key_url = api_key_url

    def _start_days_till_now(
        self,
        start_date: str,
    ) -> Generator:
        """Yield YYYY/MM/DD for every day until now.

        Arguments:
            start_date {str} -- Start date e.g. 2020-01-01

        Yields:
            Generator -- Every day until now.
        """
        # Parse input date
        year: int = int(start_date.split('-')[0])
        month: int = int(start_date.split('-')[1].lstrip())
        day: int = int(start_date.split('-')[2].lstrip())

        # Setup start period
        period: date = date(year, month, day)

        # Setup itterator
        dates: rrule = rrule(
            freq=DAILY,
            dtstart=period,
            until=datetime.utcnow(),
        )

        # Yield dates in YYYY-MM-DD format
        yield from (date_day.strftime('%Y-%m-%d') for date_day in dates)