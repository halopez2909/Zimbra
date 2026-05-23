f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines):
    if 'revenue' in line.lower() or 'Revenue' in line:
        print(i, repr(line))
