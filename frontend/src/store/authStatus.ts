import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {
  const fullName = ref('')

  const timerID = ref(0)

  async function fetchToken(token: string) {
    try {
      const response = await axios.get('/api/users/data', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });



      fullName.value = `, ${response.data.surname} ${response.data.name}`;
      const time = response.data.timer_sec * 1000;
      timerID.value = setTimeout(() => {
        logout()
      }, time);



    } catch (error) {
      logout();
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  function logout() {
    fullName.value = '';
    localStorage.removeItem('token')
  }

  return { fetchToken, fullName, timerID }
})