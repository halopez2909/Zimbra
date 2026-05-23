f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    'Select a date range and click Generate Report to see metrics.',
    'No data for selected period.'
)
f = open('src/pages/ReportsPage.tsx', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK')
