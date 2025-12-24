from datetime import timedelta, datetime
from enum import Enum
from typing import Tuple, Optional

import streamlit as st


def _ceil_to_next_hour(dt: datetime) -> datetime:
    base = dt.replace(minute=0, second=0, microsecond=0)
    return base + timedelta(hours=1)


def _get_default_start_time() -> datetime:
    now = datetime.now()
    default_end = _ceil_to_next_hour(now)
    default_start = default_end - timedelta(hours=2)
    return default_start


def _get_default_end_time() -> datetime:
    now = datetime.now()
    default_end = _ceil_to_next_hour(now)
    return default_end


class TestStatus(Enum):
    ALL = "ALL"
    COMPLETED = "COMPLETED"
    ESCALATED = "ESCALATED"
    DISCARED = "DISCARED"
    FAILED = "FAILED"


class TestedFetch:
    """Set up time period component"""

    def __init__(self):
        self._stored_start: datetime = _get_default_start_time()
        self._stored_end: datetime = _get_default_end_time()
        self._status: Optional[TestStatus] = None

    @property
    def stored_start(self):
        return self._stored_start

    @stored_start.setter
    def stored_start(self, value):
        self._stored_start = value

    @property
    def stored_end(self):
        return self._stored_end

    @stored_end.setter
    def stored_end(self, value):
        self._stored_end = value

    @property
    def status(self):
        return self._status

    def render_component(self):
        cols = st.columns([1, 1, 0.5, 0.5])
        self._stored_start = cols[0].datetime_input("Log Start", value=self.stored_start)
        self._stored_end = cols[1].datetime_input("Log End", value=self.stored_end)
        self._status = cols[2].selectbox(
            "Filter",
            options=["ALL", "COMPLETED", "ESCALATED", "DISCARED", "FAILED"])
        cols[3].container(height=10, border=False)
        fetch_button = cols[3].button("Fetch", type="primary",
                                use_container_width=True)
        return fetch_button
