f = open('zimbra-frontend/src/api/api.ts', 'w', encoding='utf-8')
B = 'http://localhost:9000'
f.write('''const BASE_URL = "''' + B + '''";

// Products - Andres
export const getProducts = async () => {
  const res = await fetch(BASE_URL + "/products/");
  if (!res.ok) throw new Error("Failed to fetch products");
  return res.json();
};
export const createProduct = async (data: object) => {
  const res = await fetch(BASE_URL + "/products/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  if (!res.ok) throw new Error("Failed to create product");
  return res.json();
};
export const calculateAmount = async (productId: number, numUsers: number) => {
  const res = await fetch(BASE_URL + "/products/" + productId + "/calculate?num_users=" + numUsers);
  if (!res.ok) throw new Error("Product not found");
  return res.json();
};

// Interactions - Andres
export const getInteractions = async () => {
  const res = await fetch(BASE_URL + "/interactions/");
  if (!res.ok) throw new Error("Failed to fetch interactions");
  return res.json();
};
export const createInteraction = async (data: object) => {
  const res = await fetch(BASE_URL + "/interactions/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  if (!res.ok) throw new Error("Failed to create interaction");
  return res.json();
};

// Proposals - Andres
export const getProposals = async () => {
  const res = await fetch(BASE_URL + "/proposals/");
  if (!res.ok) throw new Error("Failed to fetch proposals");
  return res.json();
};
export const createProposal = async (data: object) => {
  const res = await fetch(BASE_URL + "/proposals/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  if (!res.ok) throw new Error("Failed to create proposal");
  return res.json();
};
export const getPipeline = async () => {
  const res = await fetch(BASE_URL + "/sales/pipeline");
  if (!res.ok) throw new Error("Failed to fetch pipeline");
  return res.json();
};

// Clients - Aleja
export const getClients = async (clientType?: string) => {
  const url = clientType ? BASE_URL + "/clients/?client_type=" + clientType : BASE_URL + "/clients/";
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to fetch clients");
  return res.json();
};
export const createClient = async (data: object) => {
  const res = await fetch(BASE_URL + "/clients/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
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
  const res = await fetch(BASE_URL + "/campaigns/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
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

// Sellers - Jenn
export const getSellers = async () => {
  const res = await fetch(BASE_URL + "/sellers/");
  if (!res.ok) throw new Error("Failed to fetch sellers");
  return res.json();
};
export const createSeller = async (data: object) => {
  const res = await fetch(BASE_URL + "/sellers/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  if (!res.ok) throw new Error("Failed to create seller");
  return res.json();
};
export const getSellerReport = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/sellers/" + sellerId + "/report");
  if (!res.ok) throw new Error("Failed to fetch seller report");
  return res.json();
};
export const getAlertRate = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/sellers/" + sellerId + "/alert-rate");
  if (!res.ok) throw new Error("Failed to fetch alert rate");
  return res.json();
};
export const getFollowupSummary = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/sellers/" + sellerId + "/followup-summary");
  if (!res.ok) throw new Error("Failed to fetch followup summary");
  return res.json();
};

// Alerts - Jenn
export const getAlertsBySeller = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/alerts/seller/" + sellerId);
  if (!res.ok) throw new Error("Failed to fetch alerts");
  return res.json();
};
export const updateAlertStatus = async (alertId: number, status: string) => {
  const res = await fetch(BASE_URL + "/alerts/" + alertId + "/status", { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ status }) });
  if (!res.ok) throw new Error("Failed to update alert");
  return res.json();
};
export const escalateAlerts = async () => {
  const res = await fetch(BASE_URL + "/alerts/escalate", { method: "POST" });
  if (!res.ok) throw new Error("Failed to escalate alerts");
  return res.json();
};

// Followups - Jenn
export const getFollowupsByClient = async (clientId: number) => {
  const res = await fetch(BASE_URL + "/followups/client/" + clientId);
  if (!res.ok) throw new Error("Failed to fetch followups");
  return res.json();
};
export const createFollowup = async (data: object) => {
  const res = await fetch(BASE_URL + "/followups/", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
  if (!res.ok) throw new Error("Failed to create followup");
  return res.json();
};
''')
f.close()
print('OK')
