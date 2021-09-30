<template>
	<div class="page">
		<div class="content">
			<div class="item-area">
				<FeedsList 
				v-if="!previewArticle"
				class="feeds-list"
				ref="feedslist" />

				<ArticlesList 
				v-if="curFeedIndex != -1 "
				class="articles-list"
				:style="{'flex': previewArticle === true ? '0 0 38.2%' :'0 0 61.8%'}"
				ref="articlelist" />
				
				<ArticlePanel
				v-if="previewArticle && curArticleIndex != -1"
				:article="$store.state.feedsList[curFeedIndex].feed_article_list[curArticleIndex]"
				class="articlePanel" 
				ref="articlePanel"/>
			</div>
	</div>		
	</div>
</template>

<script>
import ArticlesList from "@/components/ArticlesList.vue"
import ArticlePanel from "@/components/ArticlePanel.vue"
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
		ArticlePanel,
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
			} else if (this.openFeed && this.previewArticle && this.openArticle) {
				this.$refs.articlePanel.scrollUp();
			}
		},
		selectPrevItem() {
			if (!this.openFeed && !this.previewArticle && !this.openArticle) {
				this.$refs.feedslist.selectFeedByIndex(this.curFeedIndex - 1);
			} else if (this.openFeed && !this.openArticle) {
				this.$refs.articlelist.selectArticleByIndex(this.curArticleIndex - 1);
			} else if (this.openFeed && this.previewArticle && this.openArticle) {
				this.$refs.articlePanel.scrollDown();
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
		}
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

.articlePanel {
	flex: 0 0 61.8%;
}
</style>
