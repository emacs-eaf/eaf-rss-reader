<!--
尝试使article页面也滚动起来，但是没有实现。
目前可以尝试的解决方案是，保留一个空的article页面，然后写一个articlePanel的组建呈现文章。
那么滚动方案就类似home页面的cardListItem了。
-->

<template>
	<div  class="article" ref="article" id="article">
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
html, body {
   width: 100%;
   height: 100%;
   margin: 0;
   padding: 0;
 }
 ::-webkit-scrollbar {
  display: none;
}
#article{
	max-width: 1400px;
	margin:0 auto;

	display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;

  position: relative;
}
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
