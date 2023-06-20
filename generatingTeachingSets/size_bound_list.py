def all_combinations(total, highest=4):
    dp = [[[] for _ in range(total + 1)] for _ in range(highest + 1)]

    # Initialize base cases
    for i in range(highest + 1):
        dp[i][0] = [[]]
        
    for i in range(1, highest + 1):
        for j in range(1, total + 1):
            # Exclude the i
            if j < i:
                dp[i][j] = dp[i-1][j]
            else:
                # Include the i
                dp[i][j] = dp[i-1][j] + [combo + [i] for combo in dp[i][j-i]]

    # Add zero to each combination
    for i in range(1, highest + 1):
        for j in range(1, total + 1):
            dp[i][j] = sorted([ [0] + combo for combo in dp[i][j]] + [combo for combo in dp[i][j]])

    return dp[highest][total]

if __name__ == '__main__':
    for i in range(1,10):
        print("#"*10,i,"#"*10)
        for c in all_combinations(i, 4):
            print(c)
