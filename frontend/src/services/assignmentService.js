import api from './api';

export const assignmentService = {
    async create(assignmentData) {
        const { data } = await api.post('/assignments/', assignmentData);
        return data;
    }
};