"""
This application finds the shortest path of words between two words that differ by only one letter.
It has been implemented in Python, using a breadth-first search (BFS) algorithm.
The script outputs the shortest path to a specified output file.
"""

import argparse
import json
import logging
from typing import List, Set, Optional


class WordGraphFinder:
    """
    The WordGraphFinder class reads a file containing a list of words,
    generates all possible next words of a given word by changing one letter at a time,
    and finds the shortest path between a start word and an end word by performing a BFS.
    """

    def __init__(self, words: str, start_word: str, end_word: str, possible_words: dict):
        self.words = words
        self.start_word = start_word
        self.end_word = end_word
        self.possible_words = possible_words

    def get_next_words(self, word: str) -> Set[str]:
        """
        Get all possible next words of a given word from self.possible_words variable.
        In case all possible next words didn't count before call generate_next_words func
        Args:
            word: The word to get next words from.
        """

        if word in self.possible_words:
            return self.words.intersection(self.possible_words[word])

        return self.generate_next_words(word)

    def generate_next_words(self, word: str) -> Set[str]:
        """
        Generates all possible next words of a given word by changing one letter at a time.
        Add only the words contained in the input file.
        Save all possible next words to self.possible_words variable.
        Args:
            word: The word to generate next words from.
        Returns:
            A set containing all possible next words of the given word.
        """

        next_words = set()
        possible_words = []
        for i in range(len(word)):
            for j in range(ord('a'), ord('z') + 1):
                next_word = word[:i] + chr(j) + word[i + 1:]
                possible_words.append(next_word)
                if next_word in self.words and next_word != word:
                    next_words.add(next_word)
        self.possible_words[word] = possible_words
        return next_words

    def find_shortest_path(self) -> Optional[List[str]]:
        """
        Finds the shortest path from the start word to the end word by performing a BFS.
        Returns:
            A list of words representing the shortest path from the start word to the end word.
        """

        visited = set([self.start_word])
        queue = [[self.start_word]]

        while queue:
            path = queue.pop(0)
            last_word = path[-1]

            if last_word == self.end_word:
                return path
            next_words = self.get_next_words(last_word) - visited
            for next_word in next_words:
                visited.add(next_word)
                queue.append(path + [next_word])
        return None


class WordGraphCli:
    """
    The WordGraphCli class implements the command-line interface
    and parses the command-line arguments using argparse, contains logger,
    save the shortest path between a start word and an end word to a specified output file
    also saves all possible next words to  "possible_words.txt" file.
    """

    # name of json file that contains dictionary with all possible next words
    possible_words_file = "possible_words.json"

    def __init__(self):
        """
        This method sets up an argparse ArgumentParser object and adds arguments for the name
        of the dictionary file, the start word, the end word, and the name of the file to save
        the result.
        """

        self.parser = argparse.ArgumentParser(
            description="Find the shortest path of words between two words"
                        " that differ by only one letter.")
        self.parser.add_argument(
            "dictionary_file", help="The file name of a text file containing words",
        )
        self.parser.add_argument("start_word", help="A word contained in the dictionary file")
        self.parser.add_argument("end_word", help="A word contained in the dictionary file")
        self.parser.add_argument(
            "result_file", help="The file name of a text file that will contain the result"
        )

        # self.args = self.parser.parse_args()

    def read_words(self, dictionary_file: str) -> Set[str]:
        """Read words from the specified file and returns them as a set.
        Returns:
            A set containing the words from the file,
            each word converted to lowercase and stripped of any whitespace.
        """

        with open(dictionary_file, "r") as file:
            words = set(line.strip().lower() for line in file)
        return words

    def read_possible_words(self) -> dict[list]:
        """
        Read all possible next words of a given word from json "possible_words.txt" file
        and returns them as a dict.
        Returns:
            A dictionary, where each key is a word and each value is a list
            of all possible next words of a given word by changing one letter at a time.
        """

        try:
            with open(self.possible_words_file, "r") as file:
                possible_words = json.load(file)
        except FileNotFoundError:
            possible_words = {}
        return possible_words

    def save_words(self, path: list[str], result_file: str) -> None:
        """
        Saves the given list of words to the specified file
        Args:
            path (List[str]): The list of words to save to the file.
        """

        with open(result_file, 'w') as file:
            for word in path:
                file.write(word + '\n')

    def save_possible_words(self, possible_words: dict[list]) -> None:
        """
        Saves the given dict of possible words to the file specified in the constructor.
        Args:
            possible_words (Dict[list]])
        """

        with open(self.possible_words_file, "w") as file:
            json.dump(possible_words, file)

    def run(self):
        """
        Runs the word graph program.

        This method sets up logging. It also reads previously saved possible words.
        Creates a WordGraphFinder object and finds the shortest path between words.
        Saves the words to the output file and any new possible words.
        """

        args = self.parser.parse_args()

        logging.basicConfig(level=logging.INFO)

        words = self.read_words(args.dictionary_file)
        start_word = args.start_word.lower()
        end_word = args.end_word.lower()
        possible_words = self.read_possible_words()

        word_graph = WordGraphFinder(words, start_word, end_word, possible_words)

        if start_word not in words:
            logging.info(f"'{start_word}' is not contained in the source file.")
            return

        if end_word not in words:
            logging.info(f"'{args.end_word}' is not contained in the source file.")
            return

        path = word_graph.find_shortest_path()
        if path:
            self.save_words(path, args.result_file)
        else:
            logging.info(f"No path from '{args.start_word}' to '{args.end_word}' found. "
                         f"Output file not created")

        self.save_possible_words(word_graph.possible_words)


def main():
    """This function is setuptools entrypoint."""
    cli = WordGraphCli()
    cli.run()


if __name__ == "__main__":
    main()
