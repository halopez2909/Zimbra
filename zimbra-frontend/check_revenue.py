f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines):
    if 'total_revenue' in line and 'toLocaleString' in line:
        print(i, repr(line))
