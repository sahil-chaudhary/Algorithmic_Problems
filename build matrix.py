def greedy_pawn_placement(r, c):
  n = len(r)
  A = [[0 for _ in range(n)] for _ in range(n)]

  for i in range(n):
    # Calculate the number of 1's in each column of the first i-1 rows.
    a = [0 for _ in range(n)]
    for j in range(i):
      for k in range(n):
        a[k] += A[j][k]

    # Find the r_i columns with the maximum c_j - a_j.
    max_cols = []
    for j in range(n):
      max_cols.append((c[j] - a[j], j))
    max_cols.sort(reverse=True)

    # Assign 1's to the r_i columns with the maximum c_j - a_j.
    for j in range(r[i]):
      col = max_cols[j][1]
      A[i][col] = 1

  return A
r=[3,2,1,1]
c=[2,2,2,1]
print(greedy_pawn_placement(r,c))