<template>
  <div class="page">
    <FeedsList class="feeds-list" ref="feedslist"/>
    <ArticlesList class="articles-list" ref="articlelist" />
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
   components:{
     ArticlesList,
     FeedsList,
   },
   mounted() {
     window.selectPrevFeed = this.selectPrevFeed;
     window.selectNextFeed = this.selectNextFeed;
     window.selectPrevArticle = this.selectPrevArticle;
     window.selectNextArticle = this.selectNextArticle;
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
       this.$store.commit('changeCurArticleIndex', -1);
     },
     selectPrevFeed() {
       this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex - 1);
       this.$store.commit('changeCurArticleIndex', -1);
     },
     selectNextArticle() {
       this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex + 1);
     },
     selectPrevArticle() {
       this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex - 1);
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
