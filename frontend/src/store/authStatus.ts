import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {
  const fullName = ref('')

  const timerID = ref(0)

  async function fetchToken(token?: string) {
    try {
      if (token) {
        const response = await axios.get('/api/users/data', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        const time = response.data.timer_sec * 1000;
        fullName.value = `, ${response.data.surname} ${response.data.name}`;

        timerID.value = setTimeout(() => {
          fullName.value = '';
        }, time);
      } else {
        fullName.value = '';
      }
    } catch (error) {
      fullName.value = '';
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  return { fetchToken, fullName, timerID }
})