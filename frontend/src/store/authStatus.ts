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

  // Таймер, настроенный на время существования токена
  async function fetchUserDataOnTime() {
    try {
      const response = await axios.get('/api/users/data', {
        withCredentials: true
      });

      const time = response.data.timer_sec * 1000; // Перевод времени с секунд на милисекунды для таймера 

      fetchUserData(true)  // Обновление данных в приветствии

      setTimeout(() => {  // Запуск таймера
        fetchUserData(false)
      }, time)

      // Обработка ошибок
    } catch (error) {
      console.error('Error in timer_sec:', error);
    }
  }

  return { fetchUserData, fetchUserDataOnTime, fullName }
})