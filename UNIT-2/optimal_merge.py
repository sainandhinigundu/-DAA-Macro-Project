import heapq


def optimal_merge(sizes):
    """Return (total_cost, list_of_merge_steps) using the greedy min-heap method."""
    heap = list(sizes)
    heapq.heapify(heap)
    total, steps = 0, []
    while len(heap) > 1:
        a = heapq.heappop(heap)
        b = heapq.heappop(heap)
        merged = a + b
        total += merged
        steps.append((a, b, merged))
        heapq.heappush(heap, merged)
    return total, steps


if __name__ == "__main__":
    files = [10, 20, 30, 40]
    cost, steps = optimal_merge(files)
    for i, (a, b, m) in enumerate(steps, 1):
        print(f"Step {i}: merge {a} + {b} = {m}")
    print("Minimum total cost:", cost)
