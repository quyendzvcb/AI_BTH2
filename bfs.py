import math
import collections
from collections import defaultdict, deque
from trees import Node
from collections import deque

def breadth_first_search(problem):
    root = Node(problem.initial)

    if problem.is_goal(root.state):
        return root

    visited = {root.state}
    queue = deque([root])

    while queue:
        current_node = queue.popleft()
        print(current_node, end=" ")
        for action in problem.actions(current_node.state):
            child_state = problem.result(current_node.state, action)

            cost_to_child = problem.action_cost(current_node.state, action, child_state)
            child_node = Node(child_state, parent=current_node, action=action,
                              path_cost=current_node.path_cost + cost_to_child)

            if child_state not in visited:
                if problem.is_goal(child_state):
                    return child_node

                visited.add(child_state)
                queue.append(child_node)

    return None


