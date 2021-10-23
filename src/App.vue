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
   -webkit-font-smoothing: antialiased;
   -moz-osx-font-smoothing: grayscale;
   text-align: center;

   display: flex;
   flex-direction: column;

   width: 100%;
   height: 100%;
   position: relative;
 }

 ::-webkit-scrollbar {
   display: none;
 }

</style>
