import parsy
import pytest

from waterloo.parsers.napoleon import (
    args_parser,
    args_head,
    arg_type,
    rest_of_line,
    ignored_line,
)


def test_args_head():
    # TODO permutations of leading whitespace and Kwargs etc
    example = """Args:
"""
    result = args_head.parse(example)
    assert result == 'Args'

    no_newline = """Args:"""
    with pytest.raises(parsy.ParseError):
        args_head.parse(no_newline)


@pytest.mark.parametrize('example', [
    "key (str): identifying a specific token bucket",
    "key (str): ",
    "key (str):",
    "key (str)",
])
def test_arg_type(example):
    parser = arg_type << rest_of_line
    result = parser.parse(example)
    assert result == {
        'arg': 'key',
        'type': 'str',
    }


@pytest.mark.parametrize('example', [
    "\n",
    "Builds JSON blob to be stored in the paypal_log column\n",
    "        Builds JSON blob to be stored in the paypal_log column\n",
    "of engine_purchasetransaction. The Args: don't start here.\n",
    "        of engine_purchasetransaction. The Args: don't start here.\n",
    "Args: aren't here either.\n",
    "        Args: aren't here either.\n",
])
def test_ignored_line(example):
    result = ignored_line.parse(example)
    assert result == ""


def test_ignored_lines():
    example = """
    Builds JSON blob to be stored in the paypal_log column
    of engine_purchasetransaction. The Args: don't start here.
    Args: aren't here either.

    Args:
        key (str): identifying a specific token bucket
"""
    parser = ignored_line.many()
    result, remainder = parser.parse_partial(example)
    assert result == [""] * 5
    assert remainder == """    Args:
        key (str): identifying a specific token bucket
"""


@pytest.mark.skip
def test_parser():
    example = """
        Will block thread until `num_tokens` could be consumed from token bucket `key`.

        Args:
            key (str): identifying a specific token bucket
            num_tokens (int): will block without consuming any tokens until
                this amount are availabe to be consumed
            timeout (int): seconds to block for
            retry_interval (Optional[float]): how long to wait between polling
                for tokens to be available. `None` means use default interval
                which is equal to time needed to replenish `num_tokens`.

        Returns:
            bool: whether we got the requested tokens or not
                (False if timed out)
        """
    expected_args = {
        'key': 'str',
        'num_tokens': 'int',
        'timeout': 'int',
        'retry_interval': 'Optional[float]',
    }

    result = args_parser.parse(example)
    assert result == expected_args
