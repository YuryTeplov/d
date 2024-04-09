import axios from 'axios';

export default {
  install: (app) => {
    axios.defaults.baseURL = 'http://127.0.0.1:8000/';

    const token = localStorage.getItem('accessToken');
    axios.defaults.headers.common['Authorization'] = token ? `Bearer ${token}` : null;

    app.config.globalProperties.$axios = axios;
  },
};