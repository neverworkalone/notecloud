<template>
<v-container>
  <SettingMenu/>

  <div
    class="content text-center"
  >
    <v-form
      v-model="validation"
    >

      <v-row justify="center">
        <v-col
          cols="50"
          md="6"
        >
          <v-text-field
            v-model="user.username"
            :label="$t('accounts.USERNAME')"
            disabled
          >
          </v-text-field>
        </v-col>
      </v-row>

    </v-form>
  </div>

</v-container>
</template>

<script>
import SettingMenu from '../../components/SettingMenu'
import { mapState } from 'vuex';

export default {
  components: {
    SettingMenu,
  },

  data () {
    return {
      firstInit: false,
      validation: false,
      rules: {
        required: v => !!v || this.$t('common.REQUIRED'),
        emailRules: v => /^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$/.test(v) || this.$t('common.INVALID_EMAIL'),
      },
    }
  },
  computed: {
    ...mapState([
      'user'
    ])
  }
}
</script>
