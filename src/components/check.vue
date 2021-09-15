<template>
  <div class="check">
    <div class="curFeedIndex">
      <li>curFeedIndex:{{curFeedIndex}}</li>
    </div>

    <div class="curArticleIndex">
      <li>curArticleIndex:{{curArticleIndex}}</li>
    </div>

    <div class="openFeed">
      <li>openFeed:{{openFeed}}</li>
    </div>

    <div class="openArticle">
      <li>openArticle:{{openArticle}}</li>
    </div>
  </div>
</template>

<script>
import { mapState} from 'vuex'

export default {
  computed: {
    ...mapState([
		'curFeedIndex', 
		'curArticleIndex', 
		'openFeed', 
		'openArticle']),
  }
}
  
</script>
<style>
.check {
  flex-direction: row;
  background: white;
}
</style>