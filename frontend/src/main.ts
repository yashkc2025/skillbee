import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import 'bootstrap-icons/font/bootstrap-icons.css'

import App from './App.vue'
import router from './router'
import VueCalendarHeatmap from 'vue3-calendar-heatmap'
import 'vue3-calendar-heatmap/dist/style.css'

const app = createApp(App)

app.use(VueCalendarHeatmap)
app.use(createPinia())
app.use(router)

app.mount('#app')
