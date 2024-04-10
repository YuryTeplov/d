<template>
  <div class="container" id="service-page">
    <header class="content">
      <h1>Your Service Name</h1>
    </header>

    <main class="content">
      <section class="input-section">
        <label for="textInput">Enter Text:</label>
        <input type="text" id="textInput" v-model="input_text">
        <button @click="submit" :disabled="!input_text">Submit</button>
      </section>


      <section class="skills-and-videos">
        <div class="skill-buttons">
          <button v-for="skill in skills" @click="load_videos_by_this_skill(skill)" :key="skill">
            {{ skill }}
          </button>
        </div>

        <div class="video-list" v-if="videos.length > 0">
          <h2>Videos for {{ current_skill }}</h2>
          <ul>
            <li v-for="video in videos" :key="video.id">
              <div class="video-item">
                <a :href="video.youtube_url" target="_blank">
                  <img :src="video.thumbnail_url" alt="Thumbnail">
                </a>
                <div class="video-info">
                  <h3>{{ video.title }}</h3>
                  <p>{{ video.description }}</p>
                </div>
              </div>
            </li>
          </ul>
        </div>
      </section>
    </main>

    <footer class="content">

      <section class="user-data" v-if="user_data">
        <h2>User Data</h2>
        <pre>{{ user_data.username }}, {{ user_data.email }}</pre>  </section>

      <button @click="logout">Logout</button>
    </footer>
  </div>
</template>


<script>

export default {
  data() {
    return {
      user_data: {},
      input_text: '',
      skills: [],
      videos: [],
    };
  },
  methods: {
    async load_videos_by_this_skill(skill) {
      const response = await this.$axios.get('/api/videos/' + skill)

      this.videos = response.data.videos
    },
    logout() {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      this.$router.push('/')
    },
    async submit() {
      const response = await this.$axios.get('/api/skill/' + this.input_text)

      this.skills = response.data.skills
    },
  },
  async mounted() {
    const response = await this.$axios.get('api/user/current/')

    this.user_data = response.data
  },
}
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&display=swap");

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* Контейнер */
.container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}

/* Внутреннее содержимое */
.content {
  max-width: 1200px; /* Задайте желаемую максимальную ширину */
  padding: 1rem;
}

/* Дополнительные стили */
.hidden {
  display: none;
}

.error {
  color: red;
}

/* Шрифты */
body {
  font-family: "Roboto", sans-serif;
}

/* Общий контейнер */
#service-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Шапка */
header {
  color: #fff;
  padding: 1rem;
  text-align: center;
}

header h1 {
  margin: 0;
}

/* Основная часть */
main {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

/* Раздел ввода */
.input-section {
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
}

.input-section label {
  margin-right: 1rem;
}

.input-section input {
  padding: 0.5rem;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  flex: 1;
}

.input-section button {
  margin-left: 1rem;
  padding: 0.5rem 1rem;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

.input-section button:disabled {
  cursor: not-allowed;
}

/* Раздел данных пользователя */
.user-data {
  padding: 1rem;
  margin-bottom: 1rem;
}

.user-data pre {
  white-space: pre-wrap;
  padding: 1rem;
  border-radius: 4px;
}

/* Раздел навыков и видео */
.skills-and-videos {
  display: flex;
  flex-direction: column;
}

/* Кнопки навыков */
.skill-buttons {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 1rem;
}

.skill-buttons button {
  margin: 0.5rem;
  padding: 0.5rem 1rem;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

/* Список видео */
.video-list {
  padding: 1rem;
  margin-bottom: 1rem;
}

.video-list h2 {
  margin-top: 0;
}

.video-list ul {
  list-style: none;
  padding: 0;
}

.video-list li {
  margin-bottom: 0.5rem;
}

.video-list a {
  color: #fff;
  text-decoration: none;
  transition: color 0.2s ease-in-out;
}

.video-list a:hover {
  color: #fff;
}

/* Подвал */
footer {
  color: #fff;
  padding: 1rem;
  text-align: center;
}

footer button {
  margin-left: 1rem;
  padding: 0.5rem 1rem;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 4px;
  cursor: pointer;
}

/* Дополнительные стили */
.hidden {
  display: none;
}

.error {
  color: red;
}
</style>