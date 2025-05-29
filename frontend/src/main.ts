import './assets/main.css'
import { createPinia } from 'pinia'
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'


const pinia = createPinia()
const app = createApp(App)

app.use(router).use(pinia)

app.mount('#app')
