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
     };
   },
   computed: {
     ...mapState([
       'curFeedIndex',
       'curArticleIndex',
       'openFeed',
       'openArticle',
       'viewKey']),
     ...mapGetters(['curFeedArticleList']),
   },
   watch: {
    curFeedIndex: {
      handler: function(val, oldVal) {
        window.pyobject.vue_update_cur_feed_index(val);
      }
    },
    curArticleIndex: {
      handler: function(val, oldVal) {
        window.pyobject.vue_update_cur_article_index(val);
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
     window.giveCurFeedIndex = this.giveCurFeedIndex;
     window.giveCurArticleIndex = this.giveCurArticleIndex;
     window.giveViewKey = this.giveViewKey;
   },
   created() {
     // eslint-disable-next-line no-undef
     new QWebChannel(qt.webChannelTransport, channel => {
       window.pyobject = channel.objects.pyobject;
     });
   },
   methods: {
     articleInfoList(){
       return this.curFeedArticleList.find(
         article => article.title === this.title
       )
     },
     selectNextFeed() {
       this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex + 1);
       this.$store.commit('changeCurArticleIndex', 0);
     },
     selectPrevFeed() {
       this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex - 1);
       this.$store.commit('changeCurArticleIndex', 0);
     },
     selectNextArticle() {
       if (this.curFeedIndex != -1) {
        this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex + 1);         
       }
     },
     selectPrevArticle() {
       if (this.curFeedIndex != -1) {
        this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex - 1);
       }
     },
     selectFirstFeed() {
       this.$refs.feedslist.selectFeedByIndex(0);
       this.$store.commit('changeCurArticleIndex', 0);
     },
     selectLastFeed() {
       const last_index = this.$store.state.feedsList.length - 1;
       this.$refs.feedslist.selectFeedByIndex(last_index);
       this.$store.commit('changeCurArticleIndex', 0);
     },
     selectFirstArticle() {
       if (this.curFeedIndex != -1) {
        this.$refs.articlelist.selectArticleByIndex(0); 
       }
     },
     selectLastArticle() {
       if (this.curFeedIndex != -1) {
        const last_index = this.$store.state.feedsList[this.curFeedIndex].feed_article_list.length - 1;
        this.$refs.articlelist.selectArticleByIndex(last_index);
       }
     },     
     giveCurFeedIndex() {
       return this.$store.state.curFeedIndex;
     },
     giveCurArticleIndex() {
       return this.curArticleIndex;
     },
     giveViewKey() {
       return this.viewKey;
     },
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
