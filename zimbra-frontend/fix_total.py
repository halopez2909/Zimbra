f = open('src/pages/DashboardPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
lines[27] = '          <p style={{ margin: "8px 0 0", fontSize: "28px", fontWeight: "bold", color: "#fff" }}>{"$" + Number(totalAmount).toLocaleString()}</p>\n'
f = open('src/pages/DashboardPage.tsx', 'w', encoding='utf-8')
f.writelines(lines)
f.close()
print('OK')
