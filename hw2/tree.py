import math

class Node:
    """
    Represents a node in a binary tree.
    """
    def __init__(self, non_terminal, log_prob, left, right, word=None):
        """
        Initializes a new instance of the Node class.

        Args:
            non_terminal (str): The non-terminal value of the node.
            log_prob (float): The log probability of the node.
            left (Node): The left child of the node.
            right (Node): The right child of the node.
            word (str, optional): The word value of the node. Defaults to None.
        """
        # Set the value of the node based on whether it is a leaf or not
        if word is None:
            self.value = non_terminal
        else:
            self.value = f"{non_terminal}-{word}"
        
        # Set the left and right child nodes
        self.left = left
        self.right = right

        # Set the score of the node based on the log probability of the node and its children
        if self.left is None:
            left_score = 0
        else:
            left_score = self.left.score
            
        if self.right is None:
            right_score = 0
        else:
            right_score = self.right.score
        
        self.score = log_prob + left_score + right_score
        
        # Calculate the probability of the node
        self.prob = math.exp(self.score)

    def __repr__(self):
        """
        Returns a string representation of the node.

        Returns:
            str: The probability of the node.
        """
        return str(self.prob)
    
    
def marginalize_prob(trees):
    """
    Calculates the marginal probability of a list of trees.

    Args:
        trees (list): A list of trees.

    Returns:
        float: The marginal probability of the trees.
    """
    if not trees:
        return 0
    return sum([tree.prob for tree in trees])

def print_tree(node, node_name_attr='value', left_child_attr='left', right_child_attr='right', indent='', last_link='updown'):
    """Prints a syntax tree for the given node.
    
    Args:
    - node: The current node to print.
    - node_name_attr (optional): The attribute of the node that contains the node's name (default: 'value').
    - left_child_attr (optional): The attribute of the node that contains the left child node (default: 'left').
    - right_child_attr (optional): The attribute of the node that contains the right child node (default: 'right').
    - indent (optional): The current indentation of the tree (default: '').
    - last_link (optional): The type of link to the previous node (default: 'updown').
    """

    if hasattr(node, node_name_attr):
        name = lambda node: getattr(node, node_name_attr)
    else:
        name = lambda node: str(node)

    left_child = getattr(node, left_child_attr)
    right_child = getattr(node, right_child_attr)

    if left_child is not None:
        next_last_link = 'up'
        next_indent = f"{indent}{' ' if 'up' in last_link else '|'}{' ' * len(str(name(node)))}"
        print_tree(left_child, node_name_attr, left_child_attr, right_child_attr, next_indent, next_last_link)

    if last_link == 'up':
        start_shape = '┌'
    elif last_link == 'down':
        start_shape = '└'
    elif last_link == 'updown':
        start_shape = ' '
    else:
        start_shape = '├'

    if left_child is not None and right_child is not None:
        end_shape = '┤'
    elif left_child:
        end_shape = '┘'
    elif right_child:
        end_shape = '┐'
    else:
        end_shape = ''

    print(f"{indent}{start_shape}{name(node)}{end_shape}")

    if right_child is not None:
        next_last_link = 'down'
        next_indent = f"{indent}{' ' if 'down' in last_link else '|'}{' ' * len(str(name(node)))}"
        print_tree(right_child, node_name_attr, left_child_attr, right_child_attr, next_indent, next_last_link)
