f = open('src/pages/ProposalsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines[125:160], start=125):
    print(i, repr(line))
