<template>
  <div class="articlePanel" ref="articlePanel">
    <GoBack />
    <div class="article-page">
			<div class="title-bar">
				<mu-container class="button-wrapper">
					<mu-button
					:disabled="article.isRead === false ? false : true"
					@click="changeReadStatus(article.title, true, 0)"
					color="blue"
					textColor="white"
					>
						read
					</mu-button>
					<mu-button
					:disabled="article.isRead === true ? false : true"
					@click="changeReadStatus(article.title, false, 0)"
					color="blue"
					textColor="white"
					>
						unread
					</mu-button>
				</mu-container>
				<h1>
					{{article.title}}
				</h1>
			</div>
			<p class="author">
				{{article.author}}
			</p>
			<p class="time">
				{{article.time}}
			</p>
			<p class="article-description">
				{{article.description}}
			</p>
			<span @click='go(article.link)'>
				<mu-button>
						View original page
				</mu-button>
			</span>
		</div>
  </div>
</template>

<script>
import GoBack from "@/components/GoBack.vue";
import { QWebChannel } from "qwebchannel";

export default {
  name: 'ArticlePanel',
  components: {
    GoBack,
  },
  data() {
    return {
			title: this.article.title
    }
  },
  props:{
    article:null,
	},
	computed: {
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
		window.getCurArticleStatus = this.getCurArticleStatus;
		window.getCurArticleTitle = this.getCurArticleTitle;
		window.changeReadStatus = this.changeReadStatus;
	},
	methods: {
		// from === 0 : vue.js call pyhon
		// from === 1 : python call vue.js
		changeReadStatus(title, status, from) {
			if (from === '1')
			{
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
    scrollUp() {
			this.$refs.articlePanel.scrollTop += 30;
    },
		scrollDown() {
			this.$refs.articlePanel.scrollTop -= 30;
		},
		getCurArticleTitle() {
			return this.article.title;
		},
		getCurArticleStatus() {
			return this.article.isRead;
		},
	}
}
</script>

<style scoped>
.articlePanel{
	background-color: white;
}

.article-description {
	display: flex;
	justify-content: space-between;
	padding: 0 20px;
	position: relative;
	color: black;
}

p {
	margin: 0 40px;
	font-size: 20px;
	text-align: left;
}
</style>

<style >
.button-wrapper {
  text-align: center;
}
.mu-button{
  margin: 8px;
}

.title-bar{
	position:fixed;
	margin:10 auto;
	left:0;
	right:0;
}

</style>
