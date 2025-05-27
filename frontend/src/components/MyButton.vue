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
    background: linear-gradient(to right,red, rgb(255, 90, 90));
    color: white;
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
    background: linear-gradient(to right,rgb(255, 10, 10), rgb(255, 100, 100));
}
</style>