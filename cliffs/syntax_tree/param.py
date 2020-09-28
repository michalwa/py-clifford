from typing import List, Optional
from .node import Leaf
from ..token import Token
from ..call_match import *
from ..call_matcher import CallMatcher


class Parameter(Leaf):
    """A command parameter.

    Any token present in place of the parameter will be stored as the value
    of that parameter in the match.

    Parameters may also specify types that will be checked upon matching.
    """

    node_name = 'parameter'

    def __init__(self, name: str, typename: Optional[str] = None):
        """Initializes a parameter node.

        Parameters
        ----------
          * name: `str` - The name of the parameter.
          * typename: `str` (optional) - The name of the type to parse. Defaults to string.
        """

        super().__init__()
        self.name = name
        self.typename = typename

    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__) \
            and self.name == other.name \
            and self.typename == other.typename

    def __str__(self) -> str:
        if self.typename is None:
            return f'<{self.name}>'
        else:
            return f'<{self.name}: {self.typename}>'

    def __repr__(self) -> str:
        return f'param {repr(self.name)}'

    def match(self, match: CallMatch, matcher: CallMatcher):
        super().match(match, matcher)

        if not match.has_tokens():
            raise CallMatchFail(f"Expected argument for parameter <{self.name}>")

        # Type construction
        if self.typename is not None:
            try:
                value = matcher.parse_arg(self.typename, match.tokens[0].value)
            except ValueError:
                raise CallMatchFail(f"Argument {match.tokens[0]} for parameter <{self.name}> "
                                    f"does not match type {self.typename}")

        # Type defaults to string
        else:
            value = match.tokens[0].value

        match[self.name] = value
        match.score += 0.5
        match.take_tokens(1)
