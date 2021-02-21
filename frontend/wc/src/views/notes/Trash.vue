<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="trash-description"
    >
      <v-row>
        <v-col
          class="pl-6"
        >
          {{ $t('memo.TRASH_DESCRIPTION') }}
        </v-col>
        <v-col
          class="trash-button"
        >
          <v-btn
            dark
            color="blue-grey darken-2"
            @click="emptyTrash()"
          >
            {{ $t('memo.EMPTY_TRASH') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>

    <v-container
      class="content"
    >
      <v-simple-table>
        <tbody>
          <tr
            v-for="memo in memos"
            :key="memo.id"
          >
            <td>
              <DocIcon
                :doctype="memo.doctype"
                color="blue-grey"
              />
              {{ memo.title }}
              <div
                class="ml-7"
                v-if="isMobile"
              >
                {{ getDateOrTime(memo.date_or_time) }}
              </div>
            </td>
            <td
              width="120"
              v-if="!isMobile"
            >
              {{ getDateOrTime(memo.date_or_time) }}
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
                  <v-list-item
                    @click="restoreMemo(memo)"
                  >
                    <v-list-item-content>
                      <v-list-item-title>
                        <v-icon
                          class="mr-1"
                        >
                          mdi-restore
                        </v-icon>
                        {{ $t('memo.RESTORE_FROM_TRASH') }}
                      </v-list-item-title>
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
import Mobile from '@/mixins/mobile'
import DocIcon from '@/components/DocIcon'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
  components: {
    DocIcon
  },
  data () {
    return {
      memos: '',
      firstInit: false
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.getTrash()
  },
  methods: {
    getTrash: function () {
      var vm = this

      axios({
        method: this.$api('NOTES_TRASH_MEMOS').method,
        url: this.$api('NOTES_TRASH_MEMOS').url
      })
      .then(function (response) {
        vm.memos = response.data['data']
        vm.firstInit = true
      })
      .catch(function () {
      })
    },
    restoreMemo: function (memo) {
      var vm = this

      axios({
        method: this.$api('NOTES_RESTORE_MEMO').method,
        url: this.$api('NOTES_RESTORE_MEMO').url.replace(
          '{pk}', memo.id
        )
      })
      .then(function () {
        var index = vm.memos.indexOf(memo)
        vm.memos.splice(index, 1)

        vm.$dialog.notify.success(
          vm.$t('memo.RESTORED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function () {
      })
    },
    emptyTrash: function () {
      if (!this.memos.length) {
        return
      }

      var vm = this

      axios({
        method: this.$api('NOTES_EMPTY_TRASH_MEMOS').method,
        url: this.$api('NOTES_EMPTY_TRASH_MEMOS').url
      })
      .then(function () {
        vm.memos = []
        vm.$dialog.notify.success(
          vm.$t('common.DELETED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function () {
      })
    }
  }
}
</script>

<style lang="scss">
.trash-description {
  background-color:#eee;
  padding:0;
}
.trash-button {
  max-width:150px;
}
.trash-button button {
  min-height:95%;
}
</style>
