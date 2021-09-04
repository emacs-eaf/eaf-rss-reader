<template>
	<div  class="article">
		<GoBack />
		<div class="article-page" ref="article">
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
				@click="scrollUp"
				color="blue"
				textColor="white"
				>
					Up
				</mu-button>
				<mu-button 
				@click="scrollDown"
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
	name: 'Article',
	components: {
		GoBack
	},
	
	data() {
		return {
			list:null
		};
	},
	props:{
		title: {
			type: String,
			required: true
		}
	},
	computed: {
		...mapGetters(['curFeedArticleList']),
		article(){
			return this.curFeedArticleList.find(
				article => article.title === this.title
			)
		}
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
			this.$refs.article.scrollTop += 30;
			console.log(this.$refs.article.scrollTop)
    },
		scrollDown() {
			this.$refs.article.scrollTop -= 30;
			console.log(this.$refs.article.scrollTop)
		},
	}
}
</script>

<style scoped>
.Article{
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
