export default [
  {
    path: '/notes/tasks',
    name: 'notes.tasks',
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Tasks.vue'
    )
  }
]
