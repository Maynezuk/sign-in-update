<script setup lang="ts">
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import axios, { AxiosError } from 'axios';
import MyButton from '@/components/MyButton.vue';
import MyForm from '@/components/MyForm.vue';
import MyInput from '@/components/MyInput.vue';
import { useAuthStatus } from '@/store/authStatus';

interface UserLogin {
  login: string;
  password: string;
}

const router = useRouter();

const user = ref<UserLogin>({
  login: '',
  password: ''
});

const authStatus = useAuthStatus()

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
    const response = await axios.post('/api/login', {
      login: user.value.login,
      password: user.value.password
    });

    authStatus.fetchToken(response.data.access_token);
    localStorage.setItem('token', response.data.refresh_token)

    await router.push('/');

  } catch (error) {
    const axiosError = error as AxiosError;
    if (axiosError.response && axiosError.response.status === 404) {
      alert('Не найден пользователь или некорректный пароль!');
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