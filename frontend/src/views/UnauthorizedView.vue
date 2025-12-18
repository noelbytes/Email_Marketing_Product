<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="unauthorized surface">
    <h2>Access restricted</h2>
    <p>
      Your current role does not grant access to this area. Contact an organization administrator to
      request the proper permissions.
    </p>
    <RouterLink class="text-button" to="/">Return to Mission Control</RouterLink>
  </section>
</template>

<style scoped>
.unauthorized {
  padding: 2rem;
  margin: 4rem auto;
  max-width: 480px;
  text-align: center;
}

.text-button {
  display: inline-block;
  margin-top: 1rem;
  color: var(--md-sys-color-primary);
  font-weight: 600;
}
</style>
