<template>
    <button class="btn" >
        <slot></slot>
    </button>
</template>

<script setup lang="ts">
defineOptions({
    name: 'my-button'
})
</script>

<style scoped>
.btn {
    border: 1px solid whitesmoke;
    background: linear-gradient(to right,red, rgb(255, 145, 145), rgb(255, 208, 208));
    height: 35px;
    padding: 0 10px;
    border-radius: 15px;
    margin: 5px;
    font-family: Arial, Helvetica, sans-serif;
    font-weight: 600;
    font-size: 18px;
}

.btn:hover {
    border: 1px solid red;
}
</style>