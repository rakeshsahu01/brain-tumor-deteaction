import axios from "axios";

const API_BASE = process.env.REACT_APP_API_BASE_URL || "

const api = axios.create({
  baseURL: API_BASE,
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authApi = {
  signup: (payload) => api.post("/api/auth/signup", payload),
  login: (payload) => api.post("/api/auth/login", payload),
};

export const predictionApi = {
  predict: (payload) => api.post("/api/predict", payload),
  legacyPredict: (payload) => api.post("/", payload),
};

export const patientApi = {
  create: (payload) => api.post("/api/patients/", payload),
  getById: (id) => api.get(`/api/patients/${id}`),
};

export const historyApi = {
  list: () => api.get("/api/history/"),
};

export const reportApi = {
  downloadUrl: (id) => `${API_BASE}/api/report/${id}/download`,
  download: (id) => api.get(`/api/report/${id}/download`, { responseType: "blob" }),
};

export default api;
