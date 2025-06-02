import { defineStore } from 'pinia'
import axios from 'axios';
import { ref } from 'vue';

export const useAuthStatus = defineStore('authStatus', () => {

  const fullName = ref('Гость')

  async function fetchUserNameData(isAuth: boolean) {
    try {
      if (isAuth === true) {
        const response = await axios.get('/api/users/data', {
          withCredentials: true
        });
        const time = response.data.timer_sec * 1000; // Перевод времени с секунд на милисекунды для таймера 

        fullName.value = `${response.data.surname} ${response.data.name}`; // Запись данных Фамилии и Имени для показа в приветствии

        setTimeout(() => {  // Запуск таймера
          fullName.value = 'Гость'
        }, time)
      } else {
        fullName.value = 'Гость'
      }
      // Обработка ошибок
    } catch (error) {
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);
    }
  };

  return { fetchUserNameData, fullName }
})