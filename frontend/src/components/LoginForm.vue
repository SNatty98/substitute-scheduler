<script setup>
import { ref } from 'vue';
import { authService } from '../services/authService';
import FormInput from './FormInput.vue';
import Button from './Button.vue';

const username = ref('');
const password = ref('');
const error = ref('');
const loading = ref(false);

async function handleSubmit() {
  error.value = '';
  loading.value = true;

  try {
    await authService.login(username.value, password.value);
    const user = await authService.getCurrentUser();

    if (user.role === 'admin') {
      window.location.href = '/admin/dashboard';
    } else {
      window.location.href = '/substitute/dashboard';
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Login failed. Please check your credentials.';
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <form @submit.prevent="handleSubmit">
    <FormInput
      label="Username"
      type="text"
      v-model="username"
      required
      placeholder="Enter your username"
    />

    <FormInput
      label="Password"
      type="password"
      v-model="password"
      required
      placeholder="Enter your password"
    />

    <div v-if="error" class="error-alert">
      {{ error }}
    </div>

    <Button type="submit" :loading="loading">
      Login
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