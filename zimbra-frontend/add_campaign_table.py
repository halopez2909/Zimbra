f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

campaign_table = '''
      <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px", marginTop: "24px" }}>
        <h3 style={{ marginTop: 0, color: "#1F3864" }}>Campaign Effectiveness - Heyleen Alejandra Lopez</h3>
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr style={{ background: "#1F3864", color: "#fff" }}>
              {["ID", "Campaign", "Type", "Status", "Interactions", "Converted", "Conversion Rate", "Cost/Conv"].map(h => (
                <th key={h} style={{ padding: "10px", textAlign: "left", fontSize: "13px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {campaigns.map((c, i) => (
              <tr key={c.campaign_id} style={{ background: i % 2 === 0 ? "#f9f9f9" : "#fff" }}>
                <td style={{ padding: "8px" }}>{c.campaign_id}</td>
                <td style={{ padding: "8px", fontSize: "13px" }}>{c.campaign_name}</td>
                <td style={{ padding: "8px", fontSize: "12px" }}>{c.campaign_type}</td>
                <td style={{ padding: "8px" }}>
                  <span style={{ background: c.status === "active" ? "#E2EFDA" : c.status === "high_demand" ? "#DEEAF1" : "#F2F2F2", color: c.status === "active" ? "#1E8449" : c.status === "high_demand" ? "#1F3864" : "#555", padding: "2px 8px", borderRadius: "12px", fontSize: "11px" }}>
                    {c.status}
                  </span>
                </td>
                <td style={{ padding: "8px" }}>{c.total_interactions}</td>
                <td style={{ padding: "8px" }}>{c.total_converted}</td>
                <td style={{ padding: "8px", fontWeight: "bold", color: c.conversion_rate > 50 ? "#1E8449" : c.conversion_rate < 20 ? "#922B21" : "#F39C12" }}>
                  {c.conversion_rate}%
                </td>
                <td style={{ padding: "8px", fontSize: "13px" }}>{c.cost_per_conversion ? "$" + Number(c.cost_per_conversion).toLocaleString() : "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
'''

lines.insert(97, campaign_table)
f = open('src/pages/ReportsPage.tsx', 'w', encoding='utf-8')
f.writelines(lines)
f.close()
print('OK')
