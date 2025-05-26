import { createRouter, createWebHistory } from 'vue-router'
import MathGame from '../components/MathGame.vue'
import About from '../components/About.vue'

const routes = [
  { path: '/', component: MathGame },
  { path: '/about', component: About }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
