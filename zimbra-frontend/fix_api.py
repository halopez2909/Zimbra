f = open('src/api/api.ts', 'w', encoding='utf-8')
B = 'http://localhost:9000'
f.write('''const BASE_URL = "''' + B + '''";

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
''')
f.close()
print('OK')
