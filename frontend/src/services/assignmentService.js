import api from './api';

export const assignmentService = {
    async create(assignmentData) {
        const { data } = await api.post(`/assignments/`, assignmentData);
        return data;
    },

    async getAll() {
        const { data } = await api.get(`/assignments/`);
        return data;
    },

    async getById(id) {
        const { data } = await api.get(`/assignments/${id}/`);
        return data;
    },

    async getAvailable() {
        const { data } = await api.get(`/assignments/available/`);
        return data;
    },

    async selectSubstitute(assignmentId, applicationId) {
        const { data } = await api.post(`/assignments/${assignmentId}/select_substitute/`,
            { application_id: applicationId })
        return data;
    }
};