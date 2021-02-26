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
      name: 'notes.taskList',
      query: {
        page: 1,
        q: this.$route.params.q
      }
    })
  }
}
</script>
