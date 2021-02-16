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
      name: 'notes.memoMenu',
      params: {
        menu: 1
      }
    }
  },
  {
    path: '/notes/memo/:menu',
    name: 'notes.memoMenu',
    component: () => import(
      /* webpackChunkName: "notes" */ '../views/notes/Memo.vue'
    )
  },
  {
    path: '/notes/memo/edit/:menu/:pk',
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
