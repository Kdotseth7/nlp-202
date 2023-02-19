import optparse

from rule import Rule, Pcfg_Rule
from grammar import Grammar
from tabulate import tabulate
from cky import CKY
from tree import print_tree, marginalize_trees

# Parse command-line arguments
optparser = optparse.OptionParser()
optparser.add_option("--cky", dest="cky", action="store_true", help="Use CKY algorithm for parsing")
optparser.add_option("--wcky", dest="wcky", action="store_true", help="Use Weighted CKY algorithm for parsing")
(opts, _) = optparser.parse_args()

def run_cky():
    # Rules in Chomsky Normal Form(CNF)
    rules = [   
        Rule("S", "NP VP"),
        Rule("NP", "JJ NP"),
        Rule("VP", "VP NP"),
        Rule("VP", "VP PP"),
        Rule("PP", "P NP"),
        Rule("NP", "British"),
        Rule("JJ", "British"),
        Rule("NP", "left"),
        Rule("VP", "left"),
        Rule("NP", "waffles"),
        Rule("VP", "waffles"),
        Rule("P", "on"),
        Rule("NP", "Falklands")
    ]
    # Grammar: A set of rules
    grammar = Grammar(rules)
    
    # Sentence to parse
    sentence = "British left waffles on Falklands"
    # Split the sentence into words
    words = sentence.split(" ")
    
    # Perform CKY parsing on the sentence
    cky_table = CKY.cky(words, grammar)
    print("CKY Table:")
    print(tabulate(cky_table, headers=words, tablefmt="fancy_grid", showindex="always"))


def run_wcky():
    # Rules in Chomsky Normal Form(CNF) with probabilities
    rules = [
        Pcfg_Rule("S", "NP VP", 1.0),
        Pcfg_Rule("PP", "P NP", 1.0),
        Pcfg_Rule("VP", "V NP", 0.7),
        Pcfg_Rule("VP", "VP PP", 0.3),
        Pcfg_Rule("P", "with", 1.0),
        Pcfg_Rule("V", "saw", 1.0),
        Pcfg_Rule("NP", "NP PP", 0.4),
        Pcfg_Rule("NP", "astronomers", 0.4),
        Pcfg_Rule("NP", "ears", 0.18),
        Pcfg_Rule("NP", "saw", 0.04),
        Pcfg_Rule("NP", "stars", 0.18),
        Pcfg_Rule("NP", "telescopes", 0.1)
    ]
    # Grammar: A set of rules
    grammar = Grammar(rules)
    
    # Sentence to parse
    sentence = "astronomers saw stars with ears"
    # Split the sentence into words
    words = sentence.split(" ")

    # Perform PCFG CKY parsing on the sentence
    wcky_tables, parse_trees = CKY.weighted_cky(words, grammar)
    best_tree = max(parse_trees, key=lambda node: node.score)
    print("Weighted CKY Table:")
    print(tabulate(wcky_tables, headers=words, tablefmt="fancy_grid", showindex="always"))
    
    # Pretty print the best tree
    print("Most Probable Parse Tree:")
    print_tree(best_tree)
    
    # Marginalize over all results trees
    print(f"Probability of Sentence: {marginalize_trees(parse_trees)}")


if __name__ == "__main__":
    if opts.cky:
        run_cky()
    elif opts.wcky:
        run_wcky()
    else:
        raise NotImplementedError("Please specify an algorithm to use for parsing")
