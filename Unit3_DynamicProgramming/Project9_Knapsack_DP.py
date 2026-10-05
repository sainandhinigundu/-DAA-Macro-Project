def knapsack(weights, values, capacity):
    n = len(weights)

    # Create DP table
    dp = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    # Fill the DP table
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):

            if weights[i - 1] <= w:
                include = values[i - 1] + dp[i - 1][w - weights[i - 1]]
                exclude = dp[i - 1][w]

                dp[i][w] = max(include, exclude)
            else:
                dp[i][w] = dp[i - 1][w]

    return dp


# 4 Items
weights = [2, 3, 4, 5]
values = [3, 4, 5, 6]
capacity = 10

dp = knapsack(weights, values, capacity)

print("DP Table:")
for row in dp:
    print(row)

print("\nMaximum Profit:", dp[len(weights)][capacity])