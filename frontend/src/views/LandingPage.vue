<template>
    <div class="landing-page">
        <h1>Welcome to Our Application</h1>
        <p>This is the landing page of our application.</p>
        <router-link to="/login_register" class="btn btn-primary">SignIn/SignUp</router-link>
    </div>
</template>

<script setup lang="ts">
</script>

<style>
.landing-page {
    text-align: center;
    margin-top: 50px;
}
</style>