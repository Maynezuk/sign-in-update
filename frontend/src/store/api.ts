import { defineStore } from 'pinia'
import axios from 'axios';

export const useApi = defineStore('api', async () => {
    const response = await axios.get('/api/users/data', {
      withCredentials: true
    });

    const isAuth = true

    const fullName = `${response.data.surname} ${response.data.name}` || '';
})

