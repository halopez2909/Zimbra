f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines[65:72], start=65):
    print(i, repr(line))
