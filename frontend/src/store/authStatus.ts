import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('api', () => {
  const isAuth = ref(false)

  async function timer_sec() {
    try {
      const response = await axios.get('/api/users/data', {
        withCredentials: true
      });

      const time = response.data.timer_sec * 1000;

      setTimeout(() => {
        isAuth.value = false;
      }, time)
    } catch (error) {
      console.error('Error in timer_sec:', error);
    }
  }

  const fullName = ref('Гость')


  return { isAuth, timer_sec, fullName }
})