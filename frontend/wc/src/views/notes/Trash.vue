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
