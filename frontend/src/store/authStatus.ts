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
      await logout()
      return false
    }
  };

  // Попытка обновить токен с помощью refresh токена
async function tryRefreshToken(refreshToken: string | null): Promise<boolean> {
  if (!refreshToken) {
    await logout();
    return false;
  }

  try {
    const response = await axios.post('/api/refresh', {
      refresh_token: refreshToken
    });
    
    const success = await fetchToken(response.data.access_token);
    if (!success) {
      await logout();
    }
    return success;
  } catch (error) {
    if (axios.isAxiosError(error) && error.response?.status === 401) {
      await logout();
    } else {
      console.error('Refresh error:', error);
    }
    return false;
  }
}

  // Выход из системы
async function logout() {
  const refreshToken = localStorage.getItem('token')
  if (refreshToken !== null) {
    try {
      await axios.post('/api/logout', {
        refresh_token: refreshToken
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      fullName.value = '';
      localStorage.removeItem('token');
      await router.push('/login');
    }
  }
}
  return {
    fetchToken,
    tryRefreshToken,
    logout,
    fullName,
  }
})