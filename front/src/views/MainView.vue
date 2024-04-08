<template>
  <div>
    main page
    <button @click="logout">logout</button>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
</style>