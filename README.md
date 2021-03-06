# cliffs
This is an implementation of [Clifford](https://github.com/michalwa/Clifford)
(originally written in Java) for Python 3.9.
Although this implementation has much more functionality,
it's still compliant with the original concept.

**Clifford** is a command parsing utility useful for creating internal
command line interfaces for your applications. Its syntax specification method
allows command definitions and usage help to be united with a single syntax.
This way usage specification can be directly used to generate command parsers.

The advantage of this method is that it makes it possible to avoid long chained
method calls for constructing command parsers, as it is usually done in libraries.

## Syntax
**Clifford** uses a rather intuitive syntax to specify the syntax of commands:
- `literals` specify required terms that the command call must contain
  in order to match the specification
- `<parameters>` accept a single token in the command call and store its value
  for processing by the command handler; parameters can also specify types
  (`<param: type>`) which their values will be validated for and parsed into
- `<varargs*>` will collect any remaining tokens and store them as a list
- `<tails...>` will collect any remaining tokens after all previous elements
  as raw text
- `(variant|groups)` encapsulate sequences of elements and accept only one of
  those sequences (index of the present sequence is stored for processing by the handler)
- `[optional sequences]` may or may not be present in the command call
  (boolean indicating presence is stored for processing by the handler)
- `{unordered groups}` whose elements can be present in an arbitrary order

## Example
To demonstrate the concept of how **Clifford** works, consider this simple command syntax
specification:

    set [loud] alarm at <hour: int> [am|pm] [every <days>] [saying <message>]

Such defined syntax accepts the following command calls:

    set alarm at 9 am
        opts = [False, True, False, False]
        vars = [0]
        params = {'hour': '9'}

    set loud alarm at 7 every monday
        opts = [True, False, True, False]
        params = {'hour': 7, 'days': 'monday'}

    set alarm at 2 pm every monday saying 'Hello, world!'
        opts = [False, True, True, True]
        vars = [1]
        params = {'hour': 2, 'days': 'monday', 'message': 'Hello, world!'}

And will reject the following with appropriate info:

    set alarm          (Expected literal 'at')
    set loud alarm at  (Expected argument for parameter <hour>)
    set alarm at pm    (Argument 'pm' for parameter <hour> does not match type int)
    ...

For more syntax features and implementation details check out the [example](example.py).
