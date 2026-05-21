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

// ============================================================
// Session 3 - Jenn Olaya - Sellers, Alerts and Follow-ups
// ============================================================

// --- Sellers (HU-01) ---
export const getSellers = async (onlyActive = true) => {
  const res = await fetch(BASE_URL + "/sellers/?only_active=" + onlyActive);
  if (!res.ok) throw new Error("Failed to fetch sellers");
  return res.json();
};

export const createSeller = async (data: object) => {
  const res = await fetch(BASE_URL + "/sellers/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to create seller");
  }
  return res.json();
};

export const getSellerReport = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/sellers/" + sellerId + "/report");
  if (!res.ok) throw new Error("Seller not found");
  return res.json();
};

export const getAlertRate = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/sellers/" + sellerId + "/alert-rate");
  if (!res.ok) throw new Error("Seller not found");
  return res.json();
};

export const getFollowupSummary = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/sellers/" + sellerId + "/followup-summary");
  if (!res.ok) throw new Error("Seller not found");
  return res.json();
};

// --- Alerts (HU-06) ---
export const getAlertsBySeller = async (sellerId: number) => {
  const res = await fetch(BASE_URL + "/alerts/seller/" + sellerId);
  if (!res.ok) {
    if (res.status === 404) return [];
    throw new Error("Failed to fetch alerts");
  }
  return res.json();
};

export const updateAlertStatus = async (alertId: number, status: string) => {
  const res = await fetch(BASE_URL + "/alerts/" + alertId + "/status", {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to update alert");
  }
  return res.json();
};

export const escalateAlerts = async () => {
  const res = await fetch(BASE_URL + "/alerts/escalate", { method: "POST" });
  if (!res.ok) throw new Error("Failed to escalate alerts");
  return res.json();
};

// --- Follow-ups (HU-07) ---
export const createFollowUp = async (data: object) => {
  const res = await fetch(BASE_URL + "/followups/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to create follow-up");
  }
  return res.json();
};

export const getFollowUpsByClient = async (clientId: number) => {
  const res = await fetch(BASE_URL + "/followups/client/" + clientId);
  if (!res.ok) {
    if (res.status === 404) return [];
    throw new Error("Failed to fetch follow-ups");
  }
  return res.json();
};
