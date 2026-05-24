f = open('src/pages/ReportsPage.tsx', 'r', encoding='utf-8')
content = f.read()
f.close()

# Add import for useEffect and campaign effectiveness
new_content = content.replace(
    'import { useState } from "react";',
    'import { useState, useEffect } from "react";'
).replace(
    'export default function ReportsPage() {',
    '''export default function ReportsPage() {
  const [campaigns, setCampaigns] = useState<any[]>([]);
  const BASE = "http://localhost:9000";

  useEffect(() => {
    fetch(BASE + "/views/campaigns")
      .then(r => r.json())
      .then(data => setCampaigns(data.sort((a: any, b: any) => b.conversion_rate - a.conversion_rate)))
      .catch(() => {});
  }, []);'''
)

f = open('src/pages/ReportsPage.tsx', 'w', encoding='utf-8')
f.write(new_content)
f.close()
print('OK - imports added')
