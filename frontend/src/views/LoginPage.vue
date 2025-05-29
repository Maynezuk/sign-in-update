<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios, { AxiosError } from 'axios';
import MyButton from '@/components/MyButton.vue';
import MyForm from '@/components/MyForm.vue';
import MyInput from '@/components/MyInput.vue';

interface UserLogin {
  login: string;
  password: string;
}

const router = useRouter();

const user = ref<UserLogin>({
  login: '',
  password: ''
});

// Показ пароля
const showPassword = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const passwordFieldType = computed(() => {
  return showPassword.value ? 'text' : 'password';
});

// Авторизация
const loginUser = async () => {
  try {
    await axios.post('/api/users/login', {
      login: user.value.login,
      password: user.value.password
    }, {
      withCredentials: true
    });
    
    localStorage.setItem('isAuth', 'true') // Сохранение переменной для существования токена
    
    // Таймер существования переменной
    const response = await axios.get('/api/users/data', {
      withCredentials: true
    });
    const delToken = () => {localStorage.removeItem('isAuth')}
    const time = response.data.timer_sec * 1000
    setTimeout(delToken, time)

    await router.push('/');
    
    // Обработка ошибок
  } catch (error) {
    const axiosError = error as AxiosError;
    if (axiosError.response) {
      switch (axiosError.response.status) {
        case 404:
          alert('Пользователь не найден!');
          break;
        case 401:
          alert('Неверный пароль!');
          break;
        default:
          alert('Ошибка сервера');
      }
    } else {
      alert('Ошибка сети');
      console.error('Неизвестная ошибка:', error);  
    }
  }
};
</script>

<template>
  <my-form @submit.prevent="loginUser">
    <h2>Вход в аккаунт</h2>
    <my-input v-model="user.login" type="text" placeholder="Введите логин" @keydown.space.prevent required />
    <my-input v-model="user.password" :type="passwordFieldType" placeholder="Введите пароль" @keydown.space.prevent
      required />
    <div class="end-of-form">
      <div>
        <input class="pass-show" type="checkbox" :checked="showPassword" @change="togglePasswordVisibility">
        <span>Показать пароль</span>
      </div>
      <router-link to="/registration">Нет аккаунта?</router-link>
    </div>
    <my-button type="submit" class="btn">Войти</my-button>
  </my-form>
</template>

<style scoped>
h2 {
  align-self: center;
}

.end-of-form {
  display: flex;
  justify-content: space-between;
}

.pass-show {
  margin: 5px;
}

span {
  font-size: small;
}

a {
  font-size: small;
  margin-top: 5px;
  text-decoration: none;
  color: black;
}

a:hover {
  text-decoration: underline;
}
</style>