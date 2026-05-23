f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    '"Total Revenue", r.total_revenue.toLocaleString(), "#1E8449"',
    '"Total Revenue", "$" + Number(r.total_revenue).toLocaleString(), "#1E8449"'
)
f = open('src/pages/ReportsPage.tsx', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK')
