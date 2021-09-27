<template>
	<div class="list-area">
		<div class="title-bar">
			<div class="feeds-list-title-bar">
				<p>Feeds List</p>
			</div>
			<div class="add-widget">
				<input type="text" v-model="newFeedLink" placeholder="Please input feed link......">
				<button class="add-button" @click="addFeedLink(newFeedLink)">
					Add
				</button>
			</div>
		</div>
		<div class="feeds-list" ref="feedlist">
			<div 
			class="feed"
			v-for="feed in $store.state.feedsList" 
			:key="feed.feed_index"
			:style="{'background':itemBackgroundColor(feed)}"
			@click="changeCurFeedByIndex(feed.feed_index), cleanArticle(), changeOpenFeed(true)">
				<div class="feed-title" 
				>
					<div class = "title" style="font-size:19px;font-weight:bold;">
						{{feed.feed_title}}
					</div>
					<div class="sub-title">
						{{feed.feed_subtitle}}
					</div>
					<div v-if="feed.feed_subtitle === ''">
						{{feed.feed_link}}
					</div>
				</div>
				<div class="button-wraper">
					<button class="refresh" @click="refreshFeed(feed.feed_index)">
						Refresh
					</button>
					<button class="remove" @click="removeFeed(feed.feed_index)">
						Remove
					</button>
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
			isAdd:false,
			newFeedLink: '',
			backgroundColor:"white",
			selectColor: "#F5F5F5",
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
		window.refreshFeed = this.refreshFeed;
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
		refreshFeed(feedlink_index) {
			window.pyobject.refresh_rsshub_list(feedlink_index);
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

.list-area {
	display: flex;
	width: 100%;
	height: 100%;
	flex-direction: column;
	overflow: hidden;

}

.title-bar {
	width: 100%;
	
	position: sticky;
	display: flex;
	flex-direction: row;
	background-color:white;

	border-style: solid;
	border-width: 1px;
	border-color: #DCDCDC;

	justify-content: space-between;
	overflow: hidden;

}

.add-widget {
	display: flex;
	flex-direction: row;
	align-self: center;
}

.feeds-list-title-bar {
	text-align: left;
	font-size: 22px;
	font-weight: bold;

}

input {
	align-self: center;
	width: 300px;
}

.add-button {
	text-align: center;
	align-self: center;
}

.feed-title {
	display: flex;
	flex-direction: column;
	text-align: left;
}

.feeds-list {
	overflow: scroll;
}

.feed {
	font-size: 17px;
	display: flex;
  flex-direction: row;
	
	border-style: solid;
	border-width: 1px;
	border-color: #DCDCDC;
	
	padding-bottom: 5px;
	padding-top: 5px;

	justify-content: space-between;
	word-break:break-all;
}

.button-wraper {
	display: flex;
	flex-direction: row;
}

button {
	background-color:#9E9E9E;
  color: white; 
	border: 1px solid #DCDCDC;
}

.refresh:hover {
	background-color: #2196F3; 
}
.remove:hover {
	background-color: #be352b; 
}
.add-button:hover {
	background-color: #2196F3; 
}
</style>

