import datetime
import numpy as np
from typing import Any, Callable, Dict, List, Sequence

from .axis import Axis
from .projections.polar import _AxisWrapper
from .ticker import _DummyAxis, Formatter, Locator
from .units import AxisInfo, ConversionInterface


# --- Global Functions ---

def _get_tzinfo(tz: str | datetime.tzinfo | None = ...) -> datetime.tzinfo: ...

def _reset_epoch_test_example() -> None: ...

def set_epoch(epoch: str) -> None: ...

def get_epoch() -> str: ...

def _dt64_to_ordinalf(d: np.datetime64 | np.ndarray) -> float | np.ndarray: ...

def _from_ordinalf(x: float, tz: str | datetime.tzinfo | None = ...) -> datetime.datetime: ...

def datestr2num(d: str | Sequence[str], default: datetime.datetime | None = ...) -> float | np.ndarray: ...

def date2num(d: datetime.datetime | np.datetime64 | Sequence[datetime.datetime | np.datetime64]) -> float | np.ndarray: ...

def num2date(x: float | Sequence[float], tz: str | datetime.tzinfo | None = ...) -> datetime.datetime | list[datetime.datetime]: ...

def num2timedelta(x: float | Sequence[float]) -> datetime.timedelta | list[datetime.timedelta]: ...

def drange(dstart: datetime.datetime, dend: datetime.datetime, delta: datetime.timedelta) -> np.ndarray: ...

def _wrap_in_tex(text: str) -> str: ...

# --- Formatter Classes ---

class DateFormatter(Formatter):
    tz: str | datetime.tzinfo | None
    fmt: str
    _usetex: bool | None

    def __init__(self, fmt: str, tz: str | datetime.tzinfo | None = None, *, usetex: bool | None = None) -> None: ...
    def __call__(self, x: float, pos: int | None = 0) -> str: ...
    def set_tzinfo(self, tz: str | datetime.tzinfo | None) -> None: ...

class ConciseDateFormatter(Formatter):
    _locator: Locator
    _tz: str | datetime.tzinfo | None
    formats: List[str]
    zero_formats: List[str]
    offset_formats: List[str]
    offset_string: str
    show_offset: bool
    _usetex: bool | None

    def __init__(self, locator: Locator,
                 tz: str | datetime.tzinfo | None = None,
                 formats: Sequence[str] | None = None,
                 offset_formats: Sequence[str] | None = None,
                 zero_formats: Sequence[str] | None = None,
                 show_offset: bool = True,
                 *, usetex: bool | None = None) -> None: ...
    def __call__(self, x: float, pos: int | None = 0) -> str: ...
    def format_ticks(self, values: Sequence[float]) -> List[str]: ...
    def get_offset(self) -> str: ...
    def format_data_short(self, value: float) -> str: ...

class AutoDateFormatter(Formatter):
    _locator: Locator
    _tz: str | datetime.tzinfo | None
    defaultfmt: str
    _formatter: DateFormatter
    _usetex: bool | None
    scaled: dict

    def __init__(self, locator: Locator,
                 tz: str | datetime.tzinfo | None = None,
                 defaultfmt: str = '%Y-%m-%d',
                 *, usetex: bool | None = None) -> None: ...
    def _set_locator(self, locator: Locator) -> None: ...
    def __call__(self, x: float, pos: int | None = 0) -> str: ...

# --- rrulewrapper (assuming it's in rrule.py and this is its stub) ---
class rrulewrapper:
    def __init__(self, freq: int, tzinfo: datetime.tzinfo | None = None, **kwargs: Any) -> None: ...
    def set(self, **kwargs: Any) -> None: ...
    def _update_rrule(self, **kwargs: Any) -> None: ...
    def _attach_tzinfo(self, dt: datetime.datetime, tzinfo: datetime.tzinfo) -> datetime.datetime: ...
    def _aware_return_wrapper(self, f: Callable[..., Any], returns_list: bool = False) -> Callable[..., Any]: ...
    def __getattr__(self, name: str) -> Any: ...
    def __setstate__(self, state: dict) -> None: ...

# --- Locator Classes ---

class DateLocator(Locator):
    hms0d: dict[str, int]

    def __init__(self, tz: datetime.tzinfo | None = None) -> None: ...
    def set_tzinfo(self, tz: datetime.tzinfo | None) -> None: ...
    def datalim_to_dt(self) -> tuple[datetime.datetime, datetime.datetime]: ...
    def viewlim_to_dt(self) -> tuple[datetime.datetime, datetime.datetime]: ...
    def _get_unit(self) -> float: ...
    def _get_interval(self) -> int: ...
    def nonsingular(self, v0: float, v1: float) -> tuple[float, float]: ...

