from typing import TypeVar, Type, Optional, Dict, Callable


class StrBuffer:
    """Accumulates a string and allows various operations on it. Mainly used in
    lexers."""

    def __init__(self):
        self._buffer = ''

    def flush(self) -> str:
        """Empties the buffer and returns its current contents.

        Returns
        -------
          * `str`: The current contents of the buffer (before emptying)
        """

        temp, self._buffer = self._buffer, ''
        return temp

    def trim(self, start: int = 0, end: Optional[int] = None):
        """Trims the buffer to the desired range.

        Parameters
        ----------
          * start: `int` (optional) - The index of the first character of the
            desired substring. Defaults to 0.
          * end: `int` (optional) - The exclusive index of the end of the
            desired substring. Defaults to None.
        """

        if end is None:
            self._buffer = self._buffer[start:]
        else:
            self._buffer = self._buffer[start:end]

    def __iadd__(self, seq: str) -> 'StrBuffer':
        self._buffer += seq
        return self

    def __str__(self) -> str:
        return self._buffer

    def __eq__(self, other) -> bool:
        return any([
            self is other,
            self._buffer == other,
            isinstance(other, self.__class__) and self._buffer == other._buffer
        ])


def loose_bool(s: str) -> bool:
    """Tries to 'loosely' convert the given string to a boolean. This is done
    by first attempting to parse it into a number, then to a boolean. If this
    fails, a set of pre-defined words is compared case-insensitively to the
    string to determine whether it's positive/affirmative or negative.

    Parameters
    ----------
      * s: `str` - The string to convert.

    Returns
    -------
      * `bool`: The resulting boolean.

    Raises
    ------
      * `ValueError` when the boolean value can't be determined.
    """

    s = s.strip()

    try:
        f = float(s)
        return bool(f)
    except ValueError:
        pass

    s = s.lower()
    if s in ['y', 'yes', 't', 'true', 'do', 'ok', 'sure', 'alright']:
        return True
    elif s in ['n', 'no', 'f', 'false', 'dont']:
        return False

    else:
        raise ValueError(f"String '{s}' cannot be loosely casted to a boolean")


def dict_get_lazy(dict: Dict, key, fn_default: Callable):
    return dict[key] if key in dict else fn_default()


_T = TypeVar('_T')


def instance_or_kwargs(obj, cls: Type[_T]) -> _T:
    """Returns the object unchanged if it's an instance of the given class.
    Otherwise, if it is a dictionary, an instance of the given class is constructed
    with the object as keyword args to the constructor.

    Parameters
    ----------
      * obj - The object to cast.
      * cls: `Type[_T]` - The class to cast to.

    Returns
    -------
      * `_T`: The instance of the given class.

    Raises
    ------
      * `TypeError` when the object is neither an instance of the given class
        nor a dictionary.
    """

    if isinstance(obj, cls):
        return obj
    elif type(obj) is dict:
        return cls(**obj)
    else:
        raise TypeError(f"{obj} is neither an instance of {cls} nor a dictionary")
