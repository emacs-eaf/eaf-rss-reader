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
       'previewArticle',
       'viewKey']),
     ...mapGetters(['curFeedArticleList']),
   },
   components:{
     ArticlesList,
     FeedsList,
   },
   mounted() {
     window.selectNextItem = this.selectNextItem;
     window.selectPrevItem = this.selectPrevItem;
     window.openCurrentItem = this.openCurrentItem;
     window.upItem = this.upItem;
     window.giveCurFeedIndex = this.giveCurFeedIndex;
     window.giveCurArticleIndex = this.giveCurArticleIndex;
     window.giveOpenFeed = this.giveOpenFeed;
     window.giveOpenArticle = this.giveOpenFeed;
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
     selectNextItem() {
       if (!this.openFeed && !this.previewArticle && !this.openArticle) {
         this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex + 1);
       } else if (this.openFeed && !this.openArticle) {
         this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex + 1);
       }
     },
     selectPrevItem() {
       if (!this.openFeed && !this.previewArticle && !this.openArticle) {
         this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex - 1);
       } else if (this.openFeed && !this.openArticle) {
         this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex - 1);
       }
     },
     openCurrentItem() {
       if (!this.openFeed && !this.previewArticle && !this.openArticle) {
         if (this.curFeedIndex != -1 && this.curArticleIndex === -1) {
           this.$store.commit('changeOpenFeed', true);
         }
       } else if (this.openFeed && !this.previewArticle && !this.openArticle) {
         if (this.curFeedIndex != -1 && this.curArticleIndex != -1) {
           this.$store.commit('changePreviewArticle', true);
         }
       } else if (this.openFeed && this.previewArticle && !this.openArticle) {
         if (this.curFeedIndex != -1 && this.curArticleIndex != -1) {
           this.$store.commit('changeOpenArticle', true);
         }
       }
     },
     upItem() {
       if (this.openArticle && this.previewArticle && this.openFeed) {
         if (this.curFeedIndex != -1 && this.curArticleIndex != -1) {
           this.$store.commit('changeOpenArticle', false);
         }
       } else if (!this.openArticle && this.previewArticle && this.openFeed) {
         if (this.curArticleIndex != -1) {
           this.$store.commit('changePreviewArticle', false);
         }
       } else if (!this.openArticle && !this.previewArticle && this.openFeed) {
         if (this.curFeedIndex != -1) {
           this.$store.commit('changeOpenFeed', false);
           this.$store.commit('changeCurArticleIndex', -1);
         }
       } else if (!this.openArticle && !this.PreviewArticle && !this.openFeed) {
         if (this.curFeedIndex != -1) {
           this.$store.commit('changeCurFeedIndex', -1);
           this.$store.commit('changeCurArticleIndex', -1);
         }
       }
     },
     giveCurFeedIndex() {
       return this.$store.state.curFeedIndex;
     },
     giveCurArticleIndex() {
       return this.curArticleIndex;
     },
     giveOpenFeed() {
       if (this.openFeed === false) return 'false';
       return 'true';
     },
     giveOpenArticle() {
       if (this.openArticle === 'false') return 'false';
       return 'true';
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
