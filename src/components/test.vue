<template>
  <div ref="test" class="test">
    <div v-for="x in 10" :key="x">
      <h1>hello</h1>
    </div>
    <button type="button" v-on:click="scrollUp()">Up</button>
    <button type="button" v-on:click="scrollDown()">Down</button>
    <div v-for="x in 10" :key="x">
      <h1>hello</h1>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Test',
  data() {
    return {
      
    }
  },
  created() {
  },
  mounted() {
		window.scrollUp = this.scrollUp;
    window.scrollDown = this.scrollDown;
  },
  
  methods: {
    scrollUp() {
			this.$refs.test.scrollTop += 30;
			// document.documentElement.scrollTop += 30;
			console.log(this.$refs.test.scrollTop);
    },
    scrollDown() {
			this.$refs.test.scrollTop -= 30;
			// document.documentElement.scrollTop -= 30;
			// this.$refs.scro.scrollTop -= 30;
			console.log(this.$refs.test.scrollTop);
    }
  }
}
</script>


<style scoped>
.test {
  padding: 10px;
  white-space: nowrap;
  text-overflow: ellipsis;
	width: 100%;
  height: 100%;
}

</style>