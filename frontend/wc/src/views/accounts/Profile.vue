<template>
<v-container>
  <SettingMenu/>

  <div
    class="content text-center"
  >
    <v-row
      justify="center"
    >
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

    <v-row
      justify="center"
    >
      <v-col
        cols="50"
        md="6"
      >
        <v-radio-group v-model="dateFormat">
          <template v-slot:label>
            <div>
              {{ $t('accounts.DATE_FORMAT_LABEL') }}
            </div>
          </template>
          <v-radio
            v-for="format in this.$const('DATE_FORMAT')"
            :key="format"
            :label="format"
            :value="format"
          ></v-radio>
        </v-radio-group>
      </v-col>
    </v-row>

    <v-row
      justify="space-around"
      class="mt-10"
    >
      <v-spacer></v-spacer>
      <v-btn
        depressed
        small
        :to="{ name: 'accounts.deactivate' }"
      >
        <v-icon
          small
          class="mr-2"
        >
          mdi-human-greeting
        </v-icon>
        {{ $t('accounts.DEACTIVATE') }}
      </v-btn>
    </v-row>

  </div>

</v-container>
</template>

<script>
import SettingMenu from '@/components/SettingMenu'
import { mapState } from 'vuex'

export default {
  components: {
    SettingMenu,
  },

  data () {
    return {
      firstInit: false,
    }
  },
  computed: {
    ...mapState([
      'user',
      'date_format'
    ]),
    dateFormat: {
      get () {
        var format = this.date_format
        if (!format) {
          format = this.$const('DATE_FORMAT_DEFAULT')
          this.$store.commit({
            type: 'updateUser',
            date_format: format
          })
        }
        return format
      },
      set (format) {
        this.$store.commit({
          type: 'updateUser',
          date_format: format
        })
        localStorage.setItem('date_format', format)
      }
    }
  }
}
</script>
