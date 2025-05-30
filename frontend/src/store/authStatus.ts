import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {

  const fullName = ref('Гость')

  // Получение данных токена
  async function fetchUserData(isAuth: boolean) {
    try {
      if(isAuth === true) {
        const response = await axios.get('/api/users/data', {
          withCredentials: true
        });
        fullName.value = `${response.data.surname} ${response.data.name}`; // Запись данных Фамилии и Имени для показа в приветствии
      } else {
        fullName.value = 'Гость'
      }

      // Обработка ошибок
    } catch (error) {
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  async function timer() {
    try {
      const response = await axios.get('/api/users/data', {
        withCredentials: true
      });

      const time = response.data.timer_sec * 100;

      fetchUserData(true)

      setTimeout(() => {
        fetchUserData(false)
      }, time)
    } catch (error) {
      console.error('Error in timer_sec:', error);
    }
  }

  return { fetchUserData, timer, fullName }
})