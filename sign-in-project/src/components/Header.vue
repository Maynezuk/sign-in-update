<template>
    <div class="btn-container">
        <my-button @click="$router.push('/')">Главная</my-button>
        <my-button @click="$router.push('/registration')">Регистрация</my-button>
        <my-button @click="$router.push('/login')">Вход</my-button>
    </div>
</template>

<script lang="ts">
import {defineComponent} from "vue";
import MyButton from "./MyButton.vue";
export default defineComponent({
    components: {
      MyButton
    },
    name: 'Header',
})
</script>

<style scoped>
.btn-container {
    position: fixed;
    /* top: 0;
    left: 0; */
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