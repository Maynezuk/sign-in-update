<template>
    <div class="content">
      <form>
        <slot></slot>
      </form>
  </div>
</template>

<script setup lang="ts">
defineOptions({
  name: 'my-form',
})
</script>

<style scoped>
.content {
    display: flex;
    margin-top: 100px;
    justify-content: center;
}

form {
    margin: auto;
    background-color: whitesmoke;
    border: 1px solid rgb(225, 225, 225);
    border-radius: 12px;
    min-height: 50px;
    min-width: 300px;
    padding: 20px;
    display: flex;
    flex-direction: column;
}

@media (max-width: 800px) {
  .content {
    margin-top: 50px;
  }
}
</style>