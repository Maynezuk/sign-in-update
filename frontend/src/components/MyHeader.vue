<template>
    <div class="btn-container">
        <my-button @click="$router.push('/')">Главная</my-button>
        <my-button @click="$router.push('/registration')">Регистрация</my-button>
        <my-button @click="$router.push('/login')">Вход</my-button>
    </div>
</template>

<script setup lang="ts">
import MyButton from "@/components/MyButton.vue";
</script>

<style scoped>
.btn-container {
    position: fixed;
    display: inline-flex;
    justify-content: center;
    height: 50px;
    background-color: whitesmoke;
    border: 1px solid rgb(225, 225, 225);
    border-radius: 0 0 10px 0;
}

@media (max-width: 800px) {
  .btn-container {
    display: flex;
    position: relative;
    border-radius: 0;
  }
}
</style>