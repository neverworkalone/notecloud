<template>

  <v-app v-if="initialized">
    <Navigation/>

    <v-content>
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-content>

    <Footer/>
  </v-app>

  <div class="uninitialized" v-else>
    <v-progress-circular
      :size="70"
      :width="7"
      indeterminate
      color="#4CAF50"
    ></v-progress-circular>
  </div>

</template>

<style lang="scss">
#app {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

.content {
  padding: 20px;
}

.uninitialized {
  text-align:center;
  margin:5em;
}
</style>

<script>
import Navigation from './components/Navigation'
import Footer from './components/Footer'
import axios from 'axios'

export default {
  name: 'App',

  components: {
    Navigation,
    Footer,
  },

  data () {
    return {
      first_init: false,
    }
  },
  computed: {
    initialized () {
      return this.first_init
    }
  },
  mounted () {
    var vm = this
    var local_key = localStorage.getItem('token')
    axios.defaults.baseURL = this.$apiURL()

    if (local_key) {
      axios({
        method: 'post',
        url: '/accounts/connect/',
        headers: {
          Authorization: 'Token ' + local_key
        }
      })
      .then(function (response) {
        axios.defaults.headers.common['Authorization'] = 'Token ' + local_key

        vm.$store.commit({
          type: 'updateUser',
          key: local_key,
          user: response.data['data']['user'],
          login_device: response.data['data']['login_device']
        })

        vm.first_init = true
      })
      .catch(function (error) {
        if (error.response.status === 401) {
          localStorage.removeItem('token')
        }
        this.first_init = true
      })
    }
    else {
      this.first_init = true
    }
  }
}
</script>
