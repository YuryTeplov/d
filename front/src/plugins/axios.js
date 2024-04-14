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

  service.interceptors.response.use(
    (response) => response,
    async (error) => {
      console.log(error)
      const originalRequest = error.config;
      const refreshToken = localStorage.getItem('refreshToken');

      // Check if the error is due to an unauthorized access (401)
      if (error.response && error.response.status === 401 && !originalRequest._retry) {
        originalRequest._retry = true; // Mark request as retried

        try {
          // Attempt to refresh the access token using refresh token
          const refreshResponse = await axios.post(`${baseURL}api/token/refresh/`, {
            refresh: refreshToken,
          });

          const newAccessToken = refreshResponse.data.access;
          localStorage.setItem('accessToken', newAccessToken);

          // Update the Authorization header with the new access token
          originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;

          return service(originalRequest); // Retry the original request with the new token
        } catch (refreshError) {
          if (refreshError.response && refreshError.response.status === 401) {
            // Refresh token failed (e.g., expired or invalid). Log out user.
            console.error('Refresh token failed:', refreshError);
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            // Handle logout logic (e.g., redirect to login page)
          } else {
            // Unexpected error during refresh. Log and re-throw.
            console.error('Failed to refresh access token:', refreshError);
            return Promise.reject(error);
          }
        }
      }

      // Handle other errors (e.g., network errors)
      return Promise.reject(error);
    }
  );

  app.config.globalProperties.$axios = service;
};

export default initAxios;