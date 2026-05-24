f = open('src/pages/DashboardPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines[20:35], start=20):
    print(i, repr(line))
