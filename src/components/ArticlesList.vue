<template>
		<div class="list-area">
			<div class="articles-list-title-bar"
			:style="{'background':highlightTitleBack(), 'color':highlightTitleFont()}">
				<h1 class="feed-title">
					{{$store.state.feedsList[curFeedIndex].feed_title}}
				</h1>
				<div class="button-wrapper">
					<button 
					class="button"
					@click="changeViewKey('all')"
					:style="{'background': $store.state.viewKey === 'all' ? selectButtonColor : buttonColor}">
						All
					</button>
					<button 
					class="button"
					@click="changeViewKey('read')"
					:style="{'background': $store.state.viewKey === 'read' ? selectButtonColor : buttonColor}">
						Read
					</button>
					<button 
					class="button"
					@click="changeViewKey('unread')"
					:style="{'background': $store.state.viewKey === 'unread' ? selectButtonColor : buttonColor}">
						Unread
					</button>
				</div>
			</div>

			<div  class="articles-list" ref="articlelist">
				<div
				class="article-item"
				v-for="article in infolist"
				@click="changeCurArticleByIndex(article.index)"
				:style="{'background':itemBackgroundColor(article), 'color':itemFontColor(article)}"
				:key="article.article_index">
					<div class="article-title" 
					@click="changeCurArticleByIndex(article.index), 
									changePreviewArticle(true),
									changeOpenArticle(true),
									changeOpenFeed(true)">
						{{article.title}}
					</div>
					<div class="article-author">
						{{article.author}}
					</div>
					<div class="article-time">
						{{article.time}}
					</div>
					<div class="article-short-description">
						{{article.shortDescription}}
					</div>
				</div>
			</div>
		</div>
</template>

<script>
import {mapGetters, mapState} from 'vuex';
import { QWebChannel } from "qwebchannel";

export default {
	name: 'listCard',
	data () {
		return {
			num: 0,
			selectColor: "#515e72",
			backgroundColor:"#F4F4F2",
			selectFontColor:"#CFCFCF",
			fontColor:"#495464",
			fontReadColor: "#919fb6",
			selectButtonColor:"#5579dd",
			buttonColor: "#9E9E9E",
		};
	},
	computed: {
		...mapGetters(['curFeedArticleList', 'infolist']),
		...mapState([
		'curFeedIndex', 
		'curArticleIndex', 
		'openFeed',
		'previewArticle'
		])
	},
	mounted() {
		window.initCardItemListColor = this.initCardItemListColor;
		window.getpic = this.getpic
		window.getitem = this.get_item
		window.changeOpenFeed = this.changeOpenFeed;
		window.changeOpenArticle = this.changeOpenArticle;
		window.changeViewKey = this.changeViewKey;
		window.changeCurArticleByIndex = this.changeCurArticleByIndex;
		window.selectArticleByIndex = this.selectArticleByIndex;
  },
	created() {
		// eslint-disable-next-line no-undef
		new QWebChannel(qt.webChannelTransport, channel => {
			window.pyobject = channel.objects.pyobject;
		});
  },
	methods: {
		changeViewKey(key) {
			this.$store.commit('changeViewKey', key)
		},
		initCardItemListColor(backgroundColor, foregroundColor) {
			this.backgroundColor = backgroundColor;
			this.foregroundColor = foregroundColor;
    },
		addFiles(files) {
			this.$store.commit('updateFileInfos', files);
		},
		highlightTitleBack() {
			if (this.openFeed && this.curArticleIndex === -1) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
		},
		highlightTitleFont() {
			if (this.openFeed && this.curArticleIndex === -1) {
				return this.selectFontColor;
			} else {
				return this.fontColor;
			}
		},
		itemBackgroundColor(article) {
			if (article.index === this.curArticleIndex) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
    },
		itemFontColor(article) {
			if (article.index === this.curArticleIndex) {
				return this.selectFontColor;
			} else if (article.isRead === true) {
				return this.fontReadColor;
			} else {
				return this.fontColor;
			}
		},
		keepSelectVisible() {
			this.$refs.articlelist.children[this.curArticleIndex].scrollIntoViewIfNeeded(false);
    },
		selectArticleByIndex(index) {
			var len = this.infolist.length;
			if (index >= len) {
				this.changeCurArticleByIndex(len - 1)
			} else if (index <= 0) {
				this.changeCurArticleByIndex(0)
			} else {
				this.changeCurArticleByIndex(index)
			}
			this.keepSelectVisible();
		},
		changeCurArticleByIndex(article_index) {
			this.$store.commit('changeCurArticleIndex', article_index);
		},
		changeOpenFeed(status) {
			if (status === 'false') status = false;
			else if (status === 'true') status = true;
			this.$store.commit('changeOpenFeed', status);
		},
		changeOpenArticle(status) {
			if (status === 'false') status = false;
			else if (status === 'true') status = true;
			this.$store.commit('changeOpenArticle', status);
		},
		changePreviewArticle(status) {
			if (status === 'false') status = false;
			else if (status === 'true') status = true;
			this.$store.commit('changePreviewArticle', status);
		},
	}
}
</script>

<style scoped>
.list-area {
	height: 100%;
	display: flex;
	flex-direction: column;

	overflow: hidden;
	color: #495464;
 }

.articles-list-title-bar {
	width: 100%;

	position: sticky;
	display: flex;
	flex-direction: row;
	background-color: #F4F4F2;

	border-style: solid;
	border-width: 1px;
	border-color: #BBBFCA;

	margin-top: -2px;
	margin-bottom: -2px;

	justify-content: space-between;
	overflow: hidden;
}

.feed-title {
	text-align: left;
	font-weight: bold;
	overflow: hidden;
	padding-left: 4px;
}

.button-wrapper {
	margin:auto 0;
	display: flex;
	flex-direction: row;
}

.button {
	width: 70px;
	height: 40px;
	font-size: 14px;
	margin-left: 5px;
	margin-right: 5px;
	font-weight: bold;
	background-color: #9E9E9E;
  color: #F4F4F2; 
	border: 1px solid #BBBFCA;
	border-radius: 4px;
}

.articles-list {
	height: 100%;
	width: 100%;
	overflow: scroll;
	display: flex;
	flex-direction: column;
}

.article-item {
	display: flex;
	flex-shrink:0;
	flex-direction: column;
	
	border-style: solid;
	border-width: 1px;
	border-color: #BBBFCA;

	padding-bottom: 5px;
	padding-top: 5px;
	padding-left: 8px;

	word-break:break-all;
}

.article-title {
	display: flex;
	font-size: 21px;
	font-weight: bold;
	text-align: left;
	cursor: pointer;
	margin-bottom: 5px;
	margin-top: 5px;
}

.article-author {
	display: flex;
	font-size: 19px;
	text-align: left;
	margin-bottom: 5px;
	margin-top: 5px;
}

.article-time {
	display: flex;
	font-size: 16px;
	text-align: left;
	color: #9E9E9E;
	flex-shrink:0;
	padding-bottom: 5px;
	padding-top: 5px;
}

.article-short-description {
	display: flex;
	font-size: 17px;
	text-align: left;
	margin-bottom: 5px;
	margin-top: 5px;
}
</style>
