import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import AxiosPlugin from './plugins/axios';
import { createPinia } from 'pinia';

const app = createApp(App)

app.use(AxiosPlugin)

const pinia = createPinia()

app.use(pinia)

app.use(router)

app.mount('#app')
