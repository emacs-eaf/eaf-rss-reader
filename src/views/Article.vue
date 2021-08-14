<template>
	<div class="article-page">
		<GoBack />
		<section class="article">
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
			<router-view></router-view>
		</section>
	</div>
</template>

<script>
import GoBack from "@/components/GoBack.vue";
import {mapGetters} from 'vuex';

export default ({
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
		go(src) {
			window.location.href=src;
		}
	}
})
</script>

<style scoped>

.article-page{
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
