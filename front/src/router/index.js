import { createRouter, createWebHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import MainView from '../views/MainView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      redirect: '/login'
      
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/main',
      name: 'main',
      component: MainView,
      meta: {requiresAuth: true}
    }
  ]
})

router.beforeEach((to, from, next) => {
  const loggedIn = localStorage.getItem('accessToken');
  if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
    // Redirect to login page if not logged in
    next('/login');
  } else {
    next();
  }
});

export default router
