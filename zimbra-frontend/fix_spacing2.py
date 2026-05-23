import os

pages = [
    'src/pages/ProductsPage.tsx',
    'src/pages/InteractionsPage.tsx',
    'src/pages/ProposalsPage.tsx',
    'src/pages/ClientsPage.tsx',
    'src/pages/CampaignsPage.tsx',
    'src/pages/ReportsPage.tsx'
]

for page in pages:
    if not os.path.exists(page):
        continue
    f = open(page, 'r', encoding='utf-8')
    content = f.read()
    f.close()
    content = content.replace(
        'color: "#666", marginBottom: "24px"',
        'color: "#666", marginTop: "10px", marginBottom: "24px"'
    ).replace(
        'color: "#666", marginBottom: "28px"',
        'color: "#666", marginTop: "10px", marginBottom: "28px"'
    )
    f = open(page, 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('OK:', page)
