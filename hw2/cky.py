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
            # Add non-terminals for each terminal to cell
            cell = grammar.bottom_up_map[words[j]]
            cky_matrix[j][j] = cell
            
            # go through every previous position
            for i in reversed(range(j)):
                sub_entry_set = set()

                # go through every possible combination
                # in the interval from i to j
                for k in range(i, j):
                    # left
                    row_set = cky_matrix[i][k]
                    # right
                    col_set = cky_matrix[k + 1][j]
                    # get the cross of 2 set in order to get all combinations of sub-constituents
                    cross_set = list(itertools.product(row_set, col_set))

                    for left, right in cross_set:
                        sub_constituent = f"{left} {right}"
                        # check if the rule exist
                        if sub_constituent in grammar.bottom_up_map.keys():
                            sub_entry_set = sub_entry_set.union(
                                grammar.bottom_up_map[sub_constituent]
                            )
                # put all possible entries in to the table
                cky_matrix[i][j] = sub_entry_set
            
            
        return cky_matrix
    
    def pcfg_cky(words, grammar) -> None:
        pass