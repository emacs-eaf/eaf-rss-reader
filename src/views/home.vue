<template>
	<div class="home" id="home">
		<h1>{{ $store.state.curFeed }}</h1>
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
		<feedsList class="feedsList"> </feedsList>
		<cardItemList class="cardItemList"></cardItemList>
	</div>
</template>

<script>
import cardItemList from "@/components/cardItemList.vue"
import feedsList from "@/components/feedsList.vue"

export default {
	name: "home",
	components:{
		cardItemList,
		feedsList,
	},
	data () {
		return {
		};
	},
	methods: {
		changeViewKey(key) {
			this.$store.commit('changeViewKey', key)
		}
	}
};
</script>

<style scoped>

<<<<<<< HEAD

=======
html, body {
   width: 100%;
   height: 100%;
   margin: 0;
   padding: 0;
 }
>>>>>>> 936291adf39121e1c2f26dcbd3078b3a012b1e0e

.view-bar {
	position: fixed;
}
#home{
	max-width: 1400px;
	margin:0 auto;

	display: flex;
  flex-direction: column;
<<<<<<< HEAD
  
=======
  align-items: center;
  justify-content: center;
>>>>>>> 936291adf39121e1c2f26dcbd3078b3a012b1e0e
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
<<<<<<< HEAD

.cardItemList {
  overflow: scroll;
}

.test {
=======

.cardItemList {
>>>>>>> 936291adf39121e1c2f26dcbd3078b3a012b1e0e
  overflow: scroll;
}
</style>
