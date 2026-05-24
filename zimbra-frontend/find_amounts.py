f = open('src/pages/DashboardPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines):
    if 'proposed_amount' in line and 'toLocaleString' in line:
        print(i, repr(line))
    if 'final_amount' in line and 'toLocaleString' in line:
        print(i, repr(line))
    if 'totalAmount' in line and 'toLocaleString' in line:
        print(i, repr(line))
