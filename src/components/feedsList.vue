<template>
	<div class="feedsList">
		<div class="content">
		<div class="list-area">
			<div class="mu-appbars-title">
				<mu-menu cover>
					<mu-appbar 
					color="white" 
					textColor="black" 
					style="text-align: center;">
						Feeds List
						<mu-button style="float: right;" >add feed</mu-button>
					</mu-appbar>

				<mu-list slot="content">
				<mu-list-item>
					<mu-text-field
					v-model="newFeedLink"
					placeholder="Please input feed link......"
					style="margin: auto;">
					</mu-text-field>
						<mu-button @click="addFeedLink(newFeedLink)">add</mu-button>
				</mu-list-item>
				</mu-list>
				</mu-menu>
			</div>

			<div class="feeds-list" ref="feedlist">
				<div 
				v-for="feed in $store.state.feedsList" 
				class="mu-appbars"
						
				:key="feed.feed_index">
					<div class="feed-title" @click="changeCurFeedByIndex(feed.feed_index), cleanArticle(), changeOpenFeed(true)">
					<mu-appbar 
					textColor="black" :style="{'background':itemBackgroundColor(feed)}">
						{{feed.feed_title}}
					</mu-appbar>
					</div>
					<mu-button style="float: right" @click="removeFeed(feed.feed_index)">
						remove
					</mu-button>
				</div>
			</div>

		</div>
		</div>
	</div>
</template>

<script>
import { QWebChannel } from "qwebchannel";
import {mapState} from 'vuex';

export default ({
	data() {
		return {
			newFeedLink: '',
			backgroundColor:"white",
			selectColor: "grey",
		};	
	},
	computed: {
		...mapState([
		'curFeedIndex', 
		'curArticleIndex', 
		'openFeed',
		])
	},
	mounted() {
		window.addFeedLink = this.addFeedLink;
		window.removeFeedLink = this.removeFeedLink;
		window.selectFeedByIndex = this.selectFeedByIndex;
		window.removeFeed = this.removeFeed;
		window.changeCurFeedByIndex = this.changeCurFeedByIndex;
	},
	created() {
		// eslint-disable-next-line no-undef
		new QWebChannel(qt.webChannelTransport, channel => {
			window.pyobject = channel.objects.pyobject;
		});
  },
	methods: {
		changeCurFeedByIndex(feed_index) {
			this.$store.commit('changeCurFeedIndex', feed_index);
		},
		addIcon (iconFile) {
			return ''
		},
		addFeedLink(new_feedlink) {
			const index = this.$store.state.feedsList.findIndex(x => x.feed_link === new_feedlink);
			if (index != -1) {
				alert("Feedlink '"+new_feedlink+"' exists.");
			} else {
				window.pyobject.add_feedlink(new_feedlink);
			}
			this.newFeedLink = '';
		},
		
		removeFeed(feedlink_index) {
			window.pyobject.remove_feedlink(feedlink_index, this.curFeedIndex);
		},
		itemBackgroundColor(feed) {
			if (feed.feed_index == this.curFeedIndex) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
    },
		
		keepSelectVisible() {
			this.$refs.feedlist.children[this.curFeedIndex].scrollIntoViewIfNeeded(false);
    },
		selectFeedByIndex(index) {
			var len = this.$store.state.feedsList.length;
			if (index >= len) {
				this.changeCurFeedByIndex(len - 1)
			} else if (index <= 0) {
				this.changeCurFeedByIndex(0)
			} else {
				this.changeCurFeedByIndex(index)
			}
			this.keepSelectVisible();
		},
		changeOpenFeed(status) {
			this.$store.commit('changeOpenFeed', status);
		},
		cleanArticle()
		{
			this.$store.commit('changeCurArticleIndex', -1);
		}
	}
})
</script>

<style scoped>

.feedsList {
	width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
	
}

.list-area {
   flex: 1 1 0px;
   height: 100%;
   display: flex;
   flex-direction: column;
 }

.content {
	position: fixed;
	width: 35%;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.mu-appbars-title {
	width: 100%;
	
	display: flex;
	flex-direction: column;
}

.mu-appbars {
	width: 100%;
	display: flex;
}

.feed-title {
	width: 100%;
}



.mu-appbars-button {
	float: right;
}

.feeds-list {
	width: 100%;
	height: 70%;
	overflow: scroll;
}
</style>

