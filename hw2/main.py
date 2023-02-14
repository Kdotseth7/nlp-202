import optparse
from rule import Rule
from grammar import Grammar
from tabulate import tabulate
from cky import CKY

optparser = optparse.OptionParser()
optparser.add_option("--cky", dest="cky", action="store_true", help="Use CKY algorithm for parsing")
optparser.add_option("--pcfg-cky", dest="pcfg_cky", action="store_true", help="Use PCFG CKY algorithm for parsing")
(opts, _) = optparser.parse_args()

def run_cky():
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
    # for i in rules:
    #     print(f"{i.left} -> {i.right}")
        
    grammar = Grammar(rules)
    print(f"Top-Down: {grammar.top_down_map}")
    print(f"Bottom-Up: {grammar.bottom_up_map}")
    
    sentence = "British left waffles on Falklands"
    words = sentence.split(" ")
    
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
