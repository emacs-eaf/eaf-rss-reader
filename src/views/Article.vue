<!--
尝试使article页面也滚动起来，但是没有实现。
目前可以尝试的解决方案是，保留一个空的article页面，然后写一个articlePanel的组建呈现文章。
那么滚动方案就类似home页面的cardListItem了。
-->

<template>
	<div  class="article" id="article">
		<h1>{{articlelist.title}}</h1>
		<articlePanel class="articlePanel" :article="articlelist()" />
	</div>
</template>

<script>
import articlePanel from "@/components/articlePanel.vue";
import {mapGetters} from 'vuex';

export default {
	name: 'Article',
	components: {
		articlePanel
	},
	data() {
		return {
			articleInfo:null
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
		
	},
	mounted() {},
	methods: {
		articlelist(){
			return this.curFeedArticleList.find(
				article => article.title === this.title
			)
		}
	}
}
</script>

<style scoped>
#article{
	max-width: 1400px;
	margin:0 auto;

	display: flex;
  flex-direction: column;
  
  width: 100%;
  height: 100%;

  position: relative;
}

::-webkit-scrollbar {
  display: none;
}

.articlePanel{
  overflow: scroll;
}
</style>
