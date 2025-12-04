<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { assignmentService } from '../services/assignmentService';
import AssignmentCard from './AssignmentCard.vue';

const assignments = ref([]);
const loading = ref(true);
const error = ref('');

const props = defineProps({
  mode:{
    type:String,
    required:                                                                                                                                                  true,
    validator: (value) => ['admin', 'substitute'].includes(value)
  }
});

async function loadAssignments() {
  try {
    if(props.mode === 'admin')
    { 
      assignments.value = await assignmentService.getAll();
    } 
    else 
    {
      assignments.value = await assignmentService.getAvailable();
    }
    console.log('Assignments loaded:', assignments.value);
  } catch (err) {
    console.error('Failed to load assignments:', err);
    error.value = 'Failed to load assignments';
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadAssignments();
  window.addEventListener('refresh-assignments', loadAssignments);
});

onUnmounted(() => {
  window.removeEventListener('refresh-assignments', loadAssignments);
});
</script>

<template>
  <div>
    <div v-if="loading" class="loading-state">
      Loading assignments...
    </div>

    <div v-else-if="error" class="error-state">
      {{ error }}
    </div>

    <div v-else-if="assignments.length === 0" class="empty-state">
      <p>No assignments yet.</p>
      <p class="hint">Click "Create Assignment" to add your first assignment</p>
    </div>

    <div v-else class="assignments-grid">
      <AssignmentCard 
        v-for="assignment in assignments" 
        :id="assignment.id"
        :school_name="assignment.school_name"
        :subject="assignment.subject"
        :date="assignment.date"
        :start_time="assignment.start_time"
        :end_time="assignment.end_time"
        :status="assignment.status"
        :application_count="assignment.application_count"
        :postcode="assignment.school_postcode"
        :linkprefix="props.mode"
      />
    </div>
  </div>
</template>

<style scoped>
.loading-state,
.error-state,
.empty-state {
  padding: var(--spacing-2xl);
  text-align: center;
  background: var(--color-bg-white);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  color: var(--color-text-light);
}

.error-state {
  color: var(--color-error);
  border-color: var(--color-error);
}

.empty-state p {
  margin: 0;
}

.hint {
  margin-top: var(--spacing-sm);
  font-size: var(--font-sm);
  color: var(--color-text-muted);
}

.assignments-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: var(--spacing-md);
}
</style>