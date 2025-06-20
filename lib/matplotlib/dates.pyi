import datetime
from typing import Any, Callable, overload, Sequence

import numpy as np

from .axis import Axis
from .projections.polar import _AxisWrapper
from .ticker import _DummyAxis, Formatter, Locator
from .units import AxisInfo, ConversionInterface

# --- Global Functions ---

def _get_tzinfo(tz: str | datetime.tzinfo | None = ...) -> datetime.tzinfo: ...

def _reset_epoch_test_example() -> None: ...

def set_epoch(epoch: str) -> None: ...

def get_epoch() -> str: ...

def _dt64_to_ordinalf(d: np.ndarray) -> np.ndarray: ...

def _from_ordinalf(x: float, tz: str | datetime.tzinfo | None = ...) -> datetime.datetime: ...

@overload
def datestr2num(d: str, default: datetime.datetime | None = ...) -> float: ...
@overload
def datestr2num(d: list[str], default: datetime.datetime | None = ...) -> np.ndarray: ...

@overload
def date2num(d: datetime.datetime | np.datetime64) -> float: ...
@overload
def date2num(d: Sequence[datetime.datetime | np.datetime64]) -> np.ndarray: ...

@overload
def num2date(x: float, tz: str | datetime.tzinfo | None = ...) -> datetime.datetime: ...
@overload
def num2date(x: Sequence[float], tz: str | datetime.tzinfo | None = ...) -> list[datetime.datetime]: ...

@overload
def num2timedelta(x: float) -> datetime.timedelta: ...
@overload
def num2timedelta(x: Sequence[float]) -> list[datetime.timedelta]: ...

def drange(dstart: datetime.datetime, dend: datetime.datetime, delta: datetime.timedelta) -> np.ndarray: ...

def _wrap_in_tex(text: str) -> str: ...

# --- Formatter Classes ---

class DateFormatter(Formatter):
    tz: datetime.tzinfo
    fmt: str

    def __init__(self, fmt: str, tz: str | datetime.tzinfo | None = ..., *, usetex: bool | None = ...) -> None: ...
    def __call__(self, x: float, pos: int | None = ...) -> str: ...
    def set_tzinfo(self, tz: str | datetime.tzinfo | None) -> None: ...

class ConciseDateFormatter(Formatter):
    _locator: Locator
    _tz: str | datetime.tzinfo | None
    formats: list[str]
    defaultfmt: str
    zero_formats: list[str]
    offset_formats: list[str]
    offset_string: str
    show_offset: bool

    def __init__(self, locator: Locator,
                 tz: str | datetime.tzinfo | None = ...,
                 formats: Sequence[str] | None = ...,
                 offset_formats: Sequence[str] | None = ...,
                 zero_formats: Sequence[str] | None = ...,
                 show_offset: bool = ...,
                 *, usetex: bool | None = ...) -> None: ...
    def __call__(self, x: float, pos: int | None = ...) -> str: ...
    def format_ticks(self, values: Sequence[float]) -> list[str]: ...
    def get_offset(self) -> str: ...
    def format_data_short(self, value: float) -> str: ...

class AutoDateFormatter(Formatter):
    _locator: Locator
    _tz: str | datetime.tzinfo | None
    defaultfmt: str
    _formatter: DateFormatter
    _usetex: bool | None
    scaled: dict[float, str | Callable[[float, int | None], str]]

    def __init__(self, locator: Locator,
                 tz: str | datetime.tzinfo | None = ...,
                 defaultfmt: str = ...,
                 *, usetex: bool | None = ...) -> None: ...
    def _set_locator(self, locator: Locator) -> None: ...
    def __call__(self, x: float, pos: int | None = ...) -> str: ...

# --- rrulewrapper ---

class rrulewrapper:
    def __init__(self, freq: int, tzinfo: datetime.tzinfo | None = ..., **kwargs: Any) -> None: ...
    def set(self, **kwargs: Any) -> None: ...
    def _update_rrule(self, **kwargs: Any) -> None: ...
    def _attach_tzinfo(self, dt: datetime.datetime, tzinfo: datetime.tzinfo) -> datetime.datetime: ...
    def _aware_return_wrapper(self, f: Callable[..., Any], returns_list: bool = ...) -> Callable[..., Any]: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setstate__(self, state: dict) -> None: ...

# --- Locator Classes ---

class DateLocator(Locator):
    hms0d: dict[str, int]

    def __init__(self, tz: datetime.tzinfo | None = ...) -> None: ...
    def set_tzinfo(self, tz: datetime.tzinfo | None) -> None: ...
    def datalim_to_dt(self) -> tuple[datetime.datetime, datetime.datetime]: ...
    def viewlim_to_dt(self) -> tuple[datetime.datetime, datetime.datetime]: ...
    def _get_unit(self) -> float: ...
    def _get_interval(self) -> int: ...
    def nonsingular(self, v0: float, v1: float) -> tuple[float, float]: ...

