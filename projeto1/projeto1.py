# imports necessarios
from search import *
from notebook import psource, heatmap, gaussian_kernel, show_map, final_path_colors, display_visual, plot_NQueens
import networkx as nx
import numpy
import matplotlib.pyplot as plt
# Needed to hide warnings in the matplotlib sections
import warnings
warnings.filterwarnings("ignore")

# # Cria o tabuleiro

# generate the nodes of the graph - need to think if I will still consider 0 as a wall
coords = []
for i in range(0,60):
    for j in range(0,60):
        coords.append((i,j))

# make the dict where the key is associated with his neighbors
mapa = {}
for element in coords:
    res = []
    if element[0] + 1 < 60:
        res.append((element[0]+1,element[1]))
    if element[0] - 1 > 0:
        res.append((element[0]-1,element[1]))
    if element[1] + 1 < 60:
        res.append((element[0],element[1]+1))
    if element[1] - 1 > 0:
        res.append((element[0],element[1]-1))

    mapa[element] = res

grafo = nx.Graph(mapa)

class RobotProblem(Problem):

    """Problema para encontrar o goal saindo de uma posicao (x,y) com um robo."""

    def __init__(self, initial, goal, mapa, graph):
        Problem.__init__(self, initial, goal)
        self.mapa = mapa
        self.graph = graph

    def actions(self, actual_pos):
        """The actions at a graph node are just its neighbors."""
        valid_actions = []
        for act in self.mapa[actual_pos]:
            try:
                if (act[0] == 20 and (0<= act[1] <= 40)) or (act[0] == 40 and (40<= act[1] <= 60)):
                    continue
                else:
                    valid_actions.append(act)
            except:
                pass
        return valid_actions

    def result(self, state, action):
        """The result of going to a neighbor is just that neighbor."""
        return action

    def path_cost(self, cost_so_far, state1, action, state2):
        return cost_so_far + 1

    def goal_test(self, state):
        if state[0] == self.goal[0] and state[1] == self.goal[1]:
            return True
        else:
            return False

#     def find_min_edge(self):
#         """Find minimum value of edges."""
#         m = infinity
#         for d in self.graph.graph_dict.values():
#             local_min = min(d.values())
#             m = min(m, local_min)

#         return m

#     def h(self, node):
#         """h function is straight-line distance from a node's state to goal."""
#         locs = getattr(self.graph, 'locations', None)
#         if locs:
#             if type(node) is str:
#                 return int(distance(locs[node], locs[self.goal]))

#             return int(distance(locs[node.state], locs[self.goal]))
#         else:
#             return infinity


# In[6]:


init_pos = (5,8)
goal_pos = (20,50)


# In[7]:
robot_problem = RobotProblem(init_pos, goal_pos, mapa, grafo)

import pdb; pdb.set_trace()

# In[ ]:


node = breadth_first_tree_search(robot_problem)
print("*************************************************************************************")
print("\nCOST:\n")
print(node.path_cost)


# In[ ]:
#
#
# def tree_breadth_search_for_vis(problem):
#     """Search through the successors of a problem to find a goal.
#     The argument frontier should be an empty queue.
#     Don't worry about repeated paths to a state. [Figure 3.7]"""
#
#     # we use these two variables at the time of visualisations
#     iterations = 0
#     all_node_colors = []
#     node_colors = {k : 'white' for k in problem.graph.nodes()}
#
#     #Adding first node to the queue
#     frontier = deque([Node(problem.initial)])
#
#     node_colors[Node(problem.initial).state] = "orange"
#     iterations += 1
#     all_node_colors.append(dict(node_colors))
#
#     while frontier:
#         #Popping first node of queue
#         node = frontier.popleft()
#
#         # modify the currently searching node to red
#         node_colors[node.state] = "red"
#         iterations += 1
#         all_node_colors.append(dict(node_colors))
#
#         if problem.goal_test(node.state):
#             # modify goal node to green after reaching the goal
#             node_colors[node.state] = "green"
#             iterations += 1
#             all_node_colors.append(dict(node_colors))
#             return(iterations, all_node_colors, node)
#
#         frontier.extend(node.expand(problem))
#
#         for n in node.expand(problem):
#             node_colors[n.state] = "orange"
#             iterations += 1
#             all_node_colors.append(dict(node_colors))
#
#         # modify the color of explored nodes to gray
#         node_colors[node.state] = "gray"
#         iterations += 1
#         all_node_colors.append(dict(node_colors))
#
#     return None
#
# def breadth_first_tree_search_aa(problem):
#     "Search the shallowest nodes in the search tree first."
#     iterations, all_node_colors, node = tree_breadth_search_for_vis(problem)
#     return(iterations, all_node_colors, node)
#
#
# # In[8]:
#
#
# def tree_depth_search_for_vis(problem):
#     """Search through the successors of a problem to find a goal.
#     The argument frontier should be an empty queue.
#     Don't worry about repeated paths to a state. [Figure 3.7]"""
#
#     # we use these two variables at the time of visualisations
#     iterations = 0
#     all_node_colors = []
#     node_colors = {k : 'white' for k in problem.graph.nodes()}
#
#     #Adding first node to the stack
#     frontier = [Node(problem.initial)]
#
#     node_colors[Node(problem.initial).state] = "orange"
#     iterations += 1
#     all_node_colors.append(dict(node_colors))
#
#     while frontier:
#         #Popping first node of stack
#         node = frontier.pop()
#
#         # modify the currently searching node to red
#         node_colors[node.state] = "red"
#         iterations += 1
#         all_node_colors.append(dict(node_colors))
#
#         if problem.goal_test(node.state):
#             # modify goal node to green after reaching the goal
#             node_colors[node.state] = "green"
#             iterations += 1
#             all_node_colors.append(dict(node_colors))
#             return(iterations, all_node_colors, node)
#
#         frontier.extend(node.expand(problem))
#
#         for n in node.expand(problem):
#             node_colors[n.state] = "orange"
#             iterations += 1
#             all_node_colors.append(dict(node_colors))
#
#         # modify the color of explored nodes to gray
#         node_colors[node.state] = "gray"
#         iterations += 1
#         all_node_colors.append(dict(node_colors))
#
#     return None
#
# def depth_first_tree_search_imp(problem):
#     "Search the deepest nodes in the search tree first."
#     iterations, all_node_colors, node = tree_depth_search_for_vis(problem)
#     return(iterations, all_node_colors, node)
#
#
# # In[ ]:
#
#
# all_node_colors = []
# a, b, c = depth_first_tree_search_imp(robot_problem)
#
#
# # In[ ]:
