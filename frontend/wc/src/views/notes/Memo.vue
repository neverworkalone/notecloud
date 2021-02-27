<template>
  <div
    v-if="initialized"
  >

    <v-bottom-navigation
      v-model="menuIndex"
      background-color="#ECEFF1"
      class="mb-5"
      color="primary"
      shift
      grow
    >
      <v-btn
        :to="{ name: 'notes.newMemo' }"
      >
        <span>{{ $t('memo.NEW_MEMO') }}</span>
        <v-icon>mdi-plus-thick</v-icon>
      </v-btn>

      <v-btn
        @click="getMemos()"
      >
        <span>{{ $t('memo.MEMO_LIST') }}</span>
        <v-icon>mdi-text-box-outline</v-icon>
      </v-btn>

      <v-btn
        @click="getMemos($const('MEMO_MENU_PINNED'))"
      >
        <span>{{ $t('memo.MEMO_PINNED') }}</span>
        <v-icon>mdi-pin-outline</v-icon>
      </v-btn>

      <v-btn
        @click="getMemos($const('MEMO_MENU_SHARED'))"
      >
        <span>{{ $t('memo.MEMO_SHARED') }}</span>
        <v-icon>mdi-account-multiple-outline</v-icon>
      </v-btn>
    </v-bottom-navigation>

    <v-container
      class="content pt-0"
    >
      <v-dialog
        v-model="copyLinkDialog"
        transition="dialog-bottom-transition"
        width="90%"
        :max-width="$const('MEMO_LINK_MAX_WIDTH')"
      >
        <template v-slot:activator="{ on, attrs }">

          <v-simple-table>
            <tbody>
              <tr
                v-for="memo in memos"
                :key="memo.id"
              >
                <td>
                  <div
                    @click="editMemo(memo)"
                    style="cursor: pointer;"
                  >
                    <DocIcon
                      :doctype="memo.doctype"
                    />
                    {{ memo.title }}

                    <div
                      class="ml-7"
                      v-if="isMobile"
                    >
                      {{ getDateOrTime(memo.date_or_time) }}
                      <v-icon
                        small
                        color="info"
                        v-if="memo.is_shared"
                      >
                        mdi-account-multiple-outline
                      </v-icon>
                      <v-icon
                        small
                        color="info"
                        v-if="memo.is_pinned"
                      >
                        mdi-pin-outline
                      </v-icon>
                    </div>
                  </div>
                </td>
                <td
                  width="50"
                  v-if="!isMobile"
                  class="pa-0"
                >
                  <v-icon
                    v-if="memo.is_shared"
                  >
                    mdi-account-multiple-outline
                  </v-icon>
                  <v-icon
                    v-if="memo.is_pinned"
                  >
                    mdi-pin-outline
                  </v-icon>
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
                        v-bind="attrs"
                        v-on="on"
                        @click="copyLink(memo)"
                        v-if="menuIndex == $const('MEMO_MENU_SHARED') && memo.is_shared"
                      >
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
                        @click="pinMemo(memo, unpin=true)"
                        v-if="memo.is_pinned"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            <v-icon
                              class="mr-1"
                            >
                              mdi-pin-off-outline
                            </v-icon>
                            {{ $t('memo.UNPIN_MEMO') }}
                          </v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item
                        @click="pinMemo(memo)"
                        v-else
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            <v-icon
                              class="mr-1"
                            >
                              mdi-pin-outline
                            </v-icon>
                            {{ $t('memo.PIN_MEMO') }}
                          </v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>

                      <v-list-item
                        @click="shareMemo(memo, unshare=true)"
                        v-if="memo.is_shared"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            <v-icon
                              class="mr-1"
                            >
                              mdi-account-multiple-remove-outline
                            </v-icon>
                            {{ $t('memo.UNSHARE_MEMO') }}
                          </v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item
                        two-line
                        @click="shareMemo(memo)"
                        v-else
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            <v-icon
                              class="mr-1"
                            >
                              mdi-account-multiple-outline
                            </v-icon>
                            {{ $t('memo.SHARE_MEMO') }}
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
                        @click="deleteMemo(memo)"
                      >
                        <v-list-item-content>
                          <v-list-item-title>
                            <v-icon
                              class="mr-1"
                            >
                              mdi-trash-can-outline
                            </v-icon>
                            {{ $t('memo.DELETE_MEMO') }}
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

        </template>

        <v-container
          class="text-center"
        >
          <v-card>
            <v-card-title>
              {{ $t('memo.SCAN_QR_CODE') }}
            </v-card-title>
            <vue-qrcode
              id="qrImage"
              :width="$const('QR_CODE_WIDTH')"
              :value="qrValue"
              :margin="0"
            />
            <v-card-subtitle
              class="pb-0"
            >
              <v-text-field
                id="opennoteURL"
                v-model="qrValue"
                outlined
                dense
                readonly
              >
              </v-text-field>
            </v-card-subtitle>
            <v-card-actions
            >
              <v-tooltip
                top
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-icon
                    v-bind="attrs"
                    v-on="on"
                  >mdi-help-circle-outline</v-icon>
                </template>
                <span>{{ $t('memo.SCAN_QR_CODE_DESCRIPTION') }}</span>
              </v-tooltip>
              <v-spacer></v-spacer>
              <v-btn
                depressed
                @click="copyLinkToClipboard()"
              >
                {{ $t('memo.COPY_MEMO_LINK') }}
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-container>

      </v-dialog>

    </v-container>

    <Pagination
      :pagination="pagination"
      :first="firstPage"
      :prev="prevPage"
      :next="nextPage"
    />

  </div>
