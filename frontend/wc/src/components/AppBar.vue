<template>
  <v-container>

    <v-app-bar
      class="nav"
      app
      flat
    >
      <Logo
        :to="{ name: 'home' }"
      />

      <v-spacer></v-spacer>

      <v-btn
        depressed
        class="pl-2 pr-2 mr-1"
        :to="{ name: 'home' }"
        v-if="!isMobile"
      >
        {{ $t('info.PRODUCT') }}
      </v-btn>
      <v-btn
        depressed
        class="pl-2 pr-2 mr-1"
        :to="{ name: 'home' }"
        v-if="!isMobile"
      >
        {{ $t('info.CONTACT') }}
      </v-btn>

      <v-divider
        vertical
        inset
        v-if="!isMobile"
      ></v-divider>

      <v-btn
        depressed
        class="pl-2 pr-2 ml-1"
        :to="{ name: 'accounts.login' }"
      >
        {{ $t('accounts.LOGIN') }}
      </v-btn>
      <v-btn
        color="primary"
        depressed
        class="pl-2 pr-2 ml-1"
        :to="{ name: 'accounts.signup' }"
      >
        {{ $t('accounts.SIGNUP') }}
      </v-btn>
    </v-app-bar>

  </v-container>
</template>

<script>
import Mobile from '@/mixins/mobile'
import Logo from '@/components/Logo'
import { mapState } from 'vuex'

export default {
  name: 'AppBar',
  mixins: [
    Mobile
  ],
  components: {
    Logo
  },
  computed: {
    ...mapState([
      'user'
    ]),
  },
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>

<style lang="scss">
.v-divider--vertical.v-divider--inset {
  max-height: calc(100% - 32px);
  margin-top: 16px;
}
</style>
