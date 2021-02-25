<template>
  <v-container>

    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <template>
        <v-list-item
          one-line
          v-if="user"
        >
          <v-list-item-avatar>
            <v-icon
            >
              mdi-account
            </v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>{{ username }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-list-item
          v-else
        >
          <v-list-item-avatar>
            <v-icon>mdi-account</v-icon>
          </v-list-item-avatar>

          <v-list-item-content>
            <v-list-item-title>
              <router-link :to="{ name: 'accounts.login' }">
                {{ $t('accounts.LOGIN') }}
              </router-link>
            </v-list-item-title>
          </v-list-item-content>
        </v-list-item>

        <v-divider></v-divider>

        <v-list
          nav
          dense
        >
          <v-list-item-group>
            <v-list-item
              v-for="(m, i) in menu"
              :key="i"
            >
              <v-list-item-icon>
                <v-icon v-text="m.icon"></v-icon>
              </v-list-item-icon>
              <v-list-item-content>
                <router-link :to="m.to">
                  <v-list-item-title v-text="m.text"></v-list-item-title>
                </router-link>
              </v-list-item-content>
            </v-list-item>

          </v-list-item-group>
        </v-list>

      </template>
    </v-navigation-drawer>

    <v-app-bar
      class="nav"
      app
    >
      <v-app-bar-nav-icon
        @click.stop="drawer = !drawer"
      >
      </v-app-bar-nav-icon>

      <Logo
        :to="{ name: 'notes.tasks' }"
      />

      <v-spacer></v-spacer>

      <v-text-field
        id="search"
        ref="search"
        v-model="search"
        outlined
        dense
        single-line
        clearable
        hide-details
        prepend-inner-icon="mdi-magnify"
        :placeholder="$t('common.SEARCH')"
        class="ml-8"
        @blur="onBlur"
        @keydown.esc="onEsc"
        @keydown.enter="onEnter"
      >
      </v-text-field>

    </v-app-bar>

  </v-container>
</template>

<script>
import Logo from '@/components/Logo'
import { mapState } from 'vuex'

export default {
  name: 'Navigation',
  components: {
    Logo
  },
  data () {
    return {
      drawer: null,
      search: '',
    }
  },
  computed: {
    ...mapState([
      'user'
    ]),
    username: function () {
      return this.user.username
    },
    menu: function () {
      var menuList = []

      menuList.push(
        {
          text: this.$t('info.PRODUCT'),
          icon: 'mdi-home-outline',
          to: { name: 'home' }
        },
        {
          text: this.$t('info.CONTACT'),
          icon: 'mdi-help',
          to: { name: 'forums.contact' }
        }
      )

      if (this.user) {
        menuList.push(
          {
            text: this.$t('info.CHECK'),
            icon: 'mdi-check',
            to: { name: 'notes.tasks' }
          }
        )
      }

      if (this.user) { // TODO: BETA_VERSION - check prime
        menuList.push(
          {
            text: this.$t('info.MEMO'),
            icon: 'mdi-text-box-outline',
            to: { name: 'notes.memo' }
          }
        )
        menuList.push(
          {
            text: this.$t('memo.MEMO_TRASH'),
            icon: 'mdi-trash-can-outline',
            to: { name: 'notes.trash' }
          }
        )
      }

      if (this.user) {
        menuList.push(
          {
            text: this.$t('accounts.SETTING'),
            icon: 'mdi-cog',
            to: { name: 'accounts.profile' }
          },
          {
            text: this.$t('accounts.LOGOUT'),
            icon: 'mdi-logout',
            to: { name: 'accounts.logout' }
          }
        )
      }
      return menuList
    }
  },
  beforeDestroy () {
    document.onkeydown = null
  },
  methods: {
    onBlur () {
      this.resetSearch()
    },
    onEsc () {
      this.resetSearch()
      this.$refs.search.blur()
    },
    resetSearch () {
      this.$nextTick(() => (this.search = undefined))
    },
    onEnter () {
      this.searchAnything(this.search)
    },
    searchAnything(anything) {
      // TODO: implement search
      window.console.log(anything)
      this.onBlur()
    }
  }
}
</script>

<style lang="scss">
.nav {
  a {
    color: #2c3e50;

    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.v-list-item {
  min-height:30px;

  a {
    color: rgba(0, 0, 0, 0.88) !important;
    text-decoration: none;
  }
  a:hover {
    color: #c0341d !important;
    text-decoration: underline;
  }
}
</style>
