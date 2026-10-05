"""
Project 13: 0/1 Knapsack using Branch and Bound
Unit V - Branch and Bound (DAA Macro Project)

What this program does (step by step):
  1. Sorts the items by profit/weight ratio (best ratio first).
  2. Builds a state space tree using Depth First Search.
       - Left branch  = INCLUDE the next item
       - Right branch = EXCLUDE the next item
  3. For every node it calculates an UPPER BOUND (best profit we could
     possibly reach from that node, using fractional items).
  4. PRUNES (cuts off) a node if
       - its weight is more than the capacity (infeasible), or
       - its upper bound <= best profit found so far (cannot improve).
  5. Prints a table of all nodes and the final answer.
  6. Saves the tree as a picture: Visualization.png

How to run:
    pip install matplotlib
    python Project13_Knapsack_BnB.py
"""

import os
import matplotlib
matplotlib.use("Agg")          # lets us save the image without opening a window
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# STEP 1: Input data (4 items, capacity 10)
# ----------------------------------------------------------------------
PROFITS = [40, 42, 25, 12]
WEIGHTS = [4, 7, 5, 3]
CAPACITY = 10

# ----------------------------------------------------------------------
# STEP 2: Sort items by profit/weight ratio (highest first)
# ----------------------------------------------------------------------
items = []
for i in range(len(PROFITS)):
    items.append({"name": "Item" + str(i + 1),
                  "profit": PROFITS[i],
                  "weight": WEIGHTS[i],
                  "ratio": PROFITS[i] / WEIGHTS[i]})
items.sort(key=lambda it: it["ratio"], reverse=True)

n = len(items)
p = [it["profit"] for it in items]
w = [it["weight"] for it in items]

# ----------------------------------------------------------------------
# Global variables used while building the tree
# ----------------------------------------------------------------------
nodes = []          # every node of the tree is stored here
best_profit = 0     # best profit found so far
best_node_id = 0    # id of the node that gave the best profit


# ----------------------------------------------------------------------
# STEP 3: Upper bound function
# ----------------------------------------------------------------------
def calculate_bound(level, profit, weight):
    """
    Upper bound = profit so far + profit of the next items that fit
    completely + a FRACTION of the first item that does not fit.
    'level' is the index of the last item already decided.
    """
    if weight > CAPACITY:
        return 0

    bound = profit
    total_weight = weight
    j = level + 1

    # take whole items while they fit
    while j < n and total_weight + w[j] <= CAPACITY:
        total_weight += w[j]
        bound += p[j]
        j += 1

    # take a fraction of the next item (this makes the bound optimistic)
    if j < n:
        bound += (CAPACITY - total_weight) * p[j] / w[j]

    return bound


# ----------------------------------------------------------------------
# STEP 4: Create a node and decide whether to keep or prune it
# ----------------------------------------------------------------------
def create_node(parent, level, profit, weight, chosen, label):
    global best_profit, best_node_id

    bound = calculate_bound(level, profit, weight)

    if weight > CAPACITY:
        status = "infeasible"            # bag is overweight
    elif bound <= best_profit:
        status = "pruned"                # cannot beat the best answer
    else:
        status = "live"                  # worth exploring further

    node_id = len(nodes)
    nodes.append({
        "id": node_id,
        "parent": parent,
        "level": level,                  # index of last decided item (-1 = root)
        "profit": profit,
        "weight": weight,
        "bound": bound,
        "chosen": chosen,
        "label": label,
        "status": status,
        "children": [],
        "on_best_path": False,
    })
    if parent is not None:
        nodes[parent]["children"].append(node_id)

    # A feasible node with a better profit becomes the new best
    if status != "infeasible" and profit > best_profit:
        best_profit = profit
        best_node_id = node_id

    return node_id


# ----------------------------------------------------------------------
# STEP 5: Branch (DFS): include first, then exclude
# ----------------------------------------------------------------------
def branch(node_id):
    node = nodes[node_id]

    # Stop if this node was pruned, or if all items are already decided
    if node["status"] != "live" or node["level"] == n - 1:
        return

    nxt = node["level"] + 1

    # Left child: INCLUDE item nxt
    inc = create_node(node_id, nxt,
                      node["profit"] + p[nxt],
                      node["weight"] + w[nxt],
                      node["chosen"] + [items[nxt]["name"]],
                      "Include " + items[nxt]["name"])
    branch(inc)

    # Right child: EXCLUDE item nxt
    exc = create_node(node_id, nxt,
                      node["profit"],
                      node["weight"],
                      node["chosen"],
                      "Exclude " + items[nxt]["name"])
    branch(exc)


# ----------------------------------------------------------------------
# STEP 6: Run the algorithm
# ----------------------------------------------------------------------
def solve():
    root = create_node(None, -1, 0, 0, [], "Root")
    branch(root)

    # Mark the path from the best node back to the root (for green colour)
    current = best_node_id
    while current is not None:
        nodes[current]["on_best_path"] = True
        current = nodes[current]["parent"]


