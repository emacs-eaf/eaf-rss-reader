<template>
	<div ref="listCard" class="listCard">
		<mu-container
		v-for="article in infolist"
		:key="article.article_title"
		>
			<mu-card>
				<router-link class="article" :to="{name: 'Article', params:{title: article.title}}">
					<mu-card-title 
						:title="article.title" 
						class="title"
					/>
				</router-link>
				<mu-card-header 
				:title="article.author" 
				:sub-title="article.time" >
				</mu-card-header>
				<mu-card-text >
					{{article.shortDescription}}
				</mu-card-text>
				<mu-card-actions>
					<router-link :to="{name: 'Article', params:{title: article.title}}">
						<mu-button flat>Read</mu-button>
					</router-link>
					<mu-button flat>Action 2</mu-button>
				</mu-card-actions>
			</mu-card>
		</mu-container>
	</div>
</template>

<script>
import {mapGetters} from 'vuex';
import { QWebChannel } from "qwebchannel";

export default {
	name: 'listCard',
	data () {
		return {
			backgroundColor: "",
			foregroundColor: "",
			num: 0,
		};
	},
	computed: {
		...mapGetters(['curFeedArticleList', 'infolist'])
	},
	mounted() {
		window.initCardItemListColor = this.initCardItemListColor;
		window.getpic = this.getpic
		window.getitem = this.get_item
		window.scrollUp = this.scrollUp;
    window.scrollDown = this.scrollDown;
  },
	created() {
		// eslint-disable-next-line no-undef
		new QWebChannel(qt.webChannelTransport, channel => {
			window.pyobject = channel.objects.pyobject;
		});
  },
	methods: {
		initCardItemListColor(backgroundColor, foregroundColor) {
			this.backgroundColor = backgroundColor;
			this.foregroundColor = foregroundColor;
    },
		addFiles(files) {
			this.$store.commit('updateFileInfos', files);
		},
		scrollUp() {
			this.$refs.listCard.scrollTop += 30;
			console.log(this.$refs.listCard.scrollTop)
    },
		scrollDown() {
			this.$refs.listCard.scrollTop -= 30;
			console.log(this.$refs.listCard.scrollTop)
		}
	}
}
</script>


<style scoped>
.listCard {
	position: relative;
	margin-top: 110px;
	margin-left: 700px;
}

.mu-card-header {
	text-align:left;
	margin-top: -20px;
	margin-bottom: -20px;
}

.mu-card {
	width: 100%; 
	max-width: 575px; 
	margin-top: 20px;
	margin-bottom: 20px;
	position: relative;
}

.title{
	text-align:left;
	margin-top: -10px;
	margin-bottom: -10px;
}

.mu-card-text{
	text-align:left;
}

::-webkit-scrollbar {
  display: none;
}

.article {
  overflow: scroll;
}

</style>
