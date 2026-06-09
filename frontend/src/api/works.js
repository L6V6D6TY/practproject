import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const worksApi = {
  getAll: (params) => api.get('/api/works', { params }),
  getById: (id) => api.get(`/api/works/${id}`),
  create: (data) => api.post('/api/works', data),
  update: (id, data) => api.put(`/api/works/${id}`, data),
  delete: (id) => api.delete(`/api/works/${id}`),
};

export default api;