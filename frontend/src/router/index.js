import { createRouter, createWebHistory } from 'vue-router';
import Wimhof from '../components/Wimhof.vue';
import App from  '../App.vue'

const routes = [
  { path: '/', component: App },
  { path: '/wimhof', component: Wimhof },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
