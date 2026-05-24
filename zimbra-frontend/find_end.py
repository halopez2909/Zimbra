f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
print('Total lines:', len(lines))
for i, line in enumerate(lines[-15:], start=len(lines)-15):
    print(i, repr(line))
