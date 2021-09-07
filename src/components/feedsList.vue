<template>
	<div class="feedsList">
		<div class="mu-appbars-title">
		<mu-appbar 
			color="white" 
			textColor="black" 
			title="Feeds List"
			style="width: 100%;"/>

		<div v-for="feed in $store.state.feedsList" 
		:key="feed.feed_title"
		class="mu-appbars">
			<mu-appbar 
			color="white" 
			textColor="black">
				{{feed.feed_title}}
				<mu-button 
				class="mu-appbars-button"
				@click="changeCurFeed(feed.feed_title)">
					check this feed
				</mu-button>
			</mu-appbar>
		</div>
		<div class="addFeedLinkWidget">
			<mu-text-field v-model="feedLink" placeholder="Please input feed link......">
			</mu-text-field><br/>
			<mu-button @click="addFeedLink(feedLink)">add</mu-button>
		</div>
		</div>
	</div>
</template>

<script>
import { QWebChannel } from "qwebchannel";

export default ({
	
	data() {
		return {
			feedLink: '',
		};	
	},
	mounted() {
		window.addFeedLink = this.addFeedLink;
		window.removeFeedLink = this.removeFeedLink;
	},
	created() {
		// eslint-disable-next-line no-undef
		new QWebChannel(qt.webChannelTransport, channel => {
			window.pyobject = channel.objects.pyobject;
		});
  },
	methods: {
		changeCurFeed(feed_title) {
			this.$store.commit('changeCurFeed', feed_title);
			this.$store.commit('changeCurFeedIndex')
		},
		addFeedLink() {
			window.pyobject.add_feedlink(this.feedLink);
		},
		removeFeedLink() {
			window.pyobject.remove_feed_link(this.feedLink);
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

