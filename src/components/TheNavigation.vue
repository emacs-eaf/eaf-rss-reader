<template>
	<nav id="nav">
		<ul class="nav-links">
			<li class="links">
				<router-link to="/">
					Home
				</router-link>
			</li>
		</ul>
	</nav>
</template>

<script>

export default ({
	data() {
		return{
		};
	},
})
</script>


<style scoped>
#nav {
	display: flex;
	justify-content: center;
  padding: 30px;
}
#nav a {
  color: #002fa7;
	text-decoration: none;
	font-weight: bold;

}
.nav-links {
	display: flex;
}
.links{
	padding-right: 20px;
	list-style: none;
}
.links:hover {
	text-decoration: underline;
}
#nav a.router-link-exact-active {
  color: #9966ff;
}
</style>
