import { createRouter, createWebHistory } from 'vue-router';
import Units from '../components/Units.vue';
import App from  '../App.vue'

const routes = [
  { path: '/', component: App },
  { path: '/units', component: Units },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
