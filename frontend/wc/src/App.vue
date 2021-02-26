<template>

  <v-app v-if="initialized">
    <Navigation
      v-if="user"
    />
    <AppBar
      v-else
    />

    <v-main>
      <v-container fluid>
        <v-fade-transition appear
          :hide-on-leave="true"
        >
          <router-view/>
        </v-fade-transition>
      </v-container>
    </v-main>

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

<script>
import AppBar from './components/AppBar'
import Navigation from '@/components/Navigation'
import Footer from '@/components/Footer'
import axios from 'axios'
import { mapState } from 'vuex'

export default {
  name: 'App',

  components: {
    AppBar,
    Navigation,
    Footer,
  },

  data () {
    return {
      firstInit: false,
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    document.title = this.$t('info.SITENAME')

    var vm = this
    var local_key = localStorage.getItem('token')
    axios.defaults.baseURL = this.$baseURL()

    var date_format = localStorage.getItem('date_format')
    if (!date_format) {
      date_format = this.$const('DATE_FORMAT_DEFAULT')
      localStorage.setItem('date_format', date_format)
    }

    if (local_key) {
      axios({
        method: this.$api('ACCOUNTS_CONNECT').method,
        url: this.$api('ACCOUNTS_CONNECT').url,
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
          login_device: response.data['data']['login_device'],
          date_format: date_format
        })

        vm.firstInit = true
      })
      .catch(function (error) {
        if (error.response.status === 401) {
          localStorage.clear()
        }
        vm.firstInit = true
      })
    }
    else {
      this.firstInit = true
    }
  }
}
</script>

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
