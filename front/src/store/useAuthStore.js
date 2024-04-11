import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    accessToken: null,
  }),
  actions: {
    setToken(token) {
      this.accessToken = token;
      localStorage.setItem('accessToken', token);
    },
    removeToken() {
      this.accessToken = null;
      localStorage.removeItem('accessToken');
    },
  },
});