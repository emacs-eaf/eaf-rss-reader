import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    feedsList: [],
    feedsLinkList: [],
    openFeed: false,
    openArticle: false,
    curFeedIndex: -1,
    curArticleIndex:-1,
    viewKey: "all"
  },
  mutations: {
    changeOpenFeed(state, status) {
      state.openFeed = status;
    },
    changeOpenArticle(state, status) {
      state.openArticle = status;
    },
    updateFeedsList(state, infos) {
      state.feedsList = infos;
    },
    updateFeedsLinkList(state, infos) {
      state.feedsLinkList = infos;
    },
    changeReadStatus(state, param) {
      const cur_feed = state.feedsList[state.curFeedIndex];
      const index = cur_feed.feed_article_list.findIndex(x => x.title === param.title);
      if (index != -1) {
        cur_feed.feed_article_list[index].isRead = param.status;
      }
    },
    changeCurFeedIndex(state, feed_index) {
      state.curFeedIndex = feed_index;
    },
    changeCurArticleIndex(state, article_index) {
      state.curArticleIndex = article_index;
    },
    changeViewKey(state, key) {
      state.viewKey = key;
    },
    markAsRead(state) {
      state.feedsList[state.curFeedIndex].feed_article_list[state.curArticleIndex].isRead = true;
    }
  },
  actions: {
	},
  getters: {
    curFeedArticleList(state) {
      if (state.curFeedIndex != -1) {
        return state.feedsList[state.curFeedIndex].feed_article_list;
      }
    },
    infolist(state) {
      const index = state.curFeedIndex;
      if (index != -1) {
        if (state.viewKey === 'all') {
          return state.feedsList[index].feed_article_list;
        }
        if (state.viewKey === 'read') {
          return state.feedsList[index].feed_article_list.filter(x => x.isRead);
        }
        if (state.viewKey === 'unread') {
          return state.feedsList[index].feed_article_list.filter(x => !x.isRead);
        }
        return state.feedsList[index].feed_article_list;
      }
		},

  }
})
