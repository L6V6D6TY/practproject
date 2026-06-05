import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Перехват ошибок
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const worksApi = {
  // Получение списка с пагинацией и фильтрацией
  getAll: async (page = 1, limit = 100, field = null, value = null) => {
    const params = { page, limit };
    if (field && value) {
      params.field = field;
      params.value = value;
    }
    const response = await api.get('/works', { params });
    return response.data; // { items, total, page, limit, total_pages }
  },

  // Получение одной записи
  getById: async (id) => {
    const response = await api.get(`/works/${id}`);
    return response.data;
  },

  // Создание записи
  create: async (data) => {
    const response = await api.post('/works', data);
    return response.data;
  },

  // Обновление записи
  update: async (id, data) => {
    const response = await api.put(`/works/${id}`, data);
    return response.data;
  },

  // Удаление записи
  delete: async (id) => {
    await api.delete(`/works/${id}`);
  },
};

export default api;