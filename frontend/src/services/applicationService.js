import api from './api';

export const applicationService = {
    async apply(id, applicationData) {
        console.log("reached apply")

        const { data } = await api.post(`/applications/`, {
            assignment: id,
            message: applicationData
        });
        return data;
    }
}