<script setup lang="ts">
import MyButton from '@/components/MyButton.vue';
import axios from 'axios';
import { useAuthStatus } from '@/store/authStatus';

const authStatus = useAuthStatus()

// Выход из системы
const logout = async () => {
  try {
    // Удалние токена

    clearTimeout(authStatus.timerID);  // Вроде бы и бесполезно, а вроде бы и не плохо
    authStatus.fullName = '';
    // delete axios.defaults.headers.common['Authorization'];
  
  } catch (error) {
    console.error('Ошибка при выходе:', error);
  }
}; 

const checkToken = async () => {
  try {
    const response = await axios.get('/api/users/data', {
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('token')}`
      }
    });

    // authStatus.fullName = `, ${response.data.surname} ${response.data.name}`;

    alert('Токен существует!')
  } catch (error) {
    alert('Попытка не удалась: токен истёк!');
    console.error('Попытка не удалась:', error);
  }
}
</script>

<template>
  <div>
    <div class="greeting">
      <h1>Добро пожаловать на сайт{{ authStatus.fullName }}!</h1>
    </div>
    <div class="btn-container">
      <my-button @click="logout">Выход</my-button>
      <my-button @click="checkToken">Проверить токен</my-button>
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