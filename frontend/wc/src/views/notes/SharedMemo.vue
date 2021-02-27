<template>
  <div
    v-if="initialized"
  >

    <v-container
    >
      <h3>
        <DocIcon
          :doctype="memo.doctype"
        />
        {{ memo.title }}
      </h3>
    </v-container>

    <v-container
      class="text-right caption pt-0"
    >
       {{ formatDate(memo.updated_at) }}
    </v-container>

    <v-container
      class="content pa-0"
    >
      <TipTap
        class="mb-5"
        :options="options"
      />
    </v-container>

    <v-container
      class="content mb-5 text-center"
    >
      <v-dialog
        v-model="copyLinkDialog"
        transition="dialog-bottom-transition"
        width="90%"
        :max-width="$const('MEMO_LINK_MAX_WIDTH')"
      >

        <template v-slot:activator="{ on, attrs }">
          <v-btn
            color="primary"
            v-bind="attrs"
            v-on="on"
            @click="copyLink(memo)"
          >
            {{ $t('memo.SHARE_MEMO') }}
          </v-btn>
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

  </div>
</template>

<script>
import axios from 'axios'
import FormatDate from '@/mixins/formatDate'
import DocIcon from '@/components/DocIcon'
import TipTap from '@/components/TipTap'
import VueQrcode from 'vue-qrcode'

export default {
  mixins: [
    FormatDate
  ],
  components: {
    DocIcon,
    TipTap,
    VueQrcode
  },
  data () {
    return {
      options: {
        content: '',
        readonly: true
      },
      memo: '',
      copyLinkDialog: false,
      qrValue: null,
      firstInit: false
    }
  },
  computed: {
    updated_at () {
      return this.$t('editor.LAST_UPDATED_AT', {
        date_or_time: this.getDateOrTime(this.memo.date_or_time)
      })
    },
    initialized () {
      return this.firstInit
    }
  },
  mounted () {
    this.getSharedMemo(this.$route.params.pk)
  },
  methods: {
    getSharedMemo: function (pk) {
      var vm = this

      axios({
        method: this.$api('NOTES_SHARED_MEMO').method,
        url: this.$api('NOTES_SHARED_MEMO').url.replace(
          '{pk}', pk
        )
      })
      .then(function (response) {
        vm.memo = response.data['data']
        vm.options.content = vm.memo.content
        vm.firstInit = true
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
