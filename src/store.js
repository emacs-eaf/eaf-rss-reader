import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    feedsList: [],
    feedsLinkList: [],
    currentFeedIndex: -1,
    currentArticleIndex:-1
  },
  mutations: {
    updateFeedsList(state, infos) {
      state.feedsList = infos;
    },
    updateFeedsLinkList(state, infos) {
      state.feedsLinkList = infos;
    },
    changeCurFeedIndex(state, feed_index) {
      state.currentFeedIndex = feed_index;
    },
    changeCurArticleIndex(state, article_index) {
      state.currentArticleIndex = article_index;
    },
    markArticleAsRead(state) {
      state.feedsList[state.currentFeedIndex].feed_article_list[state.currentArticleIndex].isRead = true;
    },
    markFeedAsRead(state) {
      state.feedsList[state.currentFeedIndex].feed_article_list.map(article => article.isRead = true);
    }
  },
  actions: {
  },
  getters: {
    currentFeedArticleList(state) {
      if (state.currentFeedIndex != -1) {
        return state.feedsList[state.currentFeedIndex].feed_article_list;
      }
    },
    infolist(state) {
      const index = state.currentFeedIndex;
      if (index != -1) {
        return state.feedsList[index].feed_article_list;
      }
    },
  }
})
