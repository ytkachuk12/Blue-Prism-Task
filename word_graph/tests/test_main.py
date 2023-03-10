"""Tests."""

import argparse
import pytest
import logging
from unittest import mock
from word_graph.main import WordGraphFinder, WordGraphCli


@pytest.mark.parametrize(
    "words, start_word, end_word, expected",
    [
        (
                {"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"},
                "fore", "tree", ["fore", "tore", "trre", "tree"]
        ),
        (
                {"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"},
                "fore", "flee", ["fore", "tore", "trre", "tree", "free", "flee"]
        ),
        (
                {"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}, "four", "four",
                ["four"]),
        ({"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}, "four", "tree", None),
    ],
)
def test_find_shortest_path(words, start_word, end_word, expected):
    """
    Test the find_shortest_path method of the WordGraphFinder class.
    Args:
        words: Set of words.
        start_word: The start word for the sequence.
        end_word: The end word for the sequence.
        expected: The expected result of the sequence.
    """
    finder = WordGraphFinder(words, start_word, end_word, {})
    actual = finder.find_shortest_path()

    assert actual == expected


@pytest.mark.parametrize("words, word, expected", [
    ({"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}, "tree", {"trre", "free"}),
    ({"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}, "trre",
     {"tore", "tree", "tire"}),
    ({"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}, "four", set())
])
def test_generate_next_words(words, word, expected):
    """
    Test the generate_next_words method of the WordGraphFinder class.
    Args:
        words: Set of words.
        word: The word to generate next words from.
        expected: The expected result of the sequence.
    """

    finder = WordGraphFinder(words, "word", "word", {})
    actual = finder.generate_next_words(word)

    assert actual == expected


@pytest.mark.parametrize('words, word, possible_words, expected', [
    (
            {"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}, "tree",
            {"tree": [
                "aree", "bree", "cree", "dree", "eree", "free", "gree", "hree", "iree", "jree",
                "kree", "lree", "mree", "nree", "oree", "pree", "qree", "rree", "sree", "tree",
                "uree", "vree", "wree", "xree", "yree", "zree", "taee", "tbee", "tcee", "tdee",
                "teee", "tfee", "tgee", "thee", "tiee", "tjee", "tkee", "tlee", "tmee", "tnee",
                "toee", "tpee", "tqee", "tree", "tsee", "ttee", "tuee", "tvee", "twee", "txee",
                "tyee", "tzee", "trae", "trbe", "trce", "trde", "tree", "trfe", "trge", "trhe",
                "trie", "trje", "trke", "trle", "trme", "trne", "troe", "trpe", "trqe", "trre",
                "trse", "trte", "true", "trve", "trwe", "trxe", "trye", "trze", "trea", "treb",
                "trec", "tred", "tree", "tref", "treg", "treh", "trei", "trej", "trek", "trel",
                "trem", "tren", "treo", "trep", "treq", "trer", "tres", "tret", "treu", "trev",
                "trew", "trex", "trey", "trez"]},
            {"trre", "free"}
    )
])
def test_get_next_words(words, word, possible_words, expected):
    """
    Test the get_next_words method of the WordGraphFinder class.
    Args:
        words: Set of words.
        word: The word to generate next words from.
        possible_words: All possible next words of a given word by changing one letter at a time
        expected: The expected result of the sequence.
    """

    finder = WordGraphFinder(words, "word", "word", possible_words)
    actual = finder.generate_next_words(word)

    assert actual == expected


@pytest.fixture
def words_file(tmp_path) -> str:
    """
    Create a temporary file with a predefined set of words.
    Args:
        tmp_path: A pytest built-in fixture that provides a temporary path.
    Returns:
        str: The path to the temporary file.
    """
    # Define the content of the file
    content = "four\ntire\ntree\nfree\nflee\nfore\ntore\ntrre\n"

    # Write the content to a temporary file
    file_path = tmp_path / "words.txt"
    file_path.write_text(content)

    return file_path


@pytest.fixture
def cli(words_file):
    return WordGraphCli()


def test_read_words(words_file, cli):
    """
    Test that the read_words function correctly reads the words from the given file.
    Args:
        words_file (str): Temp path to the file containing the words.
        cli (WordGraphCli): An instance of the WordGraphCli class.
    """

    words = cli.read_words(words_file)

    assert words == {"four", "tire", "tree", "free", "flee", "fore", "tore", "trre"}


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(dictionary_file="dict_file.txt", start_word="start_word",
                                            end_word="end", kwarg4="output.txt"))
def test_start_word_in_file(mock_args, caplog, cli):
    """
    Test that the run method logs an error message when the start word is not in the source file.
    Args:
        mock_args (Mock): A mock object representing the command-line arguments.
        caplog (pytest.LogCaptureFixture): A fixture provided by pytest to capture log messages.
        cli (WordGraphCli): An instance of the WordGraphCli class.
    """

    with caplog.at_level(logging.INFO):
        cli.run()

    assert "'start_word' is not contained in the source file." in caplog.text


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(dictionary_file="dict_file.txt", start_word="Spin",
                                            end_word="end_word", kwarg4="output.txt"))
def test_end_word_in_file(mock_args, caplog, cli):
    """
    Test that the run method logs an error message when the end word is not in the source file.
    Args:
        mock_args (Mock): A mock object representing the command-line arguments.
        caplog (pytest.LogCaptureFixture): A fixture provided by pytest to capture log messages.
        cli (WordGraphCli): An instance of the WordGraphCli class.
    """

    with caplog.at_level(logging.INFO):
        cli.run()

    assert "'end_word' is not contained in the source file." in caplog.text


@mock.patch('argparse.ArgumentParser.parse_args',
            return_value=argparse.Namespace(dictionary_file="dict_file.txt", start_word="Spin",
                                            end_word="Tree", kwarg4="output.txt"))
def test_no_path(mock_args, caplog, cli):
    """
    Test that the run method logs an error message when there is no path
    between the start and end words.
    Args:
        mock_args (Mock): A mock object representing the command-line arguments.
        caplog (pytest.LogCaptureFixture): A fixture provided by pytest to capture log messages.
        cli (WordGraphCli): An instance of the WordGraphCli class.
    """

    with caplog.at_level(logging.INFO):
        cli.run()

    assert "No path from 'Spin' to 'Tree' found. " in caplog.text
