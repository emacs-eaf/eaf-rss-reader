<template>
  <div id="app">
    <transition name="slide" mode="out-in">
      <router-view :key="$route.path"/>
    </transition>
  </div>
</template>

<script>
<<<<<<< HEAD

export default ({
  components: {
=======
import test from './components/test.vue'

export default ({
  components: {
    test
>>>>>>> 936291adf39121e1c2f26dcbd3078b3a012b1e0e
  },
  mounted() {
		window.addFiles = this.addFiles;
	},
  created() {
		this.$store.dispatch('getList');
	},
  methods: {
    addFiles(files) {
			this.$store.commit("updateFileInfos", files);
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
<<<<<<< HEAD
=======

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;

  position: relative;
}
>>>>>>> 936291adf39121e1c2f26dcbd3078b3a012b1e0e

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
