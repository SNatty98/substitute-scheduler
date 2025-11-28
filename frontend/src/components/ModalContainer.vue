<script setup>
import { ref } from 'vue';
import Modal from './Modal.vue';
import AssignmentForm from './AssignmentForm.vue';

const showModal = ref(false);

function openModal() {
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

function handleSuccess() {
  showModal.value = false;
  alert('Assignment created successfully!');
}

defineExpose({ openModal });
</script>

<template>
  <Modal :show="showModal" @close="closeModal">
    <AssignmentForm 
      @success="handleSuccess"
      @cancel="closeModal"
    />
  </Modal>
</template>