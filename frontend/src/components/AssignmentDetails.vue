<script setup>
import { ref, onMounted } from 'vue';
import { assignmentService } from '../services/assignmentService';
import Button from './Button.vue';

const assignment = ref(null);
const loading = ref(true);
const error = ref('');
const selectingApplication = ref(null);

const props = defineProps({
    assignmentId:Number
});

onMounted(async () => {
    await loadAssignment(); 
});

async function loadAssignment() {
    
  loading.value = true;
  error.value = '';
  try {
    assignment.value = await assignmentService.getById(props.assignmentId)
  }
  catch (err) {
    error.value = 'Failed to load assignment.'
  }
  finally {
     loading.value = false;
  }
}

async function handleSelectSubstitute(applicationId) {
    
  loading.value = true;
  error.value = '';
  try {
    await assignmentService.selectSubstitute(props.assignmentId, applicationId);
    alert('Substitute selected successfully!');
    goBack();
  }
  catch(err) {
    error.value = "Failed to select substitute."
  } 
  finally {
    loading.value = false;
  }
}

function goBack() {
  window.location.href = '/admin/dashboard';
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
          <Button variant="secondary" @click="goBack">← Back to Dashboard</Button>
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
              <span class="label">Applications:</span>
              <span class="value">{{ assignment.applications?.length || 0 }}</span>
            </div>
          </div>

          <div v-if="assignment.notes" class="notes-section">
            <span class="label">Notes:</span>
            <p class="notes-text">{{ assignment.notes }}</p>
          </div>
        </div>

        <!-- Applications Section -->
        <div class="applications-section">
          <h2>Applications</h2>

          <div v-if="!assignment.applications || assignment.applications.length === 0" class="no-applications">
            <p>No applications received yet.</p>
          </div>

          <div v-else class="applications-list">
            <div 
              v-for="application in assignment.applications" 
              :key="application.id"
              class="application-card"
            >
              <div class="application-header">
                <div class="substitute-info">
                  <h3 class="substitute-name">
                    {{ application.substitute.user.first_name }} 
                    {{ application.substitute.user.last_name }}
                  </h3>
                  <span class="distance">{{ Number(application.distance).toFixed(1)}} miles away</span>
                </div>
                <span :class="['app-status-badge', `badge-${application.status}`]">
                  {{ application.status }}
                </span>
              </div>

              <div v-if="application.message" class="application-message">
                <span class="label">Message:</span>
                <p>{{ application.message }}</p>
              </div>

              <div class="application-footer">
                <Button 
                  v-if="application.status === 'pending' && assignment.status === 'open'"
                  variant="success"
                  :loading="selectingApplication === application.id"
                  @click="handleSelectSubstitute(application.id)"
                >
                  Select Substitute
                </Button>
                <span v-else-if="application.status === 'accepted'" class="selected-text">
                  ✓ Selected
                </span>
              </div>
            </div>
          </div>
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
  max-width: 900px;
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

/* Assignment Info Card */
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

/* Applications Section */
.applications-section {
  background: var(--color-bg-white);
  border-radius: var(--radius-md);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-sm);
}

.applications-section h2 {
  margin: 0 0 var(--spacing-lg) 0;
  font-size: var(--font-xl);
  color: var(--color-text);
  font-weight: var(--font-semibold);
}

.no-applications {
  text-align: center;
  padding: var(--spacing-2xl);
  color: var(--color-text-light);
  background: var(--color-bg);
  border-radius: var(--radius-md);
}

.applications-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

/* Application Card */
.application-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  background: var(--color-bg);
}

.application-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-md);
}

.substitute-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.substitute-name {
  margin: 0;
  font-size: var(--font-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
}

.distance {
  font-size: var(--font-sm);
  color: var(--color-text-light);
}

.app-status-badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
  text-transform: capitalize;
}

.badge-pending {
  background: var(--color-warning);
  color: var(--color-text);
}

.badge-accepted {
  background: var(--color-success);
  color: var(--color-bg-white);
}

.badge-rejected {
  background: var(--color-danger);
  color: var(--color-bg-white);
}

.application-message {
  margin-bottom: var(--spacing-md);
}

.application-message p {
  margin: var(--spacing-xs) 0 0 0;
  color: var(--color-text);
  font-style: italic;
}

.application-footer {
  display: flex;
  justify-content: flex-end;
}

.selected-text {
  color: var(--color-success);
  font-weight: var(--font-semibold);
  font-size: var(--font-base);
}
</style>