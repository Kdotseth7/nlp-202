class Grammar:
    def __init__(self, rules) -> None:
        # Top-down Parsing
        self.top_down_map = dict()
        # Bottom-up Parsing
        self.bottom_up_map = dict()
        for rule in rules:
            self.top_down_map[rule.left] = set([rule.right]) if rule.left not in self.top_down_map else self.top_down_map[rule.left].union(set([rule.right]))
            self.bottom_up_map[rule.right] = set([rule.left]) if rule.right not in self.bottom_up_map else self.bottom_up_map[rule.right].union(set([rule.left]))
            