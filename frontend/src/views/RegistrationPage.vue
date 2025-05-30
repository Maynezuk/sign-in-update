<script setup lang="ts">
import axios from 'axios';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import MyButton from '@/components/MyButton.vue';
import MyForm from '@/components/MyForm.vue';
import MyInput from '@/components/MyInput.vue';


interface UserRegister {
    name: string;
    surname: string;
    middlename: string;
    login: string;
    password: string;
    repass: string;
}

const router =useRouter()

const user = ref<UserRegister>({
    name: '',
    surname: '',
    middlename: '',
    login: '',
    password: '',
    repass: ''
})

// Показ пароля
const showPassword = ref(false);

const showRepass = ref(false);

const togglePasswordVisibility = () => {
  showPassword.value = !showPassword.value;
};

const toggleRepassVisibility = () => {
  showRepass.value = !showRepass.value;
};

const passwordFieldType = computed(() => {
  return showPassword.value ? 'text' : 'password';
});

const repassFieldType = computed(() => {
  return showRepass.value ? 'text' : 'password';
});

// Регистрация
const registerUser = async () => {
    if (user.value.password !== user.value.repass) { // Проверка на соответствие паролей
        alert('Пароль не совпадает');
        return;
    }
    
    try {
        const response = await axios.post('/api/users/', { // Создание пользователя
            name: user.value.name,
            surname: user.value.surname,
            middlename: user.value.middlename,
            login: user.value.login,
            password: user.value.password
        });
        
        if (response.status === 200) { // Переход на страницу входа, если збс
            await router.push('/login');
        }

    // Обработка ошибок
    } catch (error) {
        if (axios.isAxiosError(error)) {
            alert(error.response?.data?.message || 'Ошибка регистрации');
        } else {
            console.error('Неизвестная ошибка:', error);
            alert('Неизвестная ошибка при регистрации');
        }
    }
}

</script>

<template>
    <my-form @submit.prevent="registerUser">
        <h2>Регистрация</h2>
        <my-input v-model="user.name" type="text" placeholder="Имя" @keydown.space.prevent required/>
        <my-input v-model="user.surname" type="text" placeholder="Фамилия" @keydown.space.prevent required/>
        <my-input v-model="user.middlename" type="text" placeholder="Отчество (при наличии)" @keydown.space.prevent/>
        <hr>
        <my-input v-model="user.login" type="text" placeholder="Логин" @keydown.space.prevent required/>
        <my-input v-model="user.password" :type="passwordFieldType" placeholder="Пароль" @keydown.space.prevent required/>
        <div>
            <input
                class="pass-show"
                type="checkbox"
                :checked="showPassword"
                @change="togglePasswordVisibility"
            >
            <span>Показать пароль</span>
        </div>
        <my-input v-model="user.repass" :type="repassFieldType" placeholder="Подтвердите пароль" @keydown.space.prevent required/>
        <div class="end-of-form">
            <div>
                <input
                    class="pass-show"
                    type="checkbox"
                    :checked="showRepass"
                    @change="toggleRepassVisibility"
                >
                <span>Показать пароль</span>
            </div>
            <router-link to="/login">Есть аккаунт?</router-link>
        </div>
        <my-button type="submit" class="btn">Зарегистрироваться</my-button>
    </my-form>
</template>

<style scoped>
h2 {
    align-self: center;
}

hr {
    color: rgb(225, 225, 225);
    width: 95%;
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