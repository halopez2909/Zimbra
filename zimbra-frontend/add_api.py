f = open('src/api/api.ts', 'a', encoding='utf-8')
B = 'http://localhost:9000'
f.write('''
// Clients - Aleja
export const getClients = async (clientType?: string) => {
  const url = clientType ? BASE_URL + "/clients/?client_type=" + clientType : BASE_URL + "/clients/";
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch clients");
  return res.json();
};

export const createClient = async (data: object) => {
  const res = await fetch(BASE_URL + "/clients/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create client");
  return res.json();
};

// Campaigns - Aleja
export const getCampaigns = async () => {
  const res = await fetch(BASE_URL + "/campaigns/");
  if (!res.ok) throw new Error("Failed to fetch campaigns");
  return res.json();
};

export const createCampaign = async (data: object) => {
  const res = await fetch(BASE_URL + "/campaigns/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create campaign");
  return res.json();
};

export const getCampaignStats = async (campaignId: number) => {
  const res = await fetch(BASE_URL + "/campaigns/" + campaignId + "/stats");
  if (!res.ok) throw new Error("Failed to fetch campaign stats");
  return res.json();
};

// Reports - Aleja
export const getPerformanceReport = async (start: string, end: string) => {
  const res = await fetch(BASE_URL + "/reports/performance?start=" + start + "&end=" + end);
  if (!res.ok) throw new Error("Failed to fetch report");
  return res.json();
};
''')
f.close()
print('OK')
