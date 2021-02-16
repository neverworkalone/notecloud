<template>
  <div
    v-if="initialized"
  >
    <v-container
      class="content pt-0"
    >
    </v-container>
  </div>
</template>

<script>
import axios from 'axios'
import FormatDate from '@/mixins/formatDate'
import Mobile from '@/mixins/mobile'

export default {
  mixins: [
    FormatDate,
    Mobile
  ],
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
    docIcon: function (memo) {
      switch(memo.doctype) {
        case 'code':
          return 'mdi-file-code-outline'
        case 'table':
          return 'mdi-table'
        case 'bullet':
          return 'mdi-format-list-bulleted'
        case 'order':
          return 'mdi-format-list-numbered'
        default:
          return 'mdi-text-box-outline'
      }
    },
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
    }
  }
}
</script>
