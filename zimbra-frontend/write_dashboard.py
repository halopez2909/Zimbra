f = open('src/pages/DashboardPage.tsx', 'w', encoding='utf-8')
f.write('''import { useEffect, useState } from "react";

export default function DashboardPage() {
  const [pipeline, setPipeline] = useState<any[]>([]);
  const [traceability, setTraceability] = useState<any[]>([]);
  const [error, setError] = useState("");
  const BASE = "http://localhost:9000";

  useEffect(() => {
    fetch(BASE + "/views/pipeline").then(r => r.json()).then(setPipeline).catch(() => setError("Failed to load pipeline"));
    fetch(BASE + "/views/traceability").then(r => r.json()).then(setTraceability).catch(() => setError("Failed to load traceability"));
  }, []);

  const pipelineColor: Record<string, string> = { draft: "#2E75B6", sent: "#F39C12", negotiation: "#E67E22", accepted: "#1E8449", rejected: "#999" };
  const totalAmount = pipeline.reduce((a, p) => a + p.total_amount, 0);
  const totalSales = traceability.length;

  return (
    <div style={{ padding: "24px" }}>
      <h1 style={{ color: "#1F3864", marginBottom: "12px" }}>Dashboard</h1>
      <p style={{ color: "#666", marginBottom: "24px" }}>Sales pipeline and traceability - Andres Bautista (HU-03/09)</p>

      {error && <div style={{ background: "#FCE4D6", color: "#922B21", padding: "10px", borderRadius: "6px", marginBottom: "16px" }}>{error}</div>}

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: "16px", marginBottom: "24px" }}>
        <div style={{ background: "#1F3864", borderRadius: "8px", padding: "20px", textAlign: "center" }}>
          <p style={{ margin: 0, fontSize: "12px", color: "#AABBEE" }}>Total Pipeline</p>
          <p style={{ margin: "8px 0 0", fontSize: "28px", fontWeight: "bold", color: "#fff" }}></p>
        </div>
        <div style={{ background: "#1E8449", borderRadius: "8px", padding: "20px", textAlign: "center" }}>
          <p style={{ margin: 0, fontSize: "12px", color: "#E2EFDA" }}>Closed Sales</p>
          <p style={{ margin: "8px 0 0", fontSize: "28px", fontWeight: "bold", color: "#fff" }}>{totalSales}</p>
        </div>
        <div style={{ background: "#2E75B6", borderRadius: "8px", padding: "20px", textAlign: "center" }}>
          <p style={{ margin: 0, fontSize: "12px", color: "#DEEAF1" }}>Active Stages</p>
          <p style={{ margin: "8px 0 0", fontSize: "28px", fontWeight: "bold", color: "#fff" }}>{pipeline.length}</p>
        </div>
      </div>

      <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px", marginBottom: "24px" }}>
        <h3 style={{ marginTop: 0, color: "#1F3864" }}>Sales Pipeline by Status</h3>
        {pipeline.map(p => (
          <div key={p.status} style={{ marginBottom: "16px" }}>
            <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "4px" }}>
              <span style={{ fontWeight: "bold", color: pipelineColor[p.status] || "#333", textTransform: "uppercase", fontSize: "13px" }}>{p.status}</span>
              <span style={{ fontSize: "13px", color: "#555" }}>{p.total_proposals} proposals —  ({p.percentage}%)</span>
            </div>
            <div style={{ background: "#F2F2F2", borderRadius: "4px", height: "12px", overflow: "hidden" }}>
              <div style={{ background: pipelineColor[p.status] || "#ccc", width: p.percentage + "%", height: "100%", borderRadius: "4px", transition: "width 0.5s" }} />
            </div>
          </div>
        ))}
      </div>

      <div style={{ background: "#fff", border: "1px solid #ddd", borderRadius: "8px", padding: "20px" }}>
        <h3 style={{ marginTop: 0, color: "#1F3864" }}>Sales Traceability — Campaign to Closed Deal</h3>
        <div style={{ overflowX: "auto" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr style={{ background: "#1F3864", color: "#fff" }}>
                {["Sale ID", "Date", "Client", "Product", "Proposed", "Final", "Campaign", "Seller"].map(h => (
                  <th key={h} style={{ padding: "10px", textAlign: "left", whiteSpace: "nowrap" }}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {traceability.map((t, i) => (
                <tr key={t.sale_id} style={{ background: i % 2 === 0 ? "#f9f9f9" : "#fff" }}>
                  <td style={{ padding: "8px" }}>{t.sale_id}</td>
                  <td style={{ padding: "8px", fontSize: "12px" }}>{t.sale_date?.slice(0, 10)}</td>
                  <td style={{ padding: "8px", fontSize: "13px" }}>{t.client_name}</td>
                  <td style={{ padding: "8px", fontSize: "12px" }}>{t.product_name}</td>
                  <td style={{ padding: "8px" }}></td>
                  <td style={{ padding: "8px", fontWeight: "bold", color: "#1E8449" }}></td>
                  <td style={{ padding: "8px", fontSize: "12px" }}>{t.origin_campaign || "-"}</td>
                  <td style={{ padding: "8px", fontSize: "12px" }}>{t.seller_name || "-"}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
''')
f.close()
print('OK')
