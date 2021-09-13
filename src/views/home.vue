<template>
	<div class="home" id="home">
		<h1>{{ $store.state.curFeed }}</h1>
		<button @click="selectPrevFeed()">prev</button>
		<button @click="selectNextFeed()">next</button>
		<div v-if="$store.state.curFeedIndex != -1 ">
			<div class="view-bar">
			<mu-button 
			:color="$store.state.viewKey === 'all' ? 'blue' : 'grey'"
			@click="changeViewKey('all')"
			>all</mu-button>
			<mu-button 
			:color="$store.state.viewKey === 'read' ? 'blue' : 'grey'"
			@click="changeViewKey('read')"
			>read</mu-button>
			<mu-button 
			@click="changeViewKey('unread')"
			:color="$store.state.viewKey === 'unread' ? 'blue' : 'grey'"
			>unread</mu-button>
			</div>
		</div>
		<feedsList class="feedsList" ref="feedslist" > </feedsList>
		<cardItemList class="cardItemList"></cardItemList>
	</div>
</template>

<script>
import cardItemList from "@/components/cardItemList.vue"
import feedsList from "@/components/feedsList.vue"

export default {
	name: "home",
	data () {
		return {
		};
	},
	components:{
		cardItemList,
		feedsList,
	},
	mounted() {
		window.selectNextFeed = this.selectNextFeed;
		window.selectPrevFeed = this.selectPrevFeed;
	},
	methods: {
		changeViewKey(key) {
			this.$store.commit('changeViewKey', key)
		},
		selectNextFeed() {
			this.$refs.feedslist.selectFeedByIndex(this.$store.state.curFeedIndex + 1);
		},
		selectPrevFeed() {
			this.$refs.feedslist.selectFeedByIndex(this.$store.state.curFeedIndex - 1);
		}
	}
};
</script>

<style scoped>



.view-bar {
	position: fixed;
}
#home{
	max-width: 1400px;
	margin:0 auto;

	display: flex;
  flex-direction: column;
  
  width: 100%;
  height: 100%;

  position: relative;
}

.h1 {
	position: relative;
}

::-webkit-scrollbar {
  display: none;
}

.feedsList {
	overflow: scroll;
}

.cardItemList {
  overflow: scroll;
}

.test {
  overflow: scroll;
}
</style>
