import optparse
from rule import Rule
from grammar import Grammar
from tabulate import tabulate
from cky import CKY

# Parse command-line arguments
optparser = optparse.OptionParser()
optparser.add_option("--cky", dest="cky", action="store_true", help="Use CKY algorithm for parsing")
optparser.add_option("--pcfg-cky", dest="pcfg_cky", action="store_true", help="Use PCFG CKY algorithm for parsing")
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
    print("================================CKY Table================================")
    print(tabulate(cky_table, headers=words, tablefmt="fancy_grid", showindex="always"))


def run_pcfg_cky():
    pass


if __name__ == "__main__":
    if opts.cky:
        run_cky()
    elif opts.pcfg_cky:
        run_pcfg_cky()
    else:
        raise NotImplementedError("Please specify an algorithm to use for parsing")
