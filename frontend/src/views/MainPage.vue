<script setup lang="ts">
import MyButton from '@/components/MyButton.vue';
// import axios from 'axios';
import { useAuthStatus } from '@/store/authStatus';

const authStatus = useAuthStatus()

const token =localStorage.getItem('token')

// Выход из системы
const userLogout = async () => {
  try {
    await authStatus.logout()
  } catch (error) {
    console.error('Ошибка при выходе:', error);
  }
}; 
</script>

<template>
  <div>
    <div class="greeting">
      <h1>Добро пожаловать на сайт{{ authStatus.fullName }}!</h1>
    </div>
    <div class="btn-container">
      <my-button v-if="token != null" @click="userLogout">Выход</my-button>
    </div>
  </div>
</template>

<style scoped>
.greeting {
  width: 100%;
  display: flex;
  justify-content: center;
}

.btn-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>