import { defineStore } from 'pinia'
import axios, { AxiosError } from 'axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export const useAuthStatus = defineStore('authStatus', () => {
  const fullName = ref('')

  const router = useRouter()

  // Получение данных пользователя по access токену
  async function fetchToken(token: string) {
    try {
      const response = await axios.get('/api/data', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      fullName.value = `, ${response.data.surname} ${response.data.name}`;
      return true
    } catch (error) {
      // Обновление токена, если access токен истек
      if ((error as AxiosError)?.response?.status === 401) {
        return tryRefreshToken(localStorage.getItem('token'))
      }
      logout()
      return false
    }
  };

  // Попытка обновить токен с помощью refresh токена
  async function tryRefreshToken(refreshToken: string | null): Promise<boolean> {
    if (refreshToken === null) {
      logout()
      return false
    } else {
      try {
        const response = await axios.post('/api/refresh', {
          refresh_token: refreshToken
        });
        return await fetchToken(response.data.access_token)
      } catch (error) {
        console.log(error)
        logout()
        return false
      }
    }
  }

  // Выход из системы
  function logout() {
    fullName.value = ''
    localStorage.removeItem('token')
    router.push('/login')
  }

  return {
    fetchToken,
    tryRefreshToken,
    logout,
    fullName,
  }
})