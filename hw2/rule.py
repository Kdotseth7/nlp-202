class Rule:
    """A class to represent a rule in a grammar.

    A rule has a left-hand side (LHS) and a right-hand side (RHS).

    Attributes:
        left (str): The LHS of the rule.
        right (str): The RHS of the rule.
    """

    def __init__(self, left: str, right: str) -> None:
        """Initialize the rule with its LHS and RHS.

        Args:
            left (str): The LHS of the rule.
            right (str): The RHS of the rule.
        """
        self.left = left
        self.right = right
