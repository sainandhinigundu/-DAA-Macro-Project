"""
Project 1: Sorting Complexity Visualizer
Compares Merge Sort and Quick Sort for n = 10, 100, 1000
by counting key comparisons and plotting growth rates.
"""
import math
import random
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.setrecursionlimit(10000)
SIZES = [10, 100, 1000]
TRIALS = 20  # random inputs averaged per size


def merge_sort(arr, counter):
    """Divide in halves, sort each, merge. Always O(n log n)."""
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], counter)
    right = merge_sort(arr[mid:], counter)
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        counter[0] += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr, counter, random_pivot=True):
    """Partition around a pivot, recurse on both sides.
    Average O(n log n); worst case O(n^2) with a bad pivot."""
    if len(arr) <= 1:
        return arr
    pivot = random.choice(arr) if random_pivot else arr[-1]
    less, equal, greater = [], [], []
    for x in arr:
        counter[0] += 1
        if x < pivot:
            less.append(x)
        elif x == pivot:
            equal.append(x)
        else:
            greater.append(x)
    return quick_sort(less, counter, random_pivot) + equal + quick_sort(greater, counter, random_pivot)


def measure():
    results = {"Merge Sort": [], "Quick Sort (average)": [], "Quick Sort (worst case)": []}
    for n in SIZES:
        m_total = q_total = 0
        for _ in range(TRIALS):
            data = random.sample(range(n * 10), n)
            c = [0]; merge_sort(data, c); m_total += c[0]
            c = [0]; quick_sort(data, c, True); q_total += c[0]
        results["Merge Sort"].append(m_total / TRIALS)
        results["Quick Sort (average)"].append(q_total / TRIALS)
        # worst case: already sorted input with last-element pivot
        c = [0]; quick_sort(list(range(n)), c, random_pivot=False)
        results["Quick Sort (worst case)"].append(c[0])
    return results


def plot(results):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    styles = {"Merge Sort": ("tab:blue", "o"),
              "Quick Sort (average)": ("tab:green", "s"),
              "Quick Sort (worst case)": ("tab:red", "^")}
    for ax, log in zip(axes, [False, True]):
        for name, vals in results.items():
            color, marker = styles[name]
            ax.plot(SIZES, vals, marker=marker, color=color, linewidth=2, label=name)
        ax.plot(SIZES, [n * math.log2(n) for n in SIZES], "k--", alpha=0.5, label="n log2 n (reference)")
        ax.set_xlabel("Input size (n)")
        ax.set_ylabel("Number of comparisons")
        ax.grid(True, alpha=0.3)
        ax.set_xticks(SIZES)
        if log:
            ax.set_xscale("log"); ax.set_yscale("log")
            ax.set_xticks(SIZES); ax.set_xticklabels([str(s) for s in SIZES])
            ax.set_title("Log-log scale")
        else:
            ax.set_title("Linear scale")
    axes[0].legend()
    fig.suptitle("Merge Sort vs Quick Sort: Growth of Comparisons (n = 10, 100, 1000)", fontweight="bold")
    plt.tight_layout()
    plt.savefig("Visualization.png", dpi=150)


if __name__ == "__main__":
    random.seed(42)
    res = measure()
    print(f"{'n':>6} | " + " | ".join(f"{k:>24}" for k in res))
    for i, n in enumerate(SIZES):
        print(f"{n:>6} | " + " | ".join(f"{res[k][i]:>24.0f}" for k in res))
    plot(res)
    print("Saved Visualization.png")
