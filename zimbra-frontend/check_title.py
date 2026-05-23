f = open('src/pages/ProposalsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines):
    if 'Proposals' in line or 'pipeline' in line.lower() or 'Sales pipe' in line:
        print(i, repr(line))
