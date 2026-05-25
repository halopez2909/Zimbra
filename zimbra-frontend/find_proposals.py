f = open('src/pages/ProposalsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
for i, line in enumerate(lines):
    if 'proposed_amount' in line.lower() or 'Amount' in line:
        print(i, repr(line))
