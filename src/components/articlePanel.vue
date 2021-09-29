<template>
	<div class="article-page">
		<div class="article-title-bar"
		:style="{'background':highlightTitleBack(), 'color':highlightTitleFont()}">
			<h1 class="article-title">
				{{article.title}}
			</h1>
			<div class="button-wrapper">
				<button class="go-back" @click="goback()">
					Goback
				</button>
				<button class="original-page-button" @click="viewOriginalPage()">
					Original
				</button>
				<button 
				class="read-button" 
				@click="changeReadStatus(article.title, true, 0)"
				:style="{'background': article.isRead === true ? selectButtonColor : buttonColor}">
					Read
				</button>
				<button 
				class="unread-button" 
				@click="changeReadStatus(article.title, false, 0)"
				:style="{'background': article.isRead === false ? selectButtonColor : buttonColor}">
					Unread
				</button>
			</div>
		</div>
		<div class="article-wrapper" ref="articlepanel">
			<div class="article">
			<p class="article-author">
				Author : {{article.author}}
			</p>
			<p class="article-time">
				Time : {{article.time}}
			</p>
			<p class="article-description">
				{{article.description}}
			</p>
			</div>
		</div>
	</div>
</template>

<script>
import { QWebChannel } from "qwebchannel";
import { mapState } from 'vuex';

export default {
  name: 'ArticlePanel',
  components: {
  },
  data() {
    return {
			title: this.article.title,
			selectColor: "#515e72",
			selectButtonColor:"#5579dd",
			buttonColor: "#9E9E9E",
			backgroundColor:"#F4F4F2",
			selectFontColor:"#CFCFCF",
			fontColor:"#495464",
    }
  },
  props:{
    article:null,
	},
	computed: {
		...mapState([
		'curFeedIndex', 
		'curArticleIndex', 
		'openFeed', 
		'openArticle',
		'previewArticle',
		])
	},
	created() {
		// eslint-disable-next-line no-undef
		new QWebChannel(qt.webChannelTransport, channel => {
			window.pyobject = channel.objects.pyobject;
		});
  },
	mounted() {
		window.scrollUp = this.scrollUp;
    window.scrollDown = this.scrollDown;
		window.goback = this.goback;
		window.getCurArticleStatus = this.getCurArticleStatus;
		window.getCurArticleTitle = this.getCurArticleTitle;
		window.changeReadStatus = this.changeReadStatus;
		window.viewOriginalPage = this.viewOriginalPage;
	},
	methods: {
		// from === 0 : vue.js call pyhon
		// from === 1 : python call vue.js
		changeReadStatus(title, status, from) {
			if (from === '1') {
				if (status === 'False') status = false;
				else if (status === 'True') status = true;
			}
			var param = {
				title : title,
				status : status
			}
			this.$store.commit('changeReadStatus', param);
			if (from === 0) {
				window.pyobject.change_read_status(this.$store.state.curFeedIndex, this.article.index, param.status);
			}				
		},
		highlightTitleBack() {
			if (this.openArticle) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
		},
		highlightTitleFont() {
			if (this.openArticle ) {
				return this.selectFontColor;
			} else {
				return this.fontColor;
			}
		},
    scrollUp() {
			this.$refs.articlepanel.scrollTop += 30;
    },
		scrollDown() {
			this.$refs.articlepanel.scrollTop -= 30;
		},
		getCurArticleTitle() {
			return this.article.title;
		},
		getCurArticleStatus() {
			return this.article.isRead;
		},
		goback() {
			this.$store.commit('changeOpenArticle', false);
			this.$store.commit('changePreviewArticle', false);
		},
		viewOriginalPage() {
			window.pyobject.view_original_page(this.article.link)
		}
	}
}
</script>

<style scoped>
.article-page {
	height:100%;
	flex-direction: column;
	display: flex;
	overflow: hidden;
	background: #F4F4F2;
	color: #495464;
}

.article-title-bar {
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

.button-wrapper {
	display: flex;
	flex-direction: row;
	margin:auto 0;
}

button {
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

.article-title {
	text-align: left;
	font-weight: bold;
	overflow: hidden;
	padding-left: 4px;
}

.article-wrapper {
	height: 100%;
	width: 100%;
	overflow: scroll;
	display: flex;
	flex-direction: column;
	font-size: 18px;
	text-align: left;
	padding-left: 8px;
	padding-right: 8px;
}

.article-description {
	position: relative;
	white-space: pre-line;
}

.go-back {
	background: #5579dd;
}

.original-page-button {
	background: #5579dd;
}
</style>
