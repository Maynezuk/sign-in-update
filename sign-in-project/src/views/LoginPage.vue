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

const showPassword = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const passwordFieldType = computed(() => {
  return showPassword.value ? 'text' : 'password';
});

const loginUser = async () => {
  try {
    const response = await axios.post(
      'http://127.0.0.1:8000/users/login',
      {
        login: user.value.login,
        password: user.value.password
      }
    );

    localStorage.setItem('isAuthenticated', 'true');
    localStorage.setItem('userId', response.data.user_id.toString());

    await router.push('/');
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
    }
  }
};
</script>

<template>
    <my-form @submit.prevent="loginUser">
        <h2>Вход в аккаунт</h2>
        <my-input
            v-model="user.login"
            type="text"
            placeholder="Введите логин"
            @keydown.space.prevent
            required
        />
        <my-input
            v-model="user.password"
            :type="passwordFieldType"
            placeholder="Введите пароль"
            @keydown.space.prevent
            required
        />
        <div class="end-of-form">
            <div>
                <input
                    class="pass-show"
                    type="checkbox"
                    :checked="showPassword"
                    @change="togglePasswordVisibility"
                >
                <span>Показать пароль</span>
            </div>
            <router-link to="/registration">Нет аккаунта?</router-link>
        </div>
        <my-button type="submit" class="btn">Вход</my-button>
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