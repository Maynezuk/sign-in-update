<template>
    <div>
        <div class="greeting">
            <h1>Добро пожаловать на сайт, {{ fullName || 'Гость' }}!</h1>
        </div>
        <div class="btn-container">
            <my-button @click="logout">Выход</my-button>
        </div>
    </div>
</template>

<script setup lang="ts">
import MyButton from '@/components/MyButton.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
// import { useRouter } from 'vue-router';

// const router = useRouter();
const fullName = ref('');

// Получение данных токена
const fetchUserData = async () => {
  try {
    const response = await axios.get('/api/users/data', {
      withCredentials: true
    });
    
    fullName.value = `${response.data.surname} ${response.data.name}`; // Запись данных Фамилии и Имени для показа в приветствии

    // Обработка ошибок
  } catch (error) {
    alert('Ошибка сети');
    console.error('Неизвестная ошибка:', error);  
  }
};

// Выход из системы
const logout = async () => {
  try {
    await axios.post('/api/users/logout', {}, { // Удаление токена
      withCredentials: true
    });
    
    fullName.value = ''; // Очистка переменной для показа Фамилии и Имени
    
    localStorage.removeItem('isAuth') // Удаление переменной для активации функции получения данных токена

    // Обработка ошибок
  } catch (error) {
    console.error('Ошибка при выходе:', error);
  }
};

// Проверка на использование функции и её активация
onMounted(() => {
  const storedAuth = localStorage.getItem('isAuth')
  if(storedAuth){
    fetchUserData();
  }

});
</script>

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