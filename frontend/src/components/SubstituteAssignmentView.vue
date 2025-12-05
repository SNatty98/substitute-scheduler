<script setup>
import { onMounted, ref } from 'vue';
import { assignmentService } from '../services/assignmentService';
import Button from '../components/Button.vue'
import FormTextArea from './FormTextArea.vue';
import { applicationService } from '../services/applicationService';

const props = defineProps({
    assignmentId:Number
});

const loading = ref(false);
const applying = ref(false)
const error = ref('');
const applicationError = ref('')
const assignment = ref(null)
const applicationMessage = ref('')

async function loadAssignment() {

    loading.value = true;
    error.value = '';
    try {
        assignment.value = await assignmentService.getById(props.assignmentId);
        console.log('Assignment loaded:', assignment.value);
    } catch(err) {
        error.value = "Failed to retrieve assignment."
    } finally {
        loading.value = false;
    }
}

onMounted(async () =>{
    await loadAssignment()
});

async function handleApplication() {
    if (!applicationMessage.value.trim()) {
        applicationError.value = 'Please provide a message';
        return;
    }

    applying.value = true;  
    applicationError.value = '';
    try {
        await applicationService.apply(props.assignmentId, applicationMessage.value)
        alert('Application submitted successfully!');
        goBack();
    }
    catch(err) {
        applicationError.value = "Failed to submit application."
    } 
    finally {
        applying.value = false;
    }
}

function goBack() {
    window.location.href="/substitute/dashboard";
}
</script>

<template>
  <div class="details-page">
    <div class="container">
      <div v-if="loading" class="loading-state">
        Loading assignment details...
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <Button @click="goBack">Back to Dashboard</Button>
      </div>

      <div v-else-if="assignment" class="details-content">
        <div class="details-header">
          <Button variant="secondary" @click="goBack">Back to Dashboard</Button>
          <span :class="['status-badge', `badge-${assignment.status}`]">
            {{ assignment.status }}
          </span>
        </div>

        <!-- Assignment Info Card -->
        <div class="info-card">
          <h1 class="school-name">{{ assignment.school_name }}</h1>
          
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Subject:</span>
              <span class="value">{{ assignment.subject }}</span>
            </div>

            <div class="info-item">
              <span class="label">Date:</span>
              <span class="value">{{ assignment.date }}</span>
            </div>

            <div class="info-item">
              <span class="label">Time:</span>
              <span class="value">
                {{ assignment.start_time.slice(0, 5) }} - {{ assignment.end_time.slice(0, 5) }}
              </span>
            </div>

            <div class="info-item">
              <span class="label">Year Group:</span>
              <span class="value">{{ assignment.year_group || 'Not specified' }}</span>
            </div>

            <div class="info-item">
              <span class="label">Postcode:</span>
              <span class="value">{{ assignment.school_postcode }}</span>
            </div>

            <div class="info-item">
              <span class="label">Distance:</span>
              <span class="value">{{ assignment.distance }} miles</span>
            </div>

            <div class="info-item">
              <span class="label">Applications:</span>
              <span class="value">{{ assignment.applications?.length || 0 }}</span>
            </div>
            
          </div>

          <div v-if="assignment.notes" class="notes-section">
            <span class="label">Notes:</span>
            <p class="notes-text">{{ assignment.notes }}</p>
          </div>
        </div>

   <!-- Application Section -->
        <div class="application-section">
            <h2>Apply for this Assignment</h2>
  
            <FormTextArea 
            label="Why are you a good fit for this assignment?"
            v-model="applicationMessage"
            :required="true"
            placeholder="Tell the school why you're suitable for this position..."
            :rows="4"
            />

            <div v-if="applicationError" class="error-alert">
                {{ applicationError }}
            </div>

            <Button 
            variant="success" 
            :loading="applying"
            @click="handleApplication"
            >
            Submit Application
            </Button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.details-page {
  min-height: 100vh;
  background: var(--color-bg);
  padding: var(--spacing-xl) 0;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
}

.loading-state,
.error-state {
  text-align: center;
  padding: var(--spacing-2xl);
  background: var(--color-bg-white);
  border-radius: var(--radius-md);
  color: var(--color-text-light);
}

.error-state {
  color: var(--color-error);
}

.error-state p {
  margin-bottom: var(--spacing-lg);
}

.details-content {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Header */
.details-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-badge {
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  font-weight: var(--font-semibold);
  text-transform: capitalize;
}

.badge-open {
  background: var(--color-success);
  color: var(--color-bg-white);
}

.badge-filled {
  background: var(--color-secondary);
  color: var(--color-bg-white);
}

.badge-cancelled {
  background: var(--color-danger);
  color: var(--color-bg-white);
}

.info-card {
  background: var(--color-bg-white);
  border-radius: var(--radius-md);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}

.school-name {
  margin: 0 0 var(--spacing-lg) 0;
  font-size: var(--font-2xl);
  color: var(--color-text);
  font-weight: var(--font-semibold);
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.info-item {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.label {
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  color: var(--color-text-light);
}

.value {
  font-size: var(--font-base);
  color: var(--color-text);
}

.notes-section {
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
}

.notes-text {
  margin: var(--spacing-sm) 0 0 0;
  color: var(--color-text);
  line-height: 1.6;
}

.application-section {
  background: var(--color-bg-white);
  border-radius: var(--radius-md);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}
</style>