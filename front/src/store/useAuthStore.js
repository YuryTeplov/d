import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
    refreshToken: null,
  }),
  actions: {
    setToken(token) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
    },
    setRefreshToken(token) {
      this.refreshToken = token;
      localStorage.setItem('refreshToken', token);
    },
    removeToken() {
      this.accessToken = null;
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    },
  },
});