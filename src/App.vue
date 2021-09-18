<template>
  <div id="app">
    <Main></Main>
  </div>
</template>

<script>
import Main from "@/components/Main.vue"
export default ({
  components: {
    Main
  },
  mounted() {
		window.addFeedsListFiles = this.addFeedsListFiles;
    window.addFeedsLinkListFiles = this.addFeedsLinkListFiles;
	},
  created() {
		this.$store.dispatch('getList');
	},
  methods: {
    addFeedsListFiles(files) {
			this.$store.commit("updateFeedsList", files);
		},
    addFeedsLinkListFiles(files) {
			this.$store.commit("updateFeedsLinkList", files);
		},
  }
  
})
</script>


<style>
html, body {
   width: 100%;
   height: 100%;
   margin: 0;
   padding: 0;
 }
 
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;

  display: flex;
  flex-direction: column;
  
  width: 100%;
  height: 100%;

  position: relative;
}


.slide-enter-active,
.slide-leave-active {
  transition : opacity 0.25s, transform 0.25s;
}

.slide-enter,
.slide-leave-to {
  opacity: 0;
  transform: translatX(-30);
}

::-webkit-scrollbar {
  display: none;
}

.test {
  overflow: scroll;
}
</style>
