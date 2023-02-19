class Grammar:
    def __init__(self, rules) -> None:
        # Map from RHS to LHS for Bottom-Up Parsing
        self.bottom_up_map = dict()
        # If Grammar is CFG
        if rules[0].__class__.__name__ == "Rule":
            for rule in rules:
                self.bottom_up_map[rule.right] = set([rule.left]) if rule.right not in self.bottom_up_map else self.bottom_up_map[rule.right].union(set([rule.left]))
        # If Grammar is PCFG
        else:
            for rule in rules:
                self.bottom_up_map[rule.right] = set([(rule.left, rule.prob)]) if rule.right not in self.bottom_up_map else self.bottom_up_map[rule.right].union(set([(rule.left, rule.prob)]))
            