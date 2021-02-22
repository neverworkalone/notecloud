export default [
  {
    path: '/notes/tasks',
    name: 'notes.tasks',
    meta: { requiresAuth: true },
    component: () => import(
      /* webpackChunkName: "checkcheck" */ '../views/notes/Tasks.vue'
    )
  },
  {
    path: '/notes/memo',
    name: 'notes.memo',
    redirect: {
      name: 'notes.memoPage',
      params: {
        menu: 1,
        page: 1
      }
    }
  },
  {
    path: '/notes/memo/:menu/:page',
    name: 'notes.memoPage',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Memo.vue'
    )
  },
  {
    path: '/notes/memo/edit/:menu/:page/:pk',
    name: 'notes.editMemo',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import(
      /* webpackChunkName: "editNotes" */ '../views/notes/EditMemo.vue'
    )
  },
  {
    path: '/notes/memo/new',
    name: 'notes.newMemo',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import(
      /* webpackChunkName: "editNotes" */ '../views/notes/NewMemo.vue'
    )
  },
  {
    path: '/notes/memo/trash',
    name: 'notes.trash',
    meta: { requiresAuth: true, requiresPrime: true },
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Trash.vue'
    )
  }
]
