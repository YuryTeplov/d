<template>
  <div class="container" id="service-page">
    <header>
      <h1>Рекомендация обучающих материалов</h1>
    </header>

    <main class="content">
      <section class="input-section">
        <form @submit.prevent="submit">
          <label for="textInput">Введите название профессии:</label>
          <input type="text" id="textInput" v-model="input_text">
          <button :disabled="!input_text">Запросить навыки</button>
        </form>
      </section>


      <section class="skills-and-videos">
        <LoaderComponent v-if="loading_skills"></LoaderComponent>
        <div v-else class="skill-buttons">
          <button v-for="skill in skills" @click="load_videos_by_this_skill(skill)" :key="skill">
            {{ skill }}
          </button>
        </div>

        <div class="video-list" v-if="videos.length > 0">
          <h2>Videos for {{ current_skill }}</h2>
          <ul>
            <li v-for="(video, k) in videos" :key="k">
              <VideoCard :video="video"></VideoCard>
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
import { useAuthStore } from '../store/useAuthStore';
import VideoCard from '../components/VideoCard.vue';
import LoaderComponent from '../components/Loader.vue'

export default {
  components: {
    VideoCard,
    LoaderComponent,
  },
  data() {
    return {
      loading_skills: false,
      current_skill: '',
      user_data: {},
      input_text: '',
      skills: [],
      videos: [],
    };
  },
  methods: {
    async load_videos_by_this_skill(skill) {
      const response = await this.$axios.get('/api/videos/${skill}/',{ params: {skill_name: skill}})

      this.videos = response.data.videos
    },
    logout() {

      const store = useAuthStore();

      store.removeToken();

      this.$router.push('/')
    },
    async submit() {
      try {
        this.loading_skills = true

        const response = await this.$axios.get('/api/skill/' + this.input_text)
        this.skills = response.data.skills
      } catch (error) {
        console.error(error)
      } finally {
        this.loading_skills = false
      }
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