import axios from 'axios';

// https://xpensaapi.luxdryft.com || http:// 10.10.1.3:8000
const BASE_URL = 'https://xpensaapi.luxdryft.com';

export const apiClient = axios.create({
  baseURL: BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});
