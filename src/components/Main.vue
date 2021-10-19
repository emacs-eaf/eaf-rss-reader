<template>
  <div class="page">
    <div class="content">
      <div class="item-area">
        <FeedsList
          class="feeds-list"
          ref="feedslist" />

        <ArticlesList
          class="articles-list"
          :style="{'flex': '0 0 61.8%'}"
          ref="articlelist" />
      </div>
    </div>
  </div>
</template>

<script>
 import { QWebChannel } from "qwebchannel";
 import ArticlesList from "@/components/ArticlesList.vue"
 import FeedsList from "@/components/FeedsList.vue"
 import {mapState, mapGetters} from 'vuex';

 export default {
   name: "home",
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
   flex-direction: column;
 }

 .content {
   width: 100%;
   height: 100%;
   overflow: hidden;
   display: flex;
   flex-direction: column;
 }

 .item-area {
   height: 100%;
   display: flex;
   flex-direction: row;
   overflow: hidden;
   background: #FFF;
 }

 .view-bar {
   position: fixed;
 }

 .test-item {
   flex-direction: column;
 }

 .button-list {
   flex-direction: row;
 }

 .feeds-list {
   flex: 0 0 38.2%;
 }
</style>
