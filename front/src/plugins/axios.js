// axios.js
import axios from 'axios';

const baseURL = 'http://127.0.0.1:8000/';

const initAxios = (app) => {
  const service = axios.create({
    baseURL,
  });

  // Add a global request interceptor to handle token inclusion
  service.interceptors.request.use(
    (config) => {
      const token = localStorage.getItem('accessToken');
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    (error) => Promise.reject(error)
  );

  app.config.globalProperties.$axios = service;
};

export default initAxios;