<template>
  <div class="list-area" :style="{'border-color':lineColor, 'background':backgroundColor}">
    <div class="feeds-list" ref="feedlist">
      <div
        v-if="$store.state.feedsList.length === 0"
        class="first-guide">
        Press A to add feed url.
      </div>
      <div
        v-else
        class="feed eaf-rss-reader-feed-item"
        v-for="feed in $store.state.feedsList"
        :key="feed.feed_index"
        :style="{
          'background':itemBackgroundColor(feed),
          'color':itemForegroundColor(feed),
          'border-color':lineColor}"
        @click="changeCurrentFeedByIndex(feed.feed_index), cleanArticle()">
        <div class="feed-title">
          <div class="title">
            <div>{{ feed.feed_title }}</div>
            <div class="unread-count">({{ unreadCount(feed.feed_index) }})</div>
            <div v-if="feed.feed_title === ''"> {{ feed.feed_subtitle }}</div>
            <div v-if="feed.feed_title === '' && feed.feed_subtitle === ''">
              {{ feed.feed_link }}
            </div>
          </div>
          <div class="sub-title">
            <div>{{ feed.feed_subtitle }}</div>
            <div v-if="feed.feed_subtitle === ''"> {{ feed.feed_link }}</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
 import { mapState } from 'vuex';

 export default ({
   name: 'FeedsList',
   data() {
     return {
       backgroundColor:"",
       foregroundColor: "",
       selectColor: "",
       readColor: "",
       lineColor:"",
     };
   },
   computed: {
     ...mapState([
       'currentFeedIndex',
       'currentArticleIndex',
     ])
   },
   mounted() {
     window.selectFeedByIndex = this.selectFeedByIndex;
     window.changeCurrentFeedByIndex = this.changeCurrentFeedByIndex;
     window.initFeedsListColor = this.initFeedsListColor;
   },
   created() {
   },
   methods: {
     initFeedsListColor(backgroundColor, foregroundColor, selectColor, readColor, lineColor) {
       this.backgroundColor = backgroundColor;
       this.foregroundColor = foregroundColor;
       this.selectColor = selectColor;
       this.readColor = readColor;
       this.lineColor = lineColor;
     },
     changeCurrentFeedByIndex(feed_index) {
       this.$store.commit('changeCurrentFeedIndex', feed_index);
     },
     itemBackgroundColor(feed) {
       if (feed.feed_index === this.currentFeedIndex) {
         return this.selectColor;
       } else {
         return this.backgroundColor;
       }
     },
     itemForegroundColor(feed) {
       if (feed.feed_article_list.filter(x => !x.isRead).length == 0) {
         return this.readColor;
       } else {
         return this.foregroundColor;
       }
     },
     keepSelectVisible() {
       this.$refs.feedlist.children[this.currentFeedIndex].scrollIntoViewIfNeeded(false);
     },
     selectFeedByIndex(index) {
       var len = this.$store.state.feedsList.length;
       if (index >= len) {
         this.changeCurrentFeedByIndex(len - 1)
       } else if (index <= 0) {
         this.changeCurrentFeedByIndex(0)
       } else {
         this.changeCurrentFeedByIndex(index)
       }
       this.keepSelectVisible();
     },
     cleanArticle() {
       this.$store.commit('changeCurrentArticleIndex', -1);
     },
     unreadCount(index) {
       return this.$store.state.feedsList[index].feed_article_list.filter(x => !x.isRead).length;
     }
   }
 })
</script>

<style scoped>
 .first-guide {
   display: flex;
   justify-content: center;
   align-items: center;
   height: 100%;
 }

 .list-area {
   display: flex;
   width: 100%;
   height: 100%;
   flex-direction: column;
   overflow: hidden;
   background-color: #FFF;
   border-right: 1px solid #BBBFCA;
   color: #495464;
 }

 .title {
   display: flex;
   font-size: 16px;
   font-weight: bold;
   padding-top: 2px;
   padding-bottom: 2px;
 }

 .sub-title {
   display: flex;
   font-size: 14px;
   padding-top: 2px;
   padding-bottom: 2px;
 }

 .feed-title {
   display: flex;
   flex-direction: column;
   text-align: left;
   padding-left: 4px;
   white-space:nowrap;
   overflow:hidden;
   text-overflow: ellipsis;
 }

 .feeds-list {
   height: 100%;
   width: 100%;
   overflow: scroll;
   display: flex;
   flex-direction: column;
 }

 .feed {
   display: flex;
   flex-shrink:0;
   flex-direction: row;
   border-bottom: 1px solid #BBBFCA;
   padding-bottom: 5px;
   padding-top: 5px;
   padding-left: 10px;
   padding-right: 10px;
   justify-content: space-between;
 }

 .unread-count {
   margin-left: 10px;
 }
</style>
