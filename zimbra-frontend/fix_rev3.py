f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
lines[68] = '              <p style={{ margin: "4px 0 0", fontSize: "22px", fontWeight: "bold", color: "#1E8449" }}>{"$" + Number(r.total_revenue).toLocaleString()}</p>\n'
f = open('src/pages/ReportsPage.tsx', 'w', encoding='utf-8')
f.writelines(lines)
f.close()
print('OK')
