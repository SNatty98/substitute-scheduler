import api from './api';

export const applicationService = {
    async apply(id, applicationData) {
        const { data } = await api.post(`/applications/`, {
            assignment: id,
            message: applicationData
        });
        return data;
    }
}