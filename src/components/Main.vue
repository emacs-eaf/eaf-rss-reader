<template>
  <div class="page">
    <FeedsList class="feeds-list" ref="feedslist"/>
    <ArticlesList class="articles-list" ref="articlelist" v-bind:pyobject=pyobject />
  </div>
</template>

<script>
 import { mapState, mapGetters } from 'vuex';
 import { QWebChannel } from "qwebchannel";
 import ArticlesList from "@/components/ArticlesList.vue"
 import FeedsList from "@/components/FeedsList.vue"

 export default {
   name: "Main",
   data () {
     return {
       pyobject: null
     };
   },
   computed: {
     ...mapState([
       'currentFeedIndex',
       'currentArticleIndex',
       'openFeed',
       'openArticle']),
     ...mapGetters(['currentFeedArticleList']),
   },
   watch: {
    currentFeedIndex: {
      // eslint-disable-next-line no-unused-vars
      handler: function(val, oldVal) {
        window.pyobject.update_current_feed_index(val);
      }
    },
    currentArticleIndex: {
      // eslint-disable-next-line no-unused-vars
      handler: function(val, oldVal) {
        window.pyobject.update_current_article_index(val);
      }
    }
  },
   components:{
     ArticlesList,
     FeedsList,
   },
   mounted() {
     window.selectPrevFeed = this.selectPrevFeed;
     window.selectNextFeed = this.selectNextFeed;
     window.selectPrevArticle = this.selectPrevArticle;
     window.selectNextArticle = this.selectNextArticle;
     window.selectFirstFeed = this.selectFirstFeed;
     window.selectLastFeed = this.selectLastFeed;
     window.selectFirstArticle = this.selectFirstArticle;
     window.selectLastArticle = this.selectLastArticle;
   },
   created() {
     // eslint-disable-next-line no-undef
     new QWebChannel(qt.webChannelTransport, channel => {
       window.pyobject = channel.objects.pyobject;
       this.pyobject = window.pyobject;
     });
   },
   methods: {
     articleInfoList(){
       return this.currentFeedArticleList.find(
         article => article.title === this.title
       )
     },
     selectNextFeed() {
       this.$refs.feedslist.selectFeedByIndex(this.currentFeedIndex + 1);
       this.$store.commit('changeCurrentArticleIndex', 0);
     },
     selectPrevFeed() {
       this.$refs.feedslist.selectFeedByIndex(this.currentFeedIndex - 1);
       this.$store.commit('changeCurrentArticleIndex', 0);
     },
     selectNextArticle() {
       if (this.currentFeedIndex != -1) {
        this.$refs.articlelist.selectArticleByIndex(this.currentArticleIndex + 1);
       }
     },
     selectPrevArticle() {
       if (this.currentFeedIndex != -1) {
        this.$refs.articlelist.selectArticleByIndex(this.currentArticleIndex - 1);
       }
     },
     selectFirstFeed() {
       this.$refs.feedslist.selectFeedByIndex(0);
       this.$store.commit('changeCurrentArticleIndex', 0);
     },
     selectLastFeed() {
       const last_index = this.$store.state.feedsList.length - 1;
       this.$refs.feedslist.selectFeedByIndex(last_index);
       this.$store.commit('changeCurrentArticleIndex', 0);
     },
     selectFirstArticle() {
       if (this.currentFeedIndex != -1) {
        this.$refs.articlelist.selectArticleByIndex(0);
       }
     },
     selectLastArticle() {
       if (this.currentFeedIndex != -1) {
        const last_index = this.$store.state.feedsList[this.currentFeedIndex].feed_article_list.length - 1;
        this.$refs.articlelist.selectArticleByIndex(last_index);
       }
     }
   }
 };
</script>

<style scoped>
 .page {
   width: 100%;
   height: 100%;
   display: flex;
   flex-direction: row;
 }

 .feeds-list {
   flex: 0 0 38.2%;
 }

 .articles-list {
   flex: 0 0 61.8%;
 }
</style>
