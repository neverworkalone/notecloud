<template>
  <div
    class="content text-center"
  >
    <v-progress-circular
      :size="70"
      :width="7"
      indeterminate
      color="#4CAF50"
    ></v-progress-circular>
  </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  mounted () {
    this.$router.replace({
      name: 'notes.taskList',
      query: {
        page: 1,
        q: this.$route.params.q
      }
    })
  }
}
</script>
