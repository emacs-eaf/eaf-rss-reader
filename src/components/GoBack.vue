<template>
	<span class="go-back">
		<mu-button 
		@click="goBack"
		color="blue"
		>goback</mu-button>
	</span>
</template>

<script>
export default {
	methods: {
		goBack() {
			return this.$router.go(-1);
		}
	},
};
</script>

<style scoped>
.go-back {
	margin-top: 0px;
	margin-left: 50px;
	position: relative;
	display: flex;
	cursor: pointer;
}

</style>
