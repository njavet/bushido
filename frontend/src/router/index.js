import { createRouter, createWebHistory } from 'vue-router';
import Units from '../components/Units.vue';

const routes = [
  { path: '/units', component: Units },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
