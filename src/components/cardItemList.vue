<template>
	<div class="listCard">
		<mu-container
		v-for="article in infolist"
		:key="article.article_title"
		>
			<mu-card>
				<router-link :to="{name: 'Article', params:{title: article.title}}">
					<mu-card-title 
						:title="article.title" 
						class="title"
					/>
				</router-link>
				<mu-card-header 
				:title="article.author" 
				:sub-title="article.time" >
				</mu-card-header>
				<mu-card-text >
					{{article.shortDescription}}
				</mu-card-text>
				<mu-card-actions>
					<router-link :to="{name: 'Article', params:{title: article.title}}">
						<mu-button flat>Read</mu-button>
					</router-link>
					<mu-button flat>Action 2</mu-button>
				</mu-card-actions>
			</mu-card>
		</mu-container>
	</div>
</template>

<script>
import {mapGetters} from 'vuex';

export default {
	name: 'cardItemList',
	data () {
		return {
			backgroundColor: "",
			foregroundColor: "",
			num: 0,
		};
	},
	computed: {
		...mapGetters(['curFeedArticleList', 'infolist'])
	},
	mounted() {
		window.initCardItemListColor = this.initCardItemListColor;
		window.getpic = this.getpic
		window.getitem = this.get_item
  },
	methods: {
		initCardItemListColor(backgroundColor, foregroundColor) {
			this.backgroundColor = backgroundColor;
			this.foregroundColor = foregroundColor;
    },
		addFiles(files) {
			this.$store.commit('updateFileInfos', files);
		},
	}
}
</script>


<style scoped>
.listCard {
	position: relative;
	margin-top: 110px;
	margin-left: 700px;
}

.mu-card-header {
	text-align:left;
	margin-top: -20px;
	margin-bottom: -20px;
}

.mu-card {
	width: 100%; 
	max-width: 575px; 
	margin-top: 20px;
	margin-bottom: 20px;
	position: relative;
}

.title{
	text-align:left;
	margin-top: -10px;
	margin-bottom: -10px;
}

.mu-card-text{
	text-align:left;
	
}
</style>
