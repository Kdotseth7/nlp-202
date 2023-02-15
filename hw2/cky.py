import itertools

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
                    cartesian_product = itertools.product(row_set, col_set)
                    cartesian_product_tuple = tuple(cartesian_product)

                    for (left, right) in cartesian_product_tuple:
                        sub_constituent = left + " " + right
                        # If the sub-constituent is in the grammar, add it to the set
                        if sub_constituent in grammar.bottom_up_map:
                            sub_constituent_set = sub_constituent_set.union(grammar.bottom_up_map[sub_constituent])
                # Add the set of sub-constituents to the cell
                cky_matrix[i][j] = sub_constituent_set
            
        return cky_matrix
    
    def pcfg_cky(words, grammar) -> None:
        pass