class RRuleLocator(DateLocator):
    def __init__(self, o: rrulewrapper, tz: datetime.tzinfo | None = None) -> None: ...
    def __call__(self) -> List[float]: ...
    def tick_values(self, vmin: float, vmax: float) -> List[float]: ...
    def _create_rrule(self, vmin: datetime.datetime, vmax: datetime.datetime) -> tuple[datetime.datetime, datetime.datetime]: ...
    def _get_unit(self) -> float: ...
    @staticmethod
    def get_unit_generic(freq: int) -> float: ...
    def _get_interval(self) -> int: ...

class AutoDateLocator(DateLocator):
    def __init__(self, tz: str | datetime.tzinfo | None = None, minticks: int = 5,
                 maxticks: int | Dict[int, int] | None = None,
                 interval_multiples: bool = True) -> None: ...
    def __call__(self) -> List[float]: ...
    def tick_values(self, vmin: float, vmax: float) -> List[float]: ...
    def nonsingular(self, v0: float, v1: float) -> tuple[float, float]: ...
    def _get_unit(self) -> float: ...
    def get_locator(self, dmin: datetime.datetime, dmax: datetime.datetime) -> RRuleLocator: ...


class YearLocator(RRuleLocator):
    def __init__(self, base: int = 1, month: int = 1, day: int = 1,
                 tz: str | datetime.tzinfo | None = None) -> None: ...
    def _create_rrule(self, vmin: datetime.datetime, vmax: datetime.datetime) -> tuple[datetime.datetime, datetime.datetime]: ...


class MonthLocator(RRuleLocator):
    def __init__(self, bymonth: int | List[int] | None = None,
                 bymonthday: int = 1, interval: int = 1,
                 tz: str | datetime.tzinfo | None = None) -> None: ...

class WeekdayLocator(RRuleLocator):
    def __init__(self, byweekday: int | List[int] = 1, interval: int = 1, tz: str | datetime.tzinfo | None = None) -> None: ...


class DayLocator(RRuleLocator):
    def __init__(self, bymonthday: int | List[int] | None = None, interval: int = 1, tz: str | datetime.tzinfo | None = None) -> None: ...


class HourLocator(RRuleLocator):
    def __init__(self, byhour: int | List[int] | None = None, interval: int = 1, tz: str | datetime.tzinfo | None = None) -> None: ...


class MinuteLocator(RRuleLocator):
    def __init__(self, byminute: int | List[int] | None = None, interval: int = 1, tz: str | datetime.tzinfo | None = None) -> None: ...


class SecondLocator(RRuleLocator):
    def __init__(self, bysecond: int | List[int] | None = None, interval: int = 1, tz: str | datetime.tzinfo | None = None) -> None: ...


class MicrosecondLocator(DateLocator):
    def __init__(self, interval: int = 1, tz: str | datetime.tzinfo | None = None) -> None: ...
    def set_axis(self, axis: Axis | _DummyAxis | _AxisWrapper | None) -> None: ...
    def __call__(self) -> List[float]: ...
    def tick_values(self, vmin: float, vmax: float) -> Sequence[float]: ...
    def _get_unit(self) -> float: ...
    def _get_interval(self) -> int: ...

# --- Converter Classes ---

class DateConverter(ConversionInterface):
    def __init__(self, *, interval_multiples: bool = True) -> None: ...
    @staticmethod
    def axisinfo(unit: datetime.tzinfo | None, axis: Axis) -> None: ...
    @staticmethod
    def convert(obj: datetime.datetime | datetime.date | float | np.datetime64 | Sequence[datetime.datetime | datetime.date | float | np.datetime64],
                unit: datetime.tzinfo | None, axis: Axis) -> float | np.ndarray: ...
    @staticmethod
    def default_units(x: datetime.datetime | datetime.date | float | np.ndarray | Sequence[datetime.datetime | datetime.date | float | np.datetime64],
                      axis: Axis) -> None: ...


class ConciseDateConverter(DateConverter):
    def __init__(self, formats: List[str] | None = None, zero_formats: List[str] | None = None,
                 offset_formats: List[str] | None = None,
                 show_offset: bool = True, *, interval_multiples: bool = True) -> None: ...
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
