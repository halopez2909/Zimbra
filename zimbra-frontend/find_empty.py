f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

# Find the last closing div before the final return closing
for i, line in enumerate(lines):
    if 'Select a date range' in line:
        print(i, repr(line))
