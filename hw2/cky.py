import numpy as np

from itertools import product
from tree import Node

class CKY:
    
    def cky(words, grammar) -> list[list[int]]:
        """Perform CKY parsing on a sentence.
    
        Args:
            words (list(str)): The words in the sentence.
            grammar (Grammar): The grammar to use for parsing.
    
        Returns:
            list(list): A table of the parses for the sentence.
        """
        # Initialize N X N table for the CKY algorithm
        cky_matrix = list()
        for i in range(len(words)):
            empty_strings = [""] * i
            empty_sets = [set()] * (len(words) - i)
            row = empty_strings + empty_sets
            cky_matrix.append(row)
            
        for j in range(len(words)):
            # Add non-terminals for each terminal to cell[j][j]
            cell = grammar.bottom_up_map[words[j]]
            cky_matrix[j][j] = cell
            
            # For each cell in the matrix, go through all possible combinations
            for i in reversed(range(j)):
                # Sub-Constituent Set is the set of all sub-constituents
                sub_constituent_set = set()

                for k in range(i, j):
                    # Row Set: cell[i][k]
                    row_set = cky_matrix[i][k]
                    # Col Set: cell[k + 1][j]
                    col_set = cky_matrix[k + 1][j]
                    # Cartesian (Cross) Product of row_set and col_set yields all combinations of sub-constituents
                    cartesian_product = product(row_set, col_set)
                    cartesian_product_tuple = tuple(cartesian_product)

                    for (left, right) in cartesian_product_tuple:
                        sub_constituent = left + " " + right
                        # If the sub-constituent is in the grammar, add it to the set
                        if sub_constituent in grammar.bottom_up_map:
                            sub_constituent_set = sub_constituent_set.union(grammar.bottom_up_map[sub_constituent])
                # Add the set of sub-constituents to the cell
                cky_matrix[i][j] = sub_constituent_set
            
        return cky_matrix
    
    
    def weighted_cky(words, grammar) -> tuple[list[list[tuple[str, Node]]], list[Node]]:
        """Perform Weighted CKY parsing on a sentence.
        
        Args: 
            words (list(str)): The words in the sentence.
            grammar (Grammar): The grammar to use for parsing.
            
        Returns:
            tuple[list[list[tuple[str, Node]]]: A table of the parses for the sentence.
            list[Node]]: A list of the trees for the sentence.
        """
        # Initialize N X N table for the Weighted CKY algorithm
        cky_matrix = list()
        for i in range(len(words)):
            empty_strings = [""] * i
            empty_sets = [set()] * (len(words) - i)
            row = empty_strings + empty_sets
            cky_matrix.append(row)
        
        # Initialize list of trees as empty
        tree_list = list()
            
        for j in range(len(words)):
            # Initialize set of entries for cell[j][j]
            cell = set()
            # Add non-terminals for each terminal to cell[j][j]
            for next_entry, prob in grammar.bottom_up_map.get(words[j], list()):
                # Create a node for each entry
                node = Node(next_entry, np.log(prob), left=None, right=None, word=words[j])
                # Add the entry and node to the cell
                cell.add((next_entry, node))
            cky_matrix[j][j] = cell
            
            # For each cell in the matrix, go through all possible combinations
            for i in reversed(range(j)):
                sub_constituent_set = set()

                for k in range(i, j):
                    # Left Set: cell[i][k]
                    row_set = cky_matrix[i][k]
                    # Right Set: cell[k + 1][j]
                    col_set = cky_matrix[k + 1][j]
                    # Cartesian (Cross) Product of row_set and col_set yields all combinations of sub-constituents
                    cartesian_product = product(row_set, col_set)
                    cartesian_product_tuple = tuple(cartesian_product)

                    for (left, right) in cartesian_product_tuple:
                        left_const, left_node = left
                        right_const, right_node = right
                        sub_constituent = left_const + " " + right_const
                        # If the sub-constituent is in the grammar, add it to the set
                        if sub_constituent in grammar.bottom_up_map:
                            for sub_const_entry, sub_const_prob in grammar.bottom_up_map[sub_constituent]:
                                sub_const_node = Node(sub_const_entry, np.log(sub_const_prob), left=left_node, right=right_node)
                                sub_entry_tuple = (sub_const_entry, sub_const_node)
                                sub_constituent_set.add(sub_entry_tuple)
                # Add the set of sub-constituents to the cell
                cky_matrix[i][j] = sub_constituent_set
        
        # Only add trees that have the root node as the start symbol(S)        
        for tag, root in cky_matrix[0][-1]:
            if tag == "S":
                tree_list.append(root)

        return cky_matrix, tree_list