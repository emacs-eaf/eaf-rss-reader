<template>
	<div class="articleList">
		<div class="content">
		<div class="list-area">
			<div class="article-list-title">
				<mu-appbar 
				color="white" 
				textColor="black"
				:style="{'background':highlightTitle()}">
					{{$store.state.feedsList[curFeedIndex].feed_title}}
				</mu-appbar>
			</div>

			<div  class="article-list" ref="articlelist">
				<div
				class="article-card"
				v-for="article in infolist"
				:style="{'background':itemBackgroundColor(article)}"
				:key="article.article_index">

				<mu-container>
					<mu-card>
						<mu-card-title 
						:title="article.title" 
						class="title" 
						@click="changeCurArticleByIndex(article.index), 
										changeOpenArticle(true),
										changeOpenFeed(true)"/>
						<mu-card-header 
						:title="article.author" 
						:sub-title="article.time"
						style="text-align:left;">
						</mu-card-header>
						<mu-card-text style="text-align:left;">
							{{article.shortDescription}}
						</mu-card-text>
					
						<mu-button 
						@click="changeCurArticleByIndex(article.index), 
										changeOpenArticle(true),
										changeOpenFeed(true)" flat>
							Read
						</mu-button>
						
					</mu-card>
				</mu-container>
				</div>
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
			backgroundColor: "white",
			selectColor: "grey",
			num: 0,
		};
	},
	computed: {
		...mapGetters(['curFeedArticleList', 'infolist']),
		...mapState([
		'curFeedIndex', 
		'curArticleIndex', 
		'openFeed',
		])
	},
	mounted() {
		window.initCardItemListColor = this.initCardItemListColor;
		window.getpic = this.getpic
		window.getitem = this.get_item
		window.changeOpenFeed = this.changeOpenFeed;
		window.changeOpenArticle = this.changeOpenArticle;
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
		initCardItemListColor(backgroundColor, foregroundColor) {
			this.backgroundColor = backgroundColor;
			this.foregroundColor = foregroundColor;
    },
		addFiles(files) {
			this.$store.commit('updateFileInfos', files);
		},
		highlightTitle() {
			if (this.openFeed && this.curArticleIndex === -1) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
		},
		itemBackgroundColor(article) {
			if (article.index == this.curArticleIndex) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
    },
		keepSelectVisible() {
			this.$refs.articlelist.children[this.curArticleIndex].scrollIntoViewIfNeeded(false);
    },
		selectArticleByIndex(index) {
			var len = this.$store.state.feedsList[this.curFeedIndex].feed_article_list.length;
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
	}
}
</script>


<style scoped>
.articleList {
	width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.content {
	margin-top: 110px;
	margin-left: 700px;
	width: 100%;
	height: 100%;
	overflow: hidden;

	display: flex;
	flex-direction: column;
 }

.list-area {
	height: 100%;
	display: flex;
	flex-direction: column;
 }

.article-list-title {
	width: 100%;
	display: flex;
	flex-direction: column;
}

.article-list {
	width: 100%;
	height: 75%;
	overflow: scroll;
}

.article-card {
	margin-top: 20px;
	width: 100%; 
	max-width: 575px; 
	flex-direction: column;
}

.single-card {
	width: 100%;
	position: relative;
	display: flex;
  flex-direction: row;
  align-items: center;
}

.title{
	text-align:left;
	margin-top: -0px;
	margin-bottom: -10px;
}

</style>
