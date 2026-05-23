const BASE_URL = "http://localhost:9000";

export const getProducts = async () => {
  const res = await fetch(BASE_URL + "/products/");
  if (!res.ok) throw new Error("Failed to fetch products");
  return res.json();
};

export const createProduct = async (data: object) => {
  const res = await fetch(BASE_URL + "/products/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create product");
  return res.json();
};

export const calculateAmount = async (productId: number, numUsers: number) => {
  const res = await fetch(BASE_URL + "/products/" + productId + "/calculate?num_users=" + numUsers);
  if (!res.ok) throw new Error("Product not found");
  return res.json();
};

export const getInteractions = async () => {
  const res = await fetch(BASE_URL + "/interactions/");
  if (!res.ok) throw new Error("Failed to fetch interactions");
  return res.json();
};

export const createInteraction = async (data: object) => {
  const res = await fetch(BASE_URL + "/interactions/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create interaction");
  return res.json();
};

export const getProposals = async () => {
  const res = await fetch(BASE_URL + "/proposals/");
  if (!res.ok) throw new Error("Failed to fetch proposals");
  return res.json();
};

export const createProposal = async (data: object) => {
  const res = await fetch(BASE_URL + "/proposals/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
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
