<script setup>
import { computed } from 'vue';
const props = defineProps({
    id:Number,
    school_name:String,
    date:String,
    subject:String,
    start_time:String,
    end_time:String,
    status:String,
    application_count:Number,
    postcode:String
});
const detailsUrl = computed(() => `/admin/assignments/${props.id}`);
</script>

<template>
  <a :href="detailsUrl" class="card-link">
    <div class="assignment-card">
      <div class="card-header">
        <h3 class="school-name">{{school_name}}</h3>
        <span class="badge badge-open">{{status}}</span>
      </div>
      
      <div class="card-body">
        <div class="info-row">
          <span class="label">Subject:</span>
          <span class="value">{{subject}}</span>
        </div>
        
        <div class="info-row">
          <span class="label">Date:</span>
          <span class="value">{{date}}</span>
        </div>
        
        <div class="info-row">
          <span class="label">Time:</span>
          <span class="value">{{start_time}} - {{end_time}}</span>
        </div>
        <div class="info-row">
          <span class="label">Postcode:</span>
          <span class="value">{{postcode}}</span>
        </div>
        <div class="info-row">
          <span class="label">Application Count:</span>
          <span class="value">{{application_count}}</span>
        </div>
      </div>
      
      <div class="card-footer">
        <!-- Buttons or actions go here -->
      </div>
    </div>
  </a>
</template>


<style scoped>
.card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  transition: transform var(--transition-base);
}

.assignment-card {
  background: var(--color-bg-white);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
  transition: box-shadow var(--transition-base);
}

.assignment-card:hover {
  box-shadow: var(--shadow-md);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  border-bottom: 1px solid var(--color-border-light);
  background: var(--color-bg);
}

.school-name {
  font-size: var(--font-lg);
  font-weight: var(--font-semibold);
  color: var(--color-text);
  margin: 0;
}

.badge {
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--radius-sm);
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
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

.card-body {
  padding: var(--spacing-md);
}

.info-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--spacing-sm);
}

.info-row:last-child {
  margin-bottom: 0;
}

.label {
  color: var(--color-text-light);
  font-size: var(--font-sm);
  font-weight: var(--font-medium);
}

.value {
  color: var(--color-text);
  font-size: var(--font-sm);
}

.card-footer {
  padding: var(--spacing-md);
  border-top: 1px solid var(--color-border-light);
  background: var(--color-bg);
}
</style>