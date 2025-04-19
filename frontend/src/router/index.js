import { createRouter, createWebHistory } from 'vue-router';
import Home from '../components/Home.vue';
import About from '../components/About.vue';
import Lab0 from '../components/Lab0.vue';
import TychoStation from "../components/TychoStation.vue";
import Bushido from '../components/Bushido.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
  { path: '/lab0', component: Lab0 },
  { path: '/tycho-station', component: TychoStation },
  { path: '/bushido', component: Bushido },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
