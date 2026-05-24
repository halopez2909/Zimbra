f = open('src/pages/DashboardPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
lines[72] = '                  <td style={{ padding: "8px" }}>{"$" + Number(t.proposed_amount).toLocaleString()}</td>\n'
lines[73] = '                  <td style={{ padding: "8px", fontWeight: "bold", color: "#1E8449" }}>{"$" + Number(t.final_amount).toLocaleString()}</td>\n'
f = open('src/pages/DashboardPage.tsx', 'w', encoding='utf-8')
f.writelines(lines)
f.close()
print('OK')
