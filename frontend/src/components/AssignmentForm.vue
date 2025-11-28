<script setup>
import {ref} from 'vue';
import {assignmentService} from '../services/assignmentService.js';
import FormInput from './FormInput.vue';
import FormTextArea from './FormTextArea.vue';
import Button from './Button.vue';

const emit = defineEmits(['success', 'cancel']);

const formData = ref({
    school_name:'',
    school_postcode:'',
    date:'',
    start_time:'',
    end_time:'',
    subject:'',
    year_group:'',
    notes:''
});

const loading = ref(false)
const error = ref('')
const errors = ref({})

async function handleSubmit() {
    error.value='';
    errors.value={};
    loading.value = true;

    try {
        const assignment = await assignmentService.create(formData.value);
        emit('success', assignment);
    } catch(err) {
    if (err.response?.data) {
      errors.value = err.response.data;
      error.value = 'Please check the form for errors';
    } else {
      error.value = 'Failed to create assignment. Please try again.';
    }
  } finally {
    loading.value = false;
  }
}

function handleCancel() {
    emit('cancel');
}
</script>

<template>
  <form @submit.prevent="handleSubmit" class="assignment-form">
    <h2>Create Assignment</h2>

    <div v-if="error" class="error-alert">
      {{ error }}
    </div>

    <FormInput
      label="School Name"
      v-model="formData.school_name"
      :error="errors.school_name?.[0]"
      required
      placeholder="e.g. Springfield Primary School"
    />

    <FormInput
      label="School Postcode"
      v-model="formData.school_postcode"
      :error="errors.school_postcode?.[0]"
      required
      placeholder="e.g. SW1A 1AA"
    />

    <FormInput
      label="Date"
      type="date"
      v-model="formData.date"
      :error="errors.date?.[0]"
      required
    />

    <div class="form-row">
      <FormInput
        label="Start Time"
        type="time"
        v-model="formData.start_time"
        :error="errors.start_time?.[0]"
        required
      />

      <FormInput
        label="End Time"
        type="time"
        v-model="formData.end_time"
        :error="errors.end_time?.[0]"
        required
      />
    </div>

    <FormInput
      label="Subject"
      v-model="formData.subject"
      :error="errors.subject?.[0]"
      required
      placeholder="e.g. Mathematics"
    />

    <FormInput
      label="Year Group"
      v-model="formData.year_group"
      :error="errors.year_group?.[0]"
      placeholder="e.g. Year 7"
    />

    <FormTextArea
      label="Notes"
      v-model="formData.notes"
      :error="errors.notes?.[0]"
      placeholder="Any additional information for substitutes..."
      :rows="3"
    />

    <div class="form-actions">
      <Button type="button" variant="secondary" @click="handleCancel">
        Cancel
      </Button>
      <Button type="submit" :loading="loading">
        Create Assignment
      </Button>
    </div>
  </form>
</template>

<style scoped>
.assignment-form {
  background: var(--color-bg-white);
  padding: var(--spacing-xl);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-md);
  max-width: 600px;
}

h2 {
  margin-bottom: var(--spacing-lg);
  color: var(--color-text);
  font-size: var(--font-xl);
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

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
}

.form-actions {
  display: flex;
  gap: var(--spacing-md);
  justify-content: flex-end;
  margin-top: var(--spacing-lg);
}
</style>