class RRuleLocator(DateLocator):
    def __init__(self, o: rrulewrapper, tz: datetime.tzinfo | None = ...) -> None: ...
    def __call__(self) -> list[float]: ...
    def tick_values(self, vmin: float, vmax: float) -> list[float]: ...
    def _create_rrule(self, vmin: datetime.datetime, vmax: datetime.datetime) -> tuple[datetime.datetime, datetime.datetime]: ...
    def _get_unit(self) -> float: ...
    @staticmethod
    def get_unit_generic(freq: int) -> float: ...
    def _get_interval(self) -> int: ...

class AutoDateLocator(DateLocator):
    def __init__(self, tz: str | datetime.tzinfo | None = ..., minticks: int = ...,
                 maxticks: int | dict[int, int] | None = ...,
                 interval_multiples: bool = ...) -> None: ...
    def __call__(self) -> list[float]: ...
    def tick_values(self, vmin: float, vmax: float) -> list[float]: ...
    def nonsingular(self, v0: float, v1: float) -> tuple[float, float]: ...
    def _get_unit(self) -> float: ...
    def get_locator(self, dmin: datetime.datetime, dmax: datetime.datetime) -> RRuleLocator: ...


class YearLocator(RRuleLocator):
    def __init__(self, base: int = ..., month: int = ..., day: int = ...,
                 tz: str | datetime.tzinfo | None = ...) -> None: ...
    def _create_rrule(self, vmin: datetime.datetime, vmax: datetime.datetime) -> tuple[datetime.datetime, datetime.datetime]: ...


class MonthLocator(RRuleLocator):
    def __init__(self, bymonth: int | list[int] | None = ...,
                 bymonthday: int = ..., interval: int = ...,
                 tz: str | datetime.tzinfo | None = ...) -> None: ...

class WeekdayLocator(RRuleLocator):
    def __init__(self, byweekday: int | list[int] = ..., interval: int = ..., tz: str | datetime.tzinfo | None = ...) -> None: ...


class DayLocator(RRuleLocator):
    def __init__(self, bymonthday: int | list[int] | None = ..., interval: int = ..., tz: str | datetime.tzinfo | None = ...) -> None: ...


class HourLocator(RRuleLocator):
    def __init__(self, byhour: int | list[int] | None = ..., interval: int = ..., tz: str | datetime.tzinfo | None = ...) -> None: ...


class MinuteLocator(RRuleLocator):
    def __init__(self, byminute: int | list[int] | None = ..., interval: int = ..., tz: str | datetime.tzinfo | None = ...) -> None: ...


class SecondLocator(RRuleLocator):
    def __init__(self, bysecond: int | list[int] | None = ..., interval: int = ..., tz: str | datetime.tzinfo | None = ...) -> None: ...


class MicrosecondLocator(DateLocator):
    def __init__(self, interval: int = ..., tz: str | datetime.tzinfo | None = ...) -> None: ...
    def set_axis(self, axis: Axis | _DummyAxis | _AxisWrapper | None) -> None: ...
    def __call__(self) -> list[float]: ...
    def tick_values(self, vmin: float, vmax: float) -> Sequence[float]: ...
    def _get_unit(self) -> float: ...
    def _get_interval(self) -> int: ...

# --- Converter Classes ---

class DateConverter(ConversionInterface):
    def __init__(self, *, interval_multiples: bool = ...) -> None: ...
    @staticmethod
    def axisinfo(unit: datetime.tzinfo | None, axis: Axis) -> None: ...
    @staticmethod
    def convert(obj: datetime.datetime | datetime.date | float | np.datetime64 | Sequence[datetime.datetime | datetime.date | float | np.datetime64],
                unit: datetime.tzinfo | None, axis: Axis) -> float | np.ndarray: ...
    @staticmethod
    def default_units(x: datetime.datetime | datetime.date | float | np.ndarray | Sequence[datetime.datetime | datetime.date | float | np.datetime64],
                      axis: Axis) -> None: ...


class ConciseDateConverter(DateConverter):
    def __init__(self, formats: list[str] | None = ..., zero_formats: list[str] | None = ...,
                 offset_formats: list[str] | None = ...,
                 show_offset: bool = ..., *, interval_multiples: bool = ...) -> None: ...
    @staticmethod
    def axisinfo(unit: datetime.tzinfo | None, axis: Axis) -> None: ...


class _SwitchableDateConverter:
    @staticmethod
    def _get_converter() -> "ConciseDateConverter" | "DateConverter": ...
    @staticmethod
    def axisinfo(unit: datetime.tzinfo | None, axis: Axis) -> AxisInfo: ...
    @staticmethod
    def default_units(x: datetime.datetime | datetime.date | float | np.ndarray | Sequence[datetime.datetime | datetime.date | float | np.datetime64],
                      axis: Axis) -> datetime.tzinfo | None: ...
    @staticmethod
    def convert(value: datetime.datetime | datetime.date | float | np.datetime64 | Sequence[datetime.datetime | datetime.date | float | np.datetime64],
                unit: datetime.tzinfo | None, axis: Axis) -> float | np.ndarray: ...
