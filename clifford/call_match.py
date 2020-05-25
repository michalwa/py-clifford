from typing import List, Dict, Optional, Callable
from .utils import loose_bool


# typedef
StrConstructor = Callable[[str], object]


class CallMatchFail(Exception):
    '''
    Raised by syntax tree nodes when matching fails in an expected way
    '''

class CallMatchError(Exception):
    '''
    Raised by syntax tree nodes when matching fails unexpectedly
    (because of a mistake in the call or the syntax)
    '''


class CallMatcher:
    def __init__(self, case_sensitive: bool = True):
        self._types = {}  # type: Dict[str, StrConstructor]
        self.case_sensitive = case_sensitive
        
        self.register_type(str)
        self.register_type(int)
        self.register_type(float)
        self.register_type(loose_bool, 'bool')

    def register_type(self, constructor: StrConstructor, name: Optional[str] = None):
        if name is None:
            name = constructor.__name__
        self._types[name] = constructor

    def get_type(self, name: str) -> StrConstructor:
        if not name in self._types:
            raise CallMatchError(f"Undefined type '{name}'")
        return self._types[name]

    def compare_literal(self, a: str, b: str) -> bool:
        if self.case_sensitive:
            return a == b
        else:
            return a.lower() == b.lower()


class CallMatch:
    def __init__(self):
        self.tokens = None  # type: Optional[List[str]]
        self.score = 0
        self._params = {}  # type: Dict[str, object]
        self._opts = []  # type: List[bool]
        self._vars = []  # type: List[int]

    def update(self, other: 'CallMatch') -> None:
        self.score += other.score
        self._params.update(other._params)
        self._opts += other._opts
        self._vars += other._vars

    def append_opt(self, present: bool) -> None:
        self._opts.append(present)

    def opt(self, index: int) -> bool:
        return self._opts[index]

    def append_var(self, variant: int) -> None:
        self._vars.append(variant)

    def var(self, index: int) -> int:
        return self._vars[index]

    def __getitem__(self, index):
        return self._params[index] if index in self._params else None

    def __setitem__(self, index, value):
        self._params[index] = value

    def __str__(self) -> str:
        return f'params: {self._params}, optionals: {self._opts}, variants: {self._vars}'