def print_results():
    print("Items sorted by profit/weight ratio:")
    print("%-8s %-8s %-8s %-8s" % ("Item", "Profit", "Weight", "Ratio"))
    for it in items:
        print("%-8s %-8d %-8d %-8.2f" % (it["name"], it["profit"], it["weight"], it["ratio"]))
    print("Capacity =", CAPACITY)
    print()
    print("%-4s %-6s %-12s %-7s %-7s %-8s %s" %
          ("ID", "Parent", "Decision", "Profit", "Weight", "Bound", "Status"))
    for nd in nodes:
        print("%-4d %-6s %-12s %-7d %-7d %-8.1f %s" %
              (nd["id"], str(nd["parent"]), nd["label"], nd["profit"],
               nd["weight"], nd["bound"], nd["status"]))
    print()
    print("Maximum profit  :", best_profit)
    print("Items selected  :", nodes[best_node_id]["chosen"])
    print("Total weight    :", nodes[best_node_id]["weight"])


# ----------------------------------------------------------------------
# STEP 7: Draw the state space tree
# ----------------------------------------------------------------------
x_position = {}
next_leaf_x = [0]


def assign_x(node_id):
    """Leaves get x = 0,1,2,...  A parent sits in the middle of its children."""
    kids = nodes[node_id]["children"]
    if len(kids) == 0:
        x_position[node_id] = next_leaf_x[0]
        next_leaf_x[0] += 1
    else:
        for k in kids:
            assign_x(k)
        x_position[node_id] = (x_position[kids[0]] + x_position[kids[-1]]) / 2


def draw_tree(filename):
    assign_x(0)

    colors = {"live": "#cfe8ff", "pruned": "#ff9b9b", "infeasible": "#ffd699"}
    fig, ax = plt.subplots(figsize=(16, 9))

    # draw edges first
    for nd in nodes:
        if nd["parent"] is None:
            continue
        x1, y1 = x_position[nd["parent"]], -(nodes[nd["parent"]]["level"] + 1)
        x2, y2 = x_position[nd["id"]], -(nd["level"] + 1)
        ax.plot([x1, x2], [y1, y2], color="gray", zorder=1)
        ax.text((x1 + x2) / 2, (y1 + y2) / 2 + 0.06,
                "Include" if nd["label"].startswith("Include") else "Exclude",
                fontsize=8, ha="center", color="#333333")

    # draw nodes
    for nd in nodes:
        x, y = x_position[nd["id"]], -(nd["level"] + 1)
        color = colors[nd["status"]]
        if nd["on_best_path"]:
            color = "#9be59b"       # green = path to the best answer

        text = "p=%d  w=%d\nub=%.1f" % (nd["profit"], nd["weight"], nd["bound"])
        if nd["status"] == "pruned":
            text += "\nPRUNED"
        if nd["status"] == "infeasible":
            text += "\nw > W"
        if nd["id"] == best_node_id:
            text += "\nBEST"

        ax.text(x, y, text, ha="center", va="center", fontsize=8, zorder=2,
                bbox=dict(boxstyle="round,pad=0.4", fc=color, ec="black"))

    # level labels on the left
    ax.text(-0.9, 0, "Start", fontsize=10, fontweight="bold", va="center")
    for i in range(n):
        ax.text(-0.9, -(i + 1), "Decide\n" + items[i]["name"] +
                "\n(p=%d, w=%d)" % (p[i], w[i]),
                fontsize=9, fontweight="bold", va="center")

    ax.set_title("0/1 Knapsack - Branch and Bound State Space Tree   "
                 "(Capacity = %d, Max Profit = %d)" % (CAPACITY, best_profit),
                 fontsize=13, pad=15)
    ax.set_xlim(-1.2, next_leaf_x[0] + 0.3)
    ax.set_ylim(-n - 0.6, 0.5)
    ax.axis("off")

    # legend
    legend_text = [("Best path", "#9be59b"), ("Explored", "#cfe8ff"),
                   ("Pruned (bound <= best)", "#ff9b9b"),
                   ("Infeasible (weight > capacity)", "#ffd699")]
    for i, (name, col) in enumerate(legend_text):
        ax.add_patch(plt.Rectangle((next_leaf_x[0] - 1.6, -n + 0.9 - i * 0.25),
                                   0.2, 0.15, fc=col, ec="black"))
        ax.text(next_leaf_x[0] - 1.3, -n + 0.97 - i * 0.25, name,
                fontsize=9, va="center")

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print("Visualization saved as:", filename)


# ----------------------------------------------------------------------
# Main program
# ----------------------------------------------------------------------
if __name__ == "__main__":
    solve()
    print_results()
    folder = os.path.dirname(os.path.abspath(__file__))
    draw_tree(os.path.join(folder, "Visualization.png"))
