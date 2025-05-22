<template>
    <input :value="modelValue" @input="updateInput" class="input" type="text">
</template>

<script lang="ts">
import { defineComponent} from "vue";
import type { PropType } from "vue";


export default defineComponent({
    name: 'my-input',
    props: {
        modelValue: {
            type: [String, Number] as PropType<string | number>,
            required: true
        }
    },
    methods: {
        updateInput(event: Event) {
            this.$emit('update:modelValue', (event.target as HTMLInputElement).value)
        }
    }
})
</script>

<style scoped>
.input {
    margin: 5px 0;
    padding: 10px;
    border: 1px solid rgb(225, 225, 225);
    border-radius: 15px;
    background: none;
}
</style>