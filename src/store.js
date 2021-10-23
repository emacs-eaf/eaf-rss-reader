import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    feedsList: [],
    feedsLinkList: [],
    curFeedIndex: -1,
    curArticleIndex:-1
  },
  mutations: {
    updateFeedsList(state, infos) {
      state.feedsList = infos;
    },
    updateFeedsLinkList(state, infos) {
      state.feedsLinkList = infos;
    },
    changeCurFeedIndex(state, feed_index) {
      state.curFeedIndex = feed_index;
    },
    changeCurArticleIndex(state, article_index) {
      state.curArticleIndex = article_index;
    },
    markArticleAsRead(state) {
      state.feedsList[state.curFeedIndex].feed_article_list[state.curArticleIndex].isRead = true;
    },
    markFeedAsRead(state) {
      state.feedsList[state.curFeedIndex].feed_article_list.map(article => article.isRead = true);
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
        return state.feedsList[index].feed_article_list;
      }
    },
  }
})
