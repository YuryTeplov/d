<template>
  <div>
    main page

    <div>
      <label for="textInput">Enter text:</label>
      <input type="text" id="textInput" v-model="input_text">
      <button @click="submit">Submit</button>
    </div>

    {{ user_data }}
    
    {{ skills }}

    <button @click="logout">logout</button>
  </div>
</template>


<script>

export default {
  data() {
    return {
      user_data: {},
      input_text: '',
      skills: [],
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      this.$router.push('/')
    },
    async submit() {
      const response = await this.$axios.get('/api/skill/' + this.input_text)

      this.skills = response.data
    },
  },
  async mounted() {
    const response = await this.$axios.get('api/user/current/')

    this.user_data = response.data
  },
}
</script>

<style scoped>
</style>