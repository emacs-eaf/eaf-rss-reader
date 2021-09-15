<template>
	<div class="home" id="home">
		<button @click="selectPrevItem()">prev</button>
		<button @click="selectNextItem()">next</button>
		<button @click="openCurrentItem()">right</button>
		<button @click="upItem()">left</button>
		
		<feedsList class="feedsList" ref="feedslist"> </feedsList>
		<articlesList v-if="$store.state.curFeedIndex!=-1"  class="articlesList" ref="articlelist"></articlesList>
	</div>
</template>

<script>
import articlesList from "@/components/articlesList.vue"
import feedsList from "@/components/feedsList.vue"
import {mapState} from 'vuex';

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
		'openArticle'])
	},
	components:{
		articlesList,
		feedsList,
	},
	mounted() {
		window.selectNextItem = this.selectNextItem;
		window.selectPrevItem = this.selectPrevItem;
		window.openCurrentItem = this.openCurrentItem;
		window.upItem = this.upItem;
	},
	methods: {
		changeViewKey(key) {
			this.$store.commit('changeViewKey', key)
		},
		selectNextItem() {
			if (!this.openFeed && !this.openArticle) {
				this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex + 1);
			} else if (this.openFeed && !this.openArticle) {
				this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex + 1);
			} 
		},
		selectPrevItem() {
			if (!this.openFeed && !this.openArticle) {
				this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex - 1);
			} else if (this.openFeed && !this.openArticle) {
				this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex - 1);
			}
		},
		openCurrentItem() {
			if (!this.openFeed && !this.openArticle) {
				if (this.curFeedIndex != -1 && this.curArticleIndex === -1) {
					
					this.$store.commit('changeOpenFeed', true);
				}
			} else if (this.openFeed && !this.openArticle) {
				if (this.curFeedIndex != -1 && this.curArticleIndex != -1) {
					this.$store.commit('changeOpenArticle', true);
				}
			}
		},
		upItem() {
			if (this.openFeed && this.openArticle) {
				if (this.curFeedIndex != -1 && this.curArticleIndex != -1) {
					this.$store.commit('changeOpenArticle', false);
					this.$store.commit('changeCurArticleIndex', -1);
				}
			} else if (this.openFeed && !this.openArticle) {
				if (this.curFeedIndex != -1) {
					this.$store.commit('changeOpenFeed', false);
					this.$store.commit('changeCurArticleIndex', -1);
				}
			} else if (!this.openFeed && !this.openArticle) {
				if (this.curFeedIndex != -1) {
					this.$store.commit('changeCurFeedIndex', -1);
					this.$store.commit('changeCurArticleIndex', -1);
				}
			}
		}
	}
};
</script>

<style scoped>

.view-bar {
	position: fixed;
}
#home{
	max-width: 1400px;
	margin:0 auto;

	display: flex;
  flex-direction: column;
  
  width: 100%;
  height: 100%;

  position: relative;
}
</style>
