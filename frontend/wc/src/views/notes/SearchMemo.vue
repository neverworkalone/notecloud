<template>
  <div class="content">
  </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  mounted () {
    this.$router.push({
      name: 'notes.memoPage',
      params: {
        menu: 1,
        page: 1
      },
      query: {
        q: this.$route.params.q
      }
    })
  }
}
</script>
