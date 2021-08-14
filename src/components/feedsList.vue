<template>
	<div class="feedsList">
		<div class="mu-appbars-title">
		<mu-appbar 
			color="white" 
			textColor="black" 
			title="Feeds List"
			style="width: 100%;"
		/>
		<div v-for="feed in $store.state.feedsList" 
		:key="feed.feed_title"
		class="mu-appbars">
			<mu-appbar 
			color="white" 
			textColor="black" 
			>
				{{feed.feed_title}}
				<mu-button 
				class="mu-appbars-button"
				@click="changeCurFeed(feed.feed_title)"
				>
					check this feed
				</mu-button>
			</mu-appbar>
		</div>
		</div>
	</div>
</template>

<script>
export default ({
	data() {
		return {};	
	},
	methods: {
		changeCurFeed(feed_title) {
			this.$store.commit('changeCurFeed', feed_title);
			this.$store.commit('changeCurFeedIndex')
		}
	}
})
</script>

<style scoped>

.mu-appbars-title {
	position: fixed;
	width: 35%;
	margin-top: 100px;
}

.mu-appbars {
	width: 100%;
	position: relative;
}
.mu-appbar {
	width: 100%;
	position: relative;
}

.mu-appbars-button {
	position: relative;
	float: right;
}
</style>>

