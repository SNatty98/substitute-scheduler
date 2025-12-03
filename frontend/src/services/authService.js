import api from './api';

export const authService = {
    async login(username, password) {
        const { data } = await api.post('/auth/login/', { username, password });
        localStorage.setItem('token', data.access);
        localStorage.setItem('refresh', data.refresh);
        return data;
    },

    async getCurrentUser() {
        const { data } = await api.get('/auth/me/');
        return data;
    },

    logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        window.location.href = '/login';
    },

    isAuthenticated() {
        return !!localStorage.getItem('token');
    },

    async register_substitute(userData) {
        const { data } = await api.post(`/auth/register/substitute/`, userData)
        return data;
    }
};