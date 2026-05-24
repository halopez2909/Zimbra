f = open('src/pages/DashboardPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines):
    if 'proposed' in line.lower() or 'final' in line.lower() or 'totalAmount' in line:
        print(i, repr(line))
