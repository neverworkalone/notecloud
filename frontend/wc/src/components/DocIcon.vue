<template>
  <v-icon
    :color="iconColor"
    class="mr-1"
  >
    {{ docIcon(doctype) }}
  </v-icon>
</template>

<script>
export default {
  props: {
    doctype: String,
    color: String
  },
  data () {
    return {
    }
  },
  computed: {
    iconColor () {
      if (this.color) {
        return this.color
      }
      return 'info'
    }
  },
  methods: {
    docIcon: function (doctype) {
      switch(doctype) {
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
    }
  }
}
</script>
