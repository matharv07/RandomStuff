n, m = map(int, input().split())

if n != m:
    print("No")

else:
    result = [['#' for _ in range(m)] for _ in range(n)]
    changes_by_index = []
    used = [set() for _ in range(n)]
    for i in range(n):
        needed = m % (i + 1)
        changes_by_index.append([needed, i])
    for i in range(n):
        if changes_by_index[i][0] > 0:
            result[i][i] = '.'
            changes_by_index[i][0] -= 1
            used[i].add(i)
    rows_with_changes = [x for x in changes_by_index if x[0] > 0]

    while rows_with_changes:
        rows_with_changes.sort(key=lambda x: x[0], reverse=True)
        r1_placeholder = rows_with_changes[0]
        r1 = r1_placeholder[1]
        rows_with_changes.pop(0)
        found = False

        for idx, item in enumerate(rows_with_changes):
            r2 = item[1]

            if r2 not in used[r1]:
                result[r1][r2] = '.'
                result[r2][r1] = '.'
                used[r1].add(r2)
                used[r2].add(r1)
                r1_placeholder[0] -= 1
                item[0] -= 1

                if item[0] == 0:
                    rows_with_changes.pop(idx)
                if r1_placeholder[0] > 0:
                    rows_with_changes.append(r1_placeholder)
                found = True
                break
        
        if not found:
            if 0 not in used[r1]:
                result[r1][0] = '.'
                result[0][r1] = '.'
                used[r1].add(0)
                used[0].add(r1)
                r1_placeholder[0] -= 1
                if r1_placeholder[0] > 0:
                    rows_with_changes.append(r1_placeholder)
            else:
                pass

    print("Yes")
    for row in result:
        print("".join(row))