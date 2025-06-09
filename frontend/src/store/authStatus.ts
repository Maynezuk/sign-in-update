import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {
  const fullName = ref('')

  const timerID = ref(0)

  const loginDate = ref(0)

  async function fetchToken(token: string) {
    try {
      const response = await axios.get('/api/users/data', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });



      fullName.value = `, ${response.data.surname} ${response.data.name}`;
      const time = response.data.timer_sec * 1000;
      // if(loginData + time <= Date.now()){
      //   logout()
      // }
      loginDate.value = Number(localStorage.getItem('loginDate'))


      timerID.value = setInterval(() => {
        console.log(loginDate.value + '   ' + Date.now())
        if (loginDate.value + time <= Date.now()) {
          logout()
        }
      }, 500);



    } catch (error) {
      logout();
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  function logout() {
    fullName.value = '';
    localStorage.removeItem('token')
    localStorage.removeItem('loginDate')
    loginDate.value = 0
    clearInterval(timerID.value)
  }

  return { fetchToken, logout, fullName, timerID, loginDate }
})