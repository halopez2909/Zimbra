f = open('src/App.tsx', 'r', encoding='utf-8')
content = f.read()
f.close()
content = content.replace(
    'import ProductsPage from "./pages/ProductsPage";',
    'import ProductsPage from "./pages/ProductsPage";\nimport DashboardPage from "./pages/DashboardPage";'
).replace(
    '<NavLink to="/products"',
    '<NavLink to="/dashboard" style={({ isActive }) => ({ ...navStyle, ...(isActive ? activeStyle : {}) })}>📊 Dashboard</NavLink>\n            <NavLink to="/products"'
).replace(
    '<Route path="/products"',
    '<Route path="/dashboard" element={<DashboardPage />} />\n            <Route path="/products"'
)
f = open('src/App.tsx', 'w', encoding='utf-8')
f.write(content)
f.close()
print('OK')
