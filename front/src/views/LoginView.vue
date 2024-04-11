<template>
  <div>
    <h2>Форма авторизации</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Имя пользователя:</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Войти</button>
    </form>
  </div>
</template>


<script>
import { useAuthStore } from '../store/useAuthStore';


export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    login() {
      this.$axios.post('/api/token/', {
        username: this.username,
        password: this.password
      })
      .then(response => {

        const store = useAuthStore();

        store.setToken(response.data.access);

        this.$router.push('/main')
      })
      .catch(error => {
        console.error('Error logging in:', error);
      });
    }
  }
}
</script>

<style scoped>
/* Стилизуйте вашу форму по желанию */
form {
  max-width: 300px;
  margin: 0 auto;
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
}
button {
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}
</style>