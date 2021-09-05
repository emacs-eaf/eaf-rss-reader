<template>
  <div id="app">
    <transition name="slide" mode="out-in">
      <router-view :key="$route.path"/>
    </transition>
  </div>
</template>

<script>
import test from './components/test.vue'

export default ({
  components: {
    test
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

  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;

  position: relative;
}

#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: lightseagreen;
  padding: 0 10px;
}

#nav a.router-link-exact-active {
  color: #9966ff;
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
