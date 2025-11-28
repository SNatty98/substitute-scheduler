<script setup>
import { computed } from 'vue';

const props = defineProps({
    label: String,
    modelValue: String,
    error: String,
    required: {
        type:Boolean, default:false
    },
    placeholder: String,
    rows: {
        type: Number,
        default: 4
    }

});

const emit = defineEmits(['update:modelValue']);

const textareaId = computed(() => `textarea-${Math.random().toString(36).substr(2, 9)}`);
</script>

<template>
    <div class="form-group">
        <label :for="textareaId" class="form-label">
            {{label}}
            <span v-if="required" class="required"></span>
        </label>
        <textarea 
            :id="textareaId"
            :value="modelValue"
            :placeholder="placeholder"
            :required="required"
            :rows="rows"
            @input="emit('update:modelValue', $event.target.value)"
            :class="['form-textarea', {'input-error': error}]" 
        />
        <span v-if="error" class="error-message">{{error}}</span>
    </div>
</template>

<style scoped>
.form-group {
  margin-bottom: var(--spacing-md);
}

.form-label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: var(--font-medium);
  color: var(--color-text);
  font-size: var(--font-sm);
}

.required {
  color: var(--color-error);
  margin-left: var(--spacing-xs);
}

.form-textarea {
  width: 100%;
  padding: var(--spacing-sm) 0.75rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: var(--font-base);
  font-family: inherit;
  transition: border-color var(--transition-base);
  background: var(--color-bg-white);
  color: var(--color-text);
  resize: vertical;
}

.form-textarea:focus {
  outline: none;
  border-color: var(--color-primary);
}

.form-textarea.input-error {
  border-color: var(--color-error);
}

.error-message {
  display: block;
  margin-top: var(--spacing-xs);
  font-size: var(--font-sm);
  color: var(--color-error);
}
</style>