import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    feedsList: [],
    curFeed: null,
    curFeedIndex: -1,
    viewKey: "all"
  },
  mutations: {
    updateFileInfos(state, infos) {
      state.feedsList = infos;
    },
    changeReadStatus(state, param) {
      const cur_feed = state.feedsList[state.curFeedIndex];
      const index = cur_feed.feed_article_list.findIndex(x => x.title === param.title);
      console.log(index);
      if (index != -1) {
        cur_feed.feed_article_list[index].isRead = param.status;
        console.log(cur_feed.feed_article_list[index].isRead);
      }
    },
    
    changeCurFeed(state, feed_title) {
      state.curFeed = feed_title;
      console.log(state.curFeed);
    },
    changeCurFeedIndex(state) {
      const index = state.feedsList.findIndex(x => x.feed_title === state.curFeed);
      if (index != -1) {
        state.curFeedIndex = index;
      }
      console.log(state.curFeedIndex);
    },
    changeViewKey(state, key) {
      state.viewKey = key;
    }
  },
  actions: {
		getList(context) {
			axios.get('/list.json').then(({data}) => {
				context.commit('updateFileInfos', data);
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
