import Vue from 'vue'
import VueRouter from 'vue-router'

import AccountsRoutes from '@/router/accounts'
import NotesRoutes from '@/router/notes'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: {
      name: 'notes.tasks'
    }
  },
  ...AccountsRoutes,
  ...NotesRoutes,
  {
    path: '/opennote/:pk',
    name: 'notes.sharedMemo',
    component: () => import(
      /* webpackChunkName: "openNotes" */ '../views/notes/SharedMemo.vue'
    )
  },
]

const router = new VueRouter({
  routes,
})

export default router
