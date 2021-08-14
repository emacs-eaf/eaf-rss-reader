<template>
  <div id="app">
    <TheNavigation />
    <transition name="slide" mode="out-in">
      <router-view :key="$route.path"/>
    </transition>
  </div>
</template>

<script>
import TheNavigation from '@/components/TheNavigation'

export default ({
  components: {
    TheNavigation
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: black;
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
</style>
