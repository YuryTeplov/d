<script setup>
</script>

<template>
  <main>
    <transition name="fade">
      <form v-if="showForm" class="form">
        <h2>Форма входа</h2>
        <input type="text" placeholder="Имя пользователя">
        <input type="password" placeholder="Пароль">
        <button>Войти</button>
      </form>
    </transition>
  </main>
</template>

<script>
export default {
  data() {return {
    showForm: false,
  }},
  mounted() {
    setTimeout(() => {
      this.showForm = true; // Показываем форму
    }, 500); // 500 миллисекунд (0.5 секунды)
  }
}
</script>

<style scoped>
/* Стили анимации */
.slide-fade-enter-active {
  transition: all 1s ease;
}
.slide-fade-leave-active {
  transition: all 1s cubic-bezier(1, 0, 0, 1);
}
.slide-fade-enter, .slide-fade-leave-to {
  transform: translateX(100%) translateY(-100%);
  opacity: 0;
}

/* Стили формы */
.form {
  position: absolute;
  top: 20px;
  right: 20px;
  max-width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.form h2 {
  margin-top: 0;
}

.form input, .form button {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  padding: 8px;
  font-size: 16px;
}

.form button {
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.form button:hover {
  background-color: #0056b3;
}

</style>