import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    feedsList: [],
    feedsLinkList: [],
    curFeed: null,
    curFeedIndex: -1,
    viewKey: "all"
  },
  mutations: {
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
    
    changeCurFeed(state, feed_title) {
      state.curFeed = feed_title;
    },
    changeCurFeedIndex(state) {
      const index = state.feedsList.findIndex(x => x.feed_title === state.curFeed);
      if (index != -1) {
        state.curFeedIndex = index;
      }
    },
    changeViewKey(state, key) {
      state.viewKey = key;
    }
  },
  actions: {
    // test in localhost
		getList(context) {
			axios.get('/list.json').then(({data}) => {
				context.commit('updateFeedsList', data);
			})
		}
	},
  getters: {
    curFeedArticleList(state) {
      const index = state.feedsList.findIndex(x => x.feed_title === state.curFeed);
      if (index != -1) {
        return state.feedsList[index].feed_article_list;
        
      }
    },
    infolist(state) {
      const index = state.feedsList.findIndex(x => x.feed_title === state.curFeed);
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
			
		}
  }
})
