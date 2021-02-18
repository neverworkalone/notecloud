export default [
  {
    path: '/notes/tasks',
    name: 'notes.tasks',
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
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Memo.vue'
    )
  },
  {
    path: '/notes/memo/edit/:menu/:page/:pk',
    name: 'notes.editMemo',
    component: () => import(
      /* webpackChunkName: "editNotes" */ '../views/notes/EditMemo.vue'
    )
  },
  {
    path: '/notes/memo/new',
    name: 'notes.newMemo',
    component: () => import(
      /* webpackChunkName: "editNotes" */ '../views/notes/NewMemo.vue'
    )
  },
  {
    path: '/notes/memo/trash',
    name: 'notes.trash',
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Trash.vue'
    )
  }
]
