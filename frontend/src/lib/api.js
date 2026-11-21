import axios from "axios";
const api = axios.create({baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api", timeout: 60000});
api.interceptors.response.use(r=>r, error=>{
  const message = error.response?.data?.detail || error.message || "Unexpected server error";
  return Promise.reject(new Error(message));
});
export default api;
