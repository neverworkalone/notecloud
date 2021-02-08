<template>
  <div
    v-if="initialized"
  >
  <v-container
    class="content pt-0"
  >

  <v-simple-table>
    <tbody>
      <tr
        v-for="memo in memos"
        :key="memo.id"
      >
        <td>
          <div>
            <v-icon
              color="info"
              class="mr-5"
            >
              mdi-text-box-outline
            </v-icon>
            {{ memo.title }}
            <div
              class="ml-12"
              v-if="isMobile"
            >
              {{ printDateOrTime(memo.date_or_time) }}
            </div>
          </div>
        </td>
        <td
          width="120"
          v-if="!isMobile"
        >
          {{ printDateOrTime(memo.date_or_time) }}
        </td>
        <td
          width="60"
          class="ma-0 pa-0"
        >
          <v-menu
            transition="slide-y-transition"
            bottom
            offset-y
            class="mx-auto"
          >
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                small
                text
                class="ml-auto"
                v-bind="attrs"
                v-on="on"
              >
                <v-icon>mdi-dots-vertical</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item>
                <v-list-item-content>
                  <v-list-item-title>
                    <v-icon
                      class="mr-1"
                    >
                      mdi-link-variant
                    </v-icon>
                    {{ $t('memo.COPY_MEMO_LINK') }}
                  </v-list-item-title>
                </v-list-item-content>
              </v-list-item>
              <v-list-item
                two-line
              >
                <v-list-item-content>
                  <v-list-item-title>
                    <v-icon
                      color="info"
                      class="mr-1"
                    >
                      mdi-account-multiple-outline
                    </v-icon>
                    <font color="#1976D2">
                      {{ $t('memo.SHARE_MEMO') }}
                    </font>
                  </v-list-item-title>
                  <v-list-item-subtitle
                    class="ml-8"
                  >
                    {{ $t('memo.SHARE_MEMO_DESCRIPTION') }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-divider></v-divider>
              <v-list-item
                two-line
              >
                <v-list-item-content>
                  <v-list-item-title>
                    <v-icon
                      color="error"
                      class="mr-1"
                    >
                      mdi-trash-can-outline
                    </v-icon>
                    <font color="error">
                      {{ $t('memo.DELETE_MEMO') }}
                    </font>
                  </v-list-item-title>
                  <v-list-item-subtitle
                    class="ml-8"
                  >
                    {{ $t('memo.DELETE_MEMO_DESCRIPTION') }}
                  </v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-menu>
        </td>
      </tr>
    </tbody>
  </v-simple-table>
</v-container>

  </div>
</template>

<script>
import axios from 'axios'
import FormatDate from '@/mixins/formatDate'

export default {
  mixins: [
    FormatDate
  ],
  data () {
    return {
      memos: '',
      isMobile: false,
      firstInit: false
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.onResize()
    window.addEventListener('resize', this.onResize, { passive: true })

    this.getMemo()
  },
  methods: {
    printDateOrTime: function (dateOrTime) {
      if (dateOrTime.date) {
        return this.formatDate(dateOrTime.date)
      }
      else {
        return dateOrTime.time
      }
    },
    getMemo: function () {
      var vm = this

      axios({
        method: this.$api('NOTES_MEMOS').method,
        url: this.$api('NOTES_MEMOS').url
      })
      .then(function (response) {
        vm.memos = response.data['data']
        vm.firstInit = true
      })
      .catch(function () {
      })
    },
    onResize () {
      this.isMobile = window.innerWidth < 600
    }
  }
}
</script>
