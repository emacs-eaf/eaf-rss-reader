<template>
	<div class="feedsList">
		<div class="mu-appbars-title">
		<mu-appbar 
			color="white" 
			textColor="black" 
			title="Feeds List"
			style="width: 100%;"/>
		<div class="feed-list" ref="feedlist">
		<div v-for="feed in $store.state.feedsList" 
		:key="feed.feed_title"
		class="mu-appbars"
		>
			<mu-appbar color="white" textColor="black">
				{{feed.feed_title}}
				<mu-button  class="mu-appbars-button" @click="changeCurFeed(feed.feed_title)">
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
		window.selectNextFeed = this.selectNextFeed;
		window.selectPrevFeed = this.selectPrevFeed;
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
			this.$store.commit('changeCurFeedIndex');
		},
		addFeedLink(new_feedlink) {
			const index = this.$store.state.feedsList.findIndex(x => x.feed_link === new_feedlink);
			if (index != -1){
				alert("Feedlink '"+new_feedlink+"' exists.");
			}
			else{
				window.pyobject.add_feedlink(new_feedlink);
			}
			this.feedLink = '';
		},
		removeFeedLink() {
			window.pyobject.remove_feed_link(this.feedLink);
		},
		keepSelectVisible() {
       this.$refs.feedlist.children[this.currentIndex].scrollIntoViewIfNeeded(false);
     },
		selectFeedByIndex(index) {
       /*
			 if (index >= this.fileNumber) {
         this.currentIndex = this.fileNumber - 1;
       } else if (index <= 0) {
         this.currentIndex = 0;
       } else {
         this.currentIndex = index;
       }

       this.keepSelectVisible();

       this.updatePreview();*/
     },
		selectNextFeed() {
			this.selectFileByIndex(this.currentIndex + 1);
		},
		selectPrevFeed() {
			this.selectFileByIndex(this.currentIndex - 1);
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
</style>

