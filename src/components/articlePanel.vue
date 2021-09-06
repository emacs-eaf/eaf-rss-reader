<template>
  <div class="articlePanel" ref="articlePanel">
    <GoBack />
    <div class="article-page">
      
			<mu-container class="button-wrapper">
				<mu-button
				:disabled="article.isRead === false ? false : true"
				@click="changeReadStatus(true)"
				color="blue"
				textColor="white"
				>
					read
				</mu-button>
				<mu-button
				:disabled="article.isRead === true ? false : true"
				@click="changeReadStatus(false)"
				color="blue"
				textColor="white"
				>
					unread
				</mu-button>
				<!--测试滚动按钮，将会被移除-->
				<mu-button
				@click="scrollUp()"
				color="blue"
				textColor="white"
				>
					Up
				</mu-button>
				<mu-button
				@click="scrollDown()"
				color="blue"
				textColor="white"
				>
					Down
				</mu-button>
			</mu-container>

			<h1>
				{{article.title}}
			</h1>
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
import {mapGetters} from 'vuex';

export default {
  name: 'ArticlePanel',

  components: {
    GoBack,
  },
  data() {
    return {
    }
  },
  props:{
    article:[],
		title: {
			type: String,
			required: true
		}
	},
	computed: {
	},
	mounted() {
		window.scrollUp = this.scrollUp;
    window.scrollDown = this.scrollDown;
	},
	methods: {
		changeReadStatus(key) {
			const param = {
				title : this.title,
				status : key
			}
      this.$store.commit('changeReadStatus', param);
		},
		add() {
			this.$store.commit('add');
		},
    scrollUp() {
			this.$refs.articlePanel.scrollTop += 30;
			console.log(this.$refs.articlePanel.scrollTop)
    },
		scrollDown() {
			this.$refs.articlePanel.scrollTop -= 30;
			console.log(this.$refs.articlePanel.scrollTop)
		}


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
</style>
