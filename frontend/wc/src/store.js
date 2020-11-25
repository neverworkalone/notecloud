import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    key: '',
    user: '',
    login_device: ''
  },
  mutations: {
    updateUser(state, payload) {
      state.key = payload.key
      state.user = payload.user
      state.login_device = payload.login_device
    },
    removeUser(state) {
      state.key = ''
      state.user = ''
      state.login_device = ''
    }
  }
})
