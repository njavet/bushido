import { createRouter, createWebHistory } from 'vue-router';
import App from  '../App.vue'
import Units from "../components/Units.vue";
import Wimhof from '../components/Wimhof.vue';

const routes = [
  { path: '/', component: App},
  { path: '/units', component: Units },
  { path: '/wimhof', component: Wimhof },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
