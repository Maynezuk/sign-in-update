<template>
    <input :value="modelValue" @input="updateInput" class="input" type="text">
</template>

<script setup lang="ts">

defineOptions({
    name: 'my-input'
})

defineProps({
    modelValue: {
        required: true
    }
})

const emit = defineEmits(['update:modelValue'])

const updateInput = (event: Event) => {
    emit('update:modelValue', (event.target as HTMLInputElement).value)
}
</script>

<style scoped>
.input {
    margin: 5px 0;
    padding: 10px;
    border: 1px solid rgb(225, 225, 225);
    border-radius: 15px;
    background: none;
    font-size: 16px;
}
</style>