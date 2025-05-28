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
import axios, { AxiosError } from 'axios';
// import { useRouter } from 'vue-router';

// const router = useRouter();
const fullName = ref('');

const fetchUserData = async () => {
  try {
    const response = await axios.get('/api/users/me', {
      withCredentials: true
    });
    fullName.value = `${response.data.name} ${response.data.surname}`;
  } catch (error) {
    const axiosError = error as AxiosError;

    if (axiosError.response) {
      if (axiosError.response.status === 401) {
        console.log('Токен отсутствует')
      }
    } else {
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);  
    }
  }
};

const logout = async () => {
  try {
    await axios.post('/api/users/logout', {}, {
      withCredentials: true
    });
    fullName.value = '';
  } catch (error) {
    console.error('Ошибка при выходе:', error);
  }
};

onMounted(() => {
  fetchUserData();
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