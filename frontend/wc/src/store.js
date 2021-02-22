import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export const store = new Vuex.Store({
  state: {
    key: '',
    user: '',
    login_device: '',
    date_format: ''
  },
  getters: {
    isApproved: state => {
      return state.user && state.user.is_approved
    },
    isPrime: state => {
      return state.user && state.user.is_approved && state.user.is_prime
    },
    isStaff: state => {
      return state.user && state.user.is_staff
    }
  },
  mutations: {
    updateUser(state, payload) {
      if (payload.key) {
        state.key = payload.key
      }
      if (payload.user) {
        state.user = payload.user
      }
      if (payload.login_device) {
        state.login_device = payload.login_device
      }
      if (payload.date_format) {
        state.date_format = payload.date_format
      }
    },
    removeUser(state) {
      state.key = ''
      state.user = ''
      state.login_device = ''
      state.date_format = ''
    }
  }
})
