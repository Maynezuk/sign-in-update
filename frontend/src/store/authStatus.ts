import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {
  const fullName = ref('Гость')

  const authToken = ref('')

  async function fetchUserNameData(isAuth: boolean, token?: string) {
    try {
      if (isAuth === true) {
        if (!token) {
          fullName.value = 'Гость';
          return;
        }

        authToken.value = token

        const response = await axios.get('/api/users/data', {
          headers: {
            'Authorization': `Bearer ${authToken.value}`
          }
        });
        
        const time = response.data.timer_sec * 1000;
        fullName.value = `${response.data.surname} ${response.data.name}`;

        setTimeout(() => {
          fullName.value = 'Гость';
          authToken.value = ''; // Очищаем токен по истечении времени
        }, time);
      } else {
        fullName.value = 'Гость';
        authToken.value = '';
      }
    } catch (error) {
      authToken.value = '';
      fullName.value = 'Гость';
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  return { fetchUserNameData, fullName }
})