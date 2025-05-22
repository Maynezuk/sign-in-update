<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router';
import Header from '@/components/Header.vue'
</script>

<template>
  <div class="app">
    <Header></Header>
    <div class="head">
      <div class="img-container">
        <img class="pride-img"
          src="@/assets/logo.png"
          alt="Логотип pride" />
      </div>
    </div>
    <RouterView></RouterView>
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
