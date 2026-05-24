f = open('src/pages/DashboardPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines[60:80], start=60):
    print(i, repr(line))
