import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {
  const fullName = ref('Гость')

  const timerID = ref(0)

  async function fetchUserNameData(isAuth: boolean, token?: string) {
    try {
      if (isAuth === true) {
        if (!token) {
          fullName.value = 'Гость';
          return;
        }

        const response = await axios.get('/api/users/data', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        const time = response.data.timer_sec * 1000;
        fullName.value = `${response.data.surname} ${response.data.name}`;

        timerID.value = setTimeout(() => {
          fullName.value = 'Гость';
        }, time);
      } else {
        fullName.value = 'Гость';
      }
    } catch (error) {
      fullName.value = 'Гость';
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  return { fetchUserNameData, fullName, timerID }
})