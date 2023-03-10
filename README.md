# **Word Graph Application**

This application finds the shortest path of words between two words that differ by only one letter. 
It has been implemented in Python, using a breadth-first search (BFS) algorithm.
The script outputs the shortest path to a specified output file.

## Installation

    1. Clone the repository:
        bash
    • $ git clone https://gitlab.nixdev.co/tkachuk/blue-prism-test-task.git
    2. Install the package 'build':
        bash
    • $ pip install build
    3. Make Python package:
        bash
    • $ python -m build
    4. Install the package:
        bash
    • $ pip install dist/word_graph-0.0.1-py3-none-any.whl

## Usage

To use the word-graph command-line tool, you must provide a dictionary file, a start word, 
an end word and a name of result file. 
The dictionary file must contain a list of words, with one word per line.

## Example:

        bash
    • $ word-graph dictionary.txt Fore Tree Result_file.txt

The above command finds the shortest path of words from the start word "fore" to the end word "tree", 
using the words contained in the "dictionary.txt" file. The result is saved in the "result_file.txt" file.

## Testing

You can run the unit tests using the following command:

        bash
    • $ python -m pytest

The tests are located in the tests/ directory.

## License

This project is licensed under the terms of the MIT license.

## Why the breadth-first search (BFS) algorithm?

I chose to use breadth-first search (BFS) algorithm because it is a good fit for finding the _shortest path_
between two nodes in an unweighted graph, where each edge has the same weight. 

In our case, the graph we are working with has four-letter words as nodes, and edges connecting 
nodes that differ by one letter, and we want to find the shortest path between two given 
nodes (start_word and end_word) that passes through other nodes (all words from dictionary file) that also exist in the graph.
BFS explores all the neighbors of a node before moving to the next level, 
and this ensures that the shortest path is found.

BFS is also relatively simple to implement and has a time complexity of O(|V| + |E|), 
where |V| is the number of nodes in the graph and |E| is the number of edges. 
Since the number of nodes in our graph is relatively small, BFS should be fast enough for our purposes.

Excluded algorithms:

* DFS (Depth-First Search) is not a good algorithm for finding the shortest path in a graph.
* Dijkstra's algorithm requires more memory and computational resources than BFS.
* BDS (Bidirectional Search) is a variation of BFS where the search is performed from both the start and end nodes 
until they meet in the middle. 
This can be more efficient than BFS in some cases. However, in our case, the graph is relatively small, and the branching factor is small (we are working with four-letter words). 
Therefore, the improvement gained by using BDS may not be significant 
but BDS requires the additional overhead in terms of memory usage.
* A* (A-star) is a more complex algorithm that uses heuristics to guide the search towards the goal node. 
It is typically used in weighted graphs, where the edges have different weights, 
and finding the shortest path may involve exploring a large number of nodes.
