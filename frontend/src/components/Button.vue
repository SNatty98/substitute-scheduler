<script setup>
const props = defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value) => ['primary', 'secondary', 'danger', 'success'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  }
});
</script>

<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="['btn', `btn-${variant}`, { 'btn-loading': loading }]"
  >
    <span v-if="loading" class="spinner"></span>
    <slot></slot>
  </button>
</template>

<style scoped>
.btn {
  padding: var(--spacing-sm) var(--spacing-lg);
  border: none;
  border-radius: var(--radius-sm);
  font-size: var(--font-base);
  font-weight: var(--font-medium);
  cursor: pointer;
  transition: all var(--transition-base);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-sm);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-primary {
  background: var(--color-primary);
  color: var(--color-bg-white);
}

.btn-primary:hover:not(:disabled) {
  background: var(--color-primary-hover);
}

.btn-secondary {
  background: var(--color-secondary);
  color: var(--color-bg-white);
}

.btn-secondary:hover:not(:disabled) {
  background: var(--color-secondary-hover);
}

.btn-danger {
  background: var(--color-danger);
  color: var(--color-bg-white);
}

.btn-danger:hover:not(:disabled) {
  background: var(--color-danger-hover);
}

.btn-success {
  background: var(--color-success);
  color: var(--color-bg-white);
}

.btn-success:hover:not(:disabled) {
  background: var(--color-success-hover);
}

.btn-loading {
  position: relative;
}

.spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: var(--color-bg-white);
  border-radius: var(--radius-full);
  animation: spin 0.6s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>