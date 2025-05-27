<template>
    <div>
        <div class="greeting">
            <h1>Добро пожаловать на сайт, {{ userSurname + ' ' + userName || 'Гость' }}!</h1>
        </div>
    </div>
</template>

<script setup lang="ts">

import { ref, onMounted } from 'vue';

const userName = ref('');
const userSurname = ref('');

onMounted(() => {
    const storedName = localStorage.getItem('userName');
    const storedSurname = localStorage.getItem('userSurname');
    if (storedName) {
        userName.value = storedName;
    }

    if (storedSurname) {
        userSurname.value = storedSurname;
    }
});

</script>

<style scoped>
.greeting {
    width: 100%;
    display: flex;
    justify-content: center;
}
</style>