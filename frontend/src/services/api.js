import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://3.110.32.50",
  headers: { "Content-Type": "application/json" }
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export async function signup(data) {
  const response = await api.post("/api/auth/signup", data);
  return response.data;
}

export async function login(data) {
  const response = await api.post("/api/auth/login", data);
  return response.data;
}

export async function getMe() {
  const response = await api.get("/api/auth/me");
  return response.data;
}

export async function createPreview(url) {
  const response = await api.post("/api/urls/preview", { url });
  return response.data;
}

export async function getSavedUrls() {
  const response = await api.get("/api/urls");
  return response.data;
}

export async function deleteSavedUrl(id) {
  await api.delete(`/api/urls/${id}`);
}

export function getErrorMessage(error) {
  return error.response?.data?.detail || error.message || "Something went wrong.";
}
