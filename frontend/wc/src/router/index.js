import Vue from 'vue'
import VueRouter from 'vue-router'

import AccountsRoutes from '@/router/accounts'
import NotesRoutes from '@/router/notes'
import ForumsRoutes from '@/router/forums'

import { store } from '@/store'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'landing',
    component: () => import('../views/Landing.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/opennote/:pk',
    name: 'notes.sharedMemo',
    component: () => import('../views/notes/SharedMemo.vue')
  },
  ...AccountsRoutes,
  ...NotesRoutes,
  ...ForumsRoutes,
]

const router = new VueRouter({
  routes,
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!store.getters.isApproved) {
      next({ name: 'accounts.login' })
    }
    else if (
      to.matched.some(record => record.meta.requiresPrime) &&
      !store.getters.isPrime
    ) {
      next() // TODO: BETA_VERSION - redirect to prime page
    }
    else {
      next()
    }
  }
  else {
    next()
  }
})

export default router
