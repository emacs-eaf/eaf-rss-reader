import Vue from 'vue'
import Router from 'vue-router'
import home from './views/home.vue'
import Article from './views/Article.vue'

Vue.use(Router)

export default new Router({
  mode: "history",
  routes: [
    {
      path:"/",
      name:"home",
      component: home,
      props: true
    },
    {
      path: "/details/:title",
      name: "Article",
      props: true,
      component: Article,
      children: [
        
      ]
    },
    
  ]
})
