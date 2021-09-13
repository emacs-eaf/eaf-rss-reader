<template>
	<div class="feedsList">
		<div class="content">
			
			<button @click="selectPrevFeed()">prev</button>
			<button @click="selectNextFeed()">next</button>
			
			<div class="mu-appbars-title">
				<mu-menu cover>
					<mu-appbar 
					color="white" 
					textColor="black" 
					style="text-align: center;">
						Feeds List
						<mu-button style="float: right;">add feed</mu-button>
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
				@click="changeCurFeedByIndex(feed.feed_index)"
				:key="feed.feed_index">
					<mu-appbar  textColor="black" :style="{'background':itemBackgroundColor(feed)}">
						{{feed.feed_title}}
					</mu-appbar>
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
			newFeedLink: '',
			backgroundColor:"white",
			selectColor: "grey",
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
		itemBackgroundColor(feed) {
			if (feed.feed_index == this.$store.state.curFeedIndex) {
				return this.selectColor;
			} else {
				return this.backgroundColor;
			}
    },
		removeFeedLink() {
			window.pyobject.remove_feed_link(this.feedLink);
		},
		keepSelectVisible() {
			this.$refs.feedlist.children[this.$store.state.curFeedIndex].scrollIntoViewIfNeeded(false);
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
		selectNextFeed() {
			this.selectFeedByIndex(this.$store.state.curFeedIndex + 1);
		},
		selectPrevFeed() {
			this.selectFeedByIndex(this.$store.state.curFeedIndex - 1);
		}
	}
})
</script>

<style scoped>

.content {
	position: fixed;
	width: 35%;
	margin-top: 100px;

  flex-direction: row;

	flex: 1 1 0px;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.mu-appbars-title {
	width: 100%;
	position: relative;
	display: flex;
	flex-direction: column;
}

.mu-appbars {
	width: 100%;
	position: relative;
	display: flex;
}

.mu-appbar {
	width: 100%;
	position: relative;
}

.mu-appbars-button {
	position: relative;
	float: right;
}

.feeds-list {
	width: 100%;
	height: 75%;
	overflow: scroll;
}
</style>

