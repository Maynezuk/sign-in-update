<script setup lang="ts">
import {RouterView } from 'vue-router';
import MyHeader from '@/components/MyHeader.vue'
</script>

<template>
  <div class="app">
    <MyHeader></MyHeader>
    <div class="head">
      <div class="img-container">
        <img class="pride-img"
          src="@/assets/logo.png"
          alt="Логотип pride" />
      </div>
    </div>
    <RouterView/>
  </div>
</template>

<style scoped>
.head {
  display: flex;
  justify-content: end;
}

.img-container {
  margin: 15px;
}

.pride-img {
  width: 200px;
}

@media (max-width: 800px) {
  .head {
    justify-content: center;
  }
}
</style>
