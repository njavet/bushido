import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
import router from './router'
import 'tabulator-tables/dist/css/tabulator.min.css'
createApp(App).use(router).mount('#app')
