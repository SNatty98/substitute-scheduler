<script setup>
const props = defineProps({
    show : {
        type: Boolean,
        default:false
    }
});

const emit = defineEmits(['close']);
</script>

<template>
    <Teleport to="body">
        <Transition name="modal">
            <div v-if="show" class="modal-backdrop" @click="emit('close')">
                <div class="modal-content" @click.stop>
                    <slot></slot>
                </div>
            </div>
        </Transition>
    </Teleport>
</template>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: var(--z-modal);
  padding: var(--spacing-md);
  overflow-y: auto;
}

.modal-content {
  max-height: 90vh;
  overflow-y: auto;
}

/* Transition animations */
.modal-enter-active,
.modal-leave-active {
  transition: opacity var(--transition-base);
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}
</style>