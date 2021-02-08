export default [
  {
    path: '/notes/tasks',
    name: 'notes.tasks',
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Tasks.vue'
    )
  },
  {
    path: '/notes/memo',
    name: 'notes.memo',
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Memo.vue'
    )
  }
]
