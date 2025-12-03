<script setup>
import { ref } from 'vue';
import { authService } from '../services/authService';
import FormInput from './FormInput.vue';
import Button from './Button.vue'

const formData = ref({
    username:'',
    email:'',
    password:'',
    first_name:'',
    last_name:'',
    postcode:'',
    phone:'',
    subjects:'',
    qualifications:'',
});

const error = ref('');
const loading = ref(false);

async function handleSubmit() {
    loading.value = true;
    try{
        await authService.register_substitute(formData.value)
        alert('Registration successful! Please login.');
        window.location.href = '/login';
    } catch (err) {
        error.value =  err.response?.data?.detail || 'Register failed. Please check you have filled the form correctly.';
    } finally {
        loading.value = false;
    }
}
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <FormInput 
            label="Username" 
            type ="text" 
            v-model="formData.username" 
            required 
            placeholder="Enter your username" 
        />
          <FormInput 
            label="Email" 
            type ="email" 
            v-model="formData.email" 
            required
            placeholder="Enter your email" 
        />
          <FormInput 
            label="Password" 
            type ="password" 
            v-model="formData.password" 
            required 
            placeholder="Enter your password" 
        />
          <FormInput 
            label="First name" 
            type ="text" 
            v-model="formData.first_name" 
            required 
            placeholder="Enter your first name" 
        />
          <FormInput 
            label="Last name" 
            type ="text" 
            v-model="formData.last_name" 
            required 
            placeholder="Enter your last name" 
        />
          <FormInput 
            label="Postcode" 
            type ="text" 
            v-model="formData.postcode" 
            required 
            placeholder="Enter your postcode" 
        />
          <FormInput 
            label="Phone" 
            type ="text" 
            v-model="formData.phone" 
            required 
            placeholder="Enter your phone number" 
        />
          <FormInput 
            label="Subjects" 
            type ="text" 
            v-model="formData.subjects" 
            required 
            placeholder="Enter your subjects" 
        />
          <FormInput 
            label="Qualifications" 
            type ="text" 
            v-model="formData.qualifications" 
            required 
            placeholder="Enter your qualifications" 
        />
        <div v-if="error" class="error-alert">
            {{ error }}
        </div>

        <Button type="submit" :loading="loading" variant="success">
            Register
        </Button>
    </form>
</template>

<style scoped>
form {
  display: flex;
  flex-direction: column;
}

.error-alert {
  padding: var(--spacing-sm) 0.75rem;
  margin-bottom: var(--spacing-md);
  background: var(--color-error-bg);
  border: 1px solid var(--color-error-border);
  border-radius: var(--radius-sm);
  color: var(--color-error-text);
  font-size: var(--font-sm);
}
</style>