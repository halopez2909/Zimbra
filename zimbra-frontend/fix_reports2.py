f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    'const [loading, setLoading] = useState(false);',
    'const [loading, setLoading] = useState(false);\n  const [searched, setSearched] = useState(false);'
)
content = content.replace(
    'try {\n      const data = await getPerformanceReport(form.start, form.end);',
    'setSearched(true);\n    try {\n      const data = await getPerformanceReport(form.start, form.end);'
)
content = content.replace(
    'reports.length === 0 && !loading',
    'reports.length === 0 && !loading && searched'
)
content = content.replace(
    'No data for selected period.',
    'No data found for the selected period.'
)
f = open('src/pages/ReportsPage.tsx', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK')
