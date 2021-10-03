<template>
	<div class="list-area">
		<div class="title-bar">
			<div class="feeds-list-title-bar">
				<h2>
					EAF-RSS-Reader
				</h2>
			</div>
			<div class="add-widget">
				<input class="input-bar" type="text" v-model="newFeedLink" placeholder="Please input feed link......">
				<button class="add-button" @click="addFeedLink(newFeedLink)">
					ADD
				</button>
			</div>
		</div>
		<div class="feeds-list" ref="feedlist">
			<div 
			class="feed"
			v-for="feed in $store.state.feedsList" 
			:key="feed.feed_index"
			:style="{'background':itemBackgroundColor(feed), 'color':itemFontColor(feed)}"
			@click="changeCurFeedByIndex(feed.feed_index), cleanArticle(), changeOpenFeed(true)">
				<div class="feed-title">
					<div class="title">
						<div>{{feed.feed_title}}</div>
						<div v-if="feed.feed_title === ''"> {{feed.feed_subtitle}}</div>
						<div v-if="feed.feed_title === '' && feed.feed_subtitle === ''"> 
							{{feed.feed_link}}
						</div>
					</div>
					<div class="sub-title">
						<div>{{feed.feed_subtitle}}</div>
						<div v-if="feed.feed_subtitle === ''"> {{feed.feed_link}}</div>
					</div>
				</div>
				<div class="button-wrapper">
					<button class="refresh" @click="refreshFeed(feed.feed_index)"
					:style="{'background':refreshButtonColor(feed)}">
						Refresh
					</button>
					<button class="remove" @click="removeFeed(feed.feed_index)"
					:style="{'background':removeButtonColor(feed)}">
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
			backgroundColor:"#F4F4F2",
			selectColor: "#515e72",
			selectFontColor:"#cfcfcf",
			selectRefreshButtonColor:"#5579dd",
			selectRemoveButtonColor:"#d6382d",
			buttonColor: "#9E9E9E",
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
		itemFontColor(feed) {
			if (feed.feed_index == this.curFeedIndex) {
				return this.selectFontColor;
			} else {
				return this.fontColor;
			}
		},
		refreshButtonColor(feed) {
			if (feed.feed_index == this.curFeedIndex) {
				return this.selectRefreshButtonColor;
			} else {
				return this.buttonColor;
			}
		},
		removeButtonColor(feed) {
			if (feed.feed_index == this.curFeedIndex) {
				return this.selectRemoveButtonColor;
			} else {
				return this.buttonColor;
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
		cleanArticle() {
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
	background-color: #F4F4F2;
	border-style: solid;
	border-width: 1px;
	border-color: #BBBFCA;
	color: #495464;
}
.title-bar {
	width: 100%;
	position: sticky;
	display: flex;
	flex-direction: row;
	background-color: #F4F4F2;
	border-style: solid;
	border-width: 1px;
	border-color: #BBBFCA;
	margin-top: -2px;
	margin-bottom: -2px;
	justify-content: space-between;
	overflow: hidden;
}
.add-widget {
	display: flex;
	flex-direction: row;
	align-self: center;
}
.feeds-list-title-bar {
	display: flex;
	text-align: left;
	font-weight: bold;
	overflow: hidden;
	padding-left: 4px;
}
input {
	align-self: center;
	width: 300px;
	height: 40px;
	background-color: #F4F4F2;
	border-style: solid;
	border-width: 2px;
	border-color: #BBBFCA;
	margin-left: 5px;
	margin-right: 5px;
}
.title {
	display: flex;
	font-size: 19px;
	font-weight: bold;
	padding-top: 2px;
	padding-bottom: 2px;
}
.sub-title { 
	display: flex;
	font-size: 17px;
	padding-top: 2px;
	padding-bottom: 2px;
}
.feed-title {
	display: flex;
	flex-direction: column;
	text-align: left;
	padding-left: 4px;
	white-space:nowrap;
	overflow:hidden;
	text-overflow: ellipsis;
}
.feeds-list {
	height: 100%;
	width: 100%;
	overflow: scroll;
	display: flex;
	flex-direction: column;
}
.feed {
	display: flex;
	flex-shrink:0;
  flex-direction: row;
	border-style: solid;
	border-width: 1px;
	border-color: #BBBFCA;
	padding-bottom: 5px;
	padding-top: 5px;
	justify-content: space-between;
}
.button-wrapper {
	display: flex;
	flex-direction: row;
	margin:auto 0;
}
button {
	width: 70px;
	height: 40px;
	font-size: 14px;
	margin-left: 5px;
	margin-right: 5px;
	font-weight: bold;
	background-color: #9E9E9E;
  color: #F4F4F2; 
	border: 1px solid #BBBFCA;
	border-radius: 4px;
}
.add-button {
	background: #5579dd;
}
</style>
