f = open('src/pages/ProductsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()
lines[120] = "                <td style={{ padding: '10px' }}>{Number(p.base_price).toLocaleString()}</td>\n"
f = open('src/pages/ProductsPage.tsx', 'w', encoding='utf-8')
f.writelines(lines)
f.close()
print('OK')
