class Grammar:
    def __init__(self, rules) -> None:
        # Map from RHS to LHS for Bottom-Up Parsing
        self.bottom_up_map = dict()
        for rule in rules:
            self.bottom_up_map[rule.right] = set([rule.left]) if rule.right not in self.bottom_up_map else self.bottom_up_map[rule.right].union(set([rule.left]))
            