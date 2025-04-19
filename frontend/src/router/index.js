import { createRouter, createWebHistory } from 'vue-router';
import Home from '../App.vue';
import Units from '../components/Units.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/units', component: Units },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