</template>

<script>
import axios from 'axios'
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'
import DocIcon from '@/components/DocIcon'
import Pagination from '@/components/Pagination'
import VueQrcode from 'vue-qrcode'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
  components: {
    DocIcon,
    Pagination,
    VueQrcode
  },
  data () {
    return {
      pagination: {
        pageTotal: 1,
        currentPage: 1,
        firstLink: null,
        prevLink: null,
        nextLink: null
      },
      menuIndex: this.$const('MEMO_MENU_DEFAULT'),
      page: 1,
      memos: '',
      copyLinkDialog: false,
      qrValue: null,
      firstInit: false
    }
  },
  computed: {
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.menuIndex = this.$route.params.menu
    if (!this.menuIndex) {
      this.menuIndex = this.$const('MEMO_MENU_DEFAULT')
    }
    this.page = this.$route.params.page
    if (!this.page) {
      this.page = 1
    }

    this.getMemos(this.menuIndex, null, this.page, this.$route.query.q)
  },
  methods: {
    editMemo: function (memo) {
      this.$router.push({
        name: 'notes.editMemo',
        params: {
          menu: this.menuIndex,
          page: this.pagination.currentPage,
          pk: memo.id
        },
        query: {
          q: this.$route.query.q
        }
      })
    },
    firstPage: function () {
      this.getMemos(this.menuIndex, this.pagination.firstLink)
    },
    prevPage: function () {
      this.getMemos(this.menuIndex, this.pagination.prevLink)
    },
    nextPage: function () {
      this.getMemos(this.menuIndex, this.pagination.nextLink)
    },
    getMemos: function (index=1, url=null, page=0, q=null) {
      var vm = this
      var method = 'get'

      if (!page) {
        page = 1
      }

      if (!url) {
        var apiType = 'NOTES_MEMOS'

        if (index == this.$const('MEMO_MENU_PINNED')) {
          apiType = 'NOTES_PINNED_MEMOS'
        }
        else if (index == this.$const('MEMO_MENU_SHARED')) {
          apiType = 'NOTES_SHARED_MEMOS'
        }
        method = this.$api(apiType).method
        url = this.$api(apiType).url.replace(
          '{page}', page
        )

        if (q) {
          url += '&q=' + q
        }
      }

      axios({
        method: method,
        url: url
      })
      .then(function (response) {
        var pagination = response.data['pagination']
        vm.pagination.pageTotal = pagination['page_total']
        vm.pagination.currentPage = pagination['current_page']
        vm.pagination.prevLink = pagination['prev_link']
        vm.pagination.nextLink = pagination['next_link']
        vm.pagination.firstLink = pagination['first_link']

        vm.memos = response.data['data']
        vm.firstInit = true
      })
      .catch(function () {
      })
    },
    pinMemo: function (memo, unpin=false) {
      var vm = this
      var apiType = 'NOTES_PIN_MEMO'

      if (unpin) {
        apiType = 'NOTES_UNPIN_MEMO'
      }

      axios({
        method: this.$api(apiType).method,
        url: this.$api(apiType).url.replace(
          '{pk}', memo.id
        )
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.memos.length; i++) {
          if (vm.memos[i].id == data.id) {
            vm.memos[i].is_pinned = data.is_pinned
          }
        }

        var pinText = 'memo.MEMO_IS_PINNED'
        if (unpin) {
          pinText = 'memo.MEMO_IS_UNPINNED'
        }

        vm.$dialog.notify.success(
          vm.$t(pinText), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function () {
      })
    },
    shareMemo: function (memo, unshare=false) {
      var vm = this
      var apiType = 'NOTES_SHARE_MEMO'

      if (unshare) {
        apiType = 'NOTES_UNSHARE_MEMO'
      }

      axios({
        method: this.$api(apiType).method,
        url: this.$api(apiType).url.replace(
          '{pk}', memo.id
        )
      })
      .then(function (response) {
        var data = response.data['data']

        for (var i=0; i<vm.memos.length; i++) {
          if (vm.memos[i].id == data.id) {
            vm.memos[i].is_shared = data.is_shared
          }
        }

        var shareText = 'memo.MEMO_IS_SHARED'
        if (unshare) {
          shareText = 'memo.MEMO_NO_LONGER_SHARED'
        }

        vm.$dialog.notify.success(
          vm.$t(shareText), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
      .catch(function () {
      })
    },
    deleteMemo: function (memo) {
      var vm = this

      axios({
        method: this.$api('NOTES_DELETE_MEMO').method,
        url: this.$api('NOTES_DELETE_MEMO').url.replace(
          '{pk}', memo.id
        )
      })
      .then(function () {
        var index = vm.memos.indexOf(memo)
        vm.memos.splice(index, 1)

        vm.$dialog.notify.success(
          vm.$t('common.DELETED'), {
            position: 'bottom-right',
            timeout: 2000
          }
        )
      })
    },
    copyLink: function (memo) {
      var props = this.$router.resolve({
        name: 'notes.sharedMemo',
        params: {
          pk: memo.id
        }
      })
      this.qrValue = location.origin + props.href
    },
    copyLinkToClipboard: function () {
      document.querySelector("#opennoteURL").select()
      document.execCommand("Copy")

      this.$dialog.notify.success(
        this.$t('tasks.COPIED_TO_CLIPBOARD'), {
          position: 'bottom-right',
          timeout: 2000
        }
      )
    }
  }
}
</script>
