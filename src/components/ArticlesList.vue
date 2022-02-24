<template>
  <div class="list-area">
    <div
    class="articles-list"
    ref="articlelist"
    :style="{'border-color':lineColor, 'background':backgroundColor}">
      <div
        class="article-item eaf-rss-reader-article-item"
        v-for="article in infolist"
        @click="changeCurrentArticleByIndex(article.index), markArticleAsRead()"
        :style="{
          'background':itemBackgroundColor(article),
          'color':itemForegroundColor(article),
          'border-color':lineColor
          }"
        :key="article.article_index">
        <div class="article-title">
          {{ article.title }}
        </div>

        <div class="article-line">
          <div
            v-if="article.author !== ''"
            class="article-author">
            {{ article.author }}
          </div>
          <div class="article-time">
            {{ formatDate(article) }}
          </div>
        </div>

        <div
          class="article-short-description"
          v-html="article.shortDescription">
        </div>
      </div>
    </div>
  </div>
</template>

<script>
 import { mapGetters, mapState } from 'vuex';

 export default {
   name: 'ArticlesList',
   data () {
     return {
       num: 0,
       backgroundColor:"",
       foregroundColor:"",
       selectColor: "",
       readColor:"",
       lineColor:"",
     };
   },
   props: {
     pyobject: Object,
   },
   computed: {
     ...mapGetters(['currentFeedArticleList', 'infolist']),
     ...mapState([
       'currentFeedIndex',
       'currentArticleIndex',
     ])
   },
   mounted() {
     window.changeCurrentArticleByIndex = this.changeCurrentArticleByIndex;
     window.selectArticleByIndex = this.selectArticleByIndex;
     window.markArticleAsRead = this.markArticleAsRead;
     window.markFeedAsRead = this.markFeedAsRead;
     window.initArticlesListColor = this.initArticlesListColor;
   },
   created() {
   },
   methods: {
     initArticlesListColor(backgroundColor, foregroundColor, selectColor, readColor, lineColor) {
       this.backgroundColor = backgroundColor;
       this.foregroundColor = foregroundColor;
       this.selectColor = selectColor;
       this.readColor = readColor;
       this.lineColor = lineColor;
     },
     itemBackgroundColor(article) {
       if (article.index === this.currentArticleIndex) {
         return this.selectColor;
       } else {
         return this.backgroundColor;
       }
     },
     itemForegroundColor(article) {
       if (article.isRead === true) {
         return this.readColor;
       } else {
         return this.foregroundColor;
       }
     },
     keepSelectVisible() {
       this.$refs.articlelist.children[this.currentArticleIndex].scrollIntoViewIfNeeded(false);
     },
     selectArticleByIndex(index) {
       var len = this.infolist.length;
       if (index >= len) {
         this.changeCurrentArticleByIndex(len - 1)
       } else if (index <= 0) {
         this.changeCurrentArticleByIndex(0)
       } else {
         this.changeCurrentArticleByIndex(index)
       }
       this.keepSelectVisible();
     },
     changeCurrentArticleByIndex(article_index) {
       this.$store.commit('changeCurrentArticleIndex', article_index);
     },
     markArticleAsRead() {
       this.$store.commit('markArticleAsRead');
       this.pyobject.mark_article_as_read(this.currentFeedIndex,
                                          this.currentArticleIndex,
                                          this.$store.state.feedsList[this.currentFeedIndex].feed_article_list[this.currentArticleIndex].link);
     },
     markFeedAsRead() {
       this.$store.commit('markFeedAsRead');
       this.pyobject.mark_feed_as_read();
     },
     formatDate(article) {
       var date = new Date(article.time);
       var fmt = "yyyy-MM-dd hh:mm:ss";

       if (!date || date == null) return null;
       var o = {
         'M+': date.getMonth() + 1,
         'd+': date.getDate(),
         'h+': date.getHours(),
         'm+': date.getMinutes(),
         's+': date.getSeconds(),
         'q+': Math.floor((date.getMonth() + 3) / 3),
         'S': date.getMilliseconds()
       }
       if (/(y+)/.test(fmt)) fmt = fmt.replace(RegExp.$1, (date.getFullYear() + '').substr(4 - RegExp.$1.length))
       for (var k in o) {
         if (new RegExp('(' + k + ')').test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length === 1) ? (o[k]) : (('00' + o[k]).substr(('' + o[k]).length)))
       }
       return fmt
     }
   }
 }
</script>

<style scoped>
 .list-area {
   height: 100%;
   display: flex;
   flex-direction: column;
   overflow: hidden;
 }

 .articles-list {
   height: 100%;
   width: 100%;
   overflow: scroll;
   display: flex;
   flex-direction: column;
   border-right: 1px solid #BBBFCA;
   background: #FFF;
 }

 .article-item {
   display: flex;
   flex-shrink:0;
   flex-direction: column;
   border-bottom: 1px solid #BBBFCA;
   padding-bottom: 5px;
   padding-top: 5px;
   padding-left: 10px;
   padding-right: 10px;
   word-break:break-all;
 }

 .article-title {
   display: flex;
   font-size: 16px;
   font-weight: bold;
   text-align: left;
   cursor: pointer;
   margin-bottom: 5px;
   margin-top: 5px;
   flex: 1 1 auto;
 }

 .article-author {
   display: flex;
   font-size: 14px;
   text-align: left;
   margin-right: 10px;
 }

 .article-time {
   display: flex;
   font-size: 14px;
   text-align: left;
   flex-shrink:0;
 }

 .article-short-description {
   font-size: 14px;
   text-align: left;
   margin-bottom: 5px;
   margin-top: 5px;
   display: inline;
 }

 .article-short-description ::v-deep * {
   font-size: 14px;
   font-weight: normal;
   padding: 0;
   margin: 0;
   width: 98%;
 }

 .article-short-description ::v-deep a {
   color: inherit;
 }

 .article-short-description ::v-deep ul {
   padding-left: 12px;
 }

 .article-short-description ::v-deep img {
   display: none;
 }

 .article-line {
   display: flex;
   flex-direction: row;
   align-items: center;
   margin-bottom: 5px;
 }
</style>
