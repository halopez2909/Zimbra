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
    content = content.replace("marginBottom: '4px' }}>", "marginBottom: '12px' }}>")
    f = open(page, 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('OK:', page)
