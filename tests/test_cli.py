"""Tests for CLI."""

import pytest
from b3_mat.cli import main


def test_cli_help(capsys):
    with pytest.raises(SystemExit):
        main()
    captured = capsys.readouterr()
    assert "usage" in captured.err


def test_cli_invalid_file():
    import sys
    from io import StringIO
    old_argv = sys.argv
    sys.argv = ["b3_mat", "-f", "nonexistent.txt"]
    try:
        with pytest.raises(SystemExit):
            main()
    finally:
        sys.argv = old_argv
