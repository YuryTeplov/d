import axios from 'axios';

export default {
  install: (app) => {
    axios.defaults.baseURL = 'http://127.0.0.1:8000/';
    app.config.globalProperties.$axios = axios;
    // You can also add defaults, interceptors, etc. here if needed
  },
};