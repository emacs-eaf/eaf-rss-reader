<template>
  <div class="list-area">
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
        :style="{'background':itemBackgroundColor(feed), 'color':itemFontColor(feed)}"
        @click="changeCurFeedByIndex(feed.feed_index), cleanArticle()">
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
       isAdd:false,
       newFeedLink: '',
       backgroundColor:"#FFF",
       selectColor: "#515e72",
       selectFontColor:"#cfcfcf",
       fontColor:"#495464",
       fontReadColor: "#919fb6",
       selectRefreshButtonColor:"#5579dd",
       selectRemoveButtonColor:"#d6382d",
       buttonColor: "#9E9E9E",
     };
   },
   computed: {
     ...mapState([
       'curFeedIndex',
       'curArticleIndex',
     ])
   },
   mounted() {
     window.selectFeedByIndex = this.selectFeedByIndex;
     window.changeCurFeedByIndex = this.changeCurFeedByIndex;
   },
   created() {
   },
   methods: {
     changeCurFeedByIndex(feed_index) {
       this.$store.commit('changeCurFeedIndex', feed_index);
     },
     itemBackgroundColor(feed) {
       if (feed.feed_index == this.curFeedIndex) {
         return this.selectColor;
       } else {
         return this.backgroundColor;
       }
     },
     itemFontColor(feed) {
       if (feed.feed_index == this.curFeedIndex) {
         return this.selectFontColor;
       } else if (feed.feed_article_list.filter(x => !x.isRead).length == 0) {
         return this.fontReadColor;
       } else {
         return this.fontColor;
       }
     },
     keepSelectVisible() {
       this.$refs.feedlist.children[this.curFeedIndex].scrollIntoViewIfNeeded(false);
     },
     selectFeedByIndex(index) {
       var len = this.$store.state.feedsList.length;
       if (index >= len) {
         this.changeCurFeedByIndex(len - 1)
       } else if (index <= 0) {
         this.changeCurFeedByIndex(0)
       } else {
         this.changeCurFeedByIndex(index)
       }
       this.keepSelectVisible();
     },
     cleanArticle() {
       this.$store.commit('changeCurArticleIndex', -1);
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
