<template>
  <nav class="bg-gray-800 p-4">
    <div class="container mx-auto flex justify-between items-center">
      <router-link to="/" class="text-white text-xl font-bold">Bitcoin On-Chain Signals</router-link>
      <div class="space-x-4">
        <router-link to="/" class="text-yellow-500 hover:text-yellow-300">Dashboard</router-link>
        <router-link to="/about" class="text-yellow-500 hover:text-yellow-300">About</router-link>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
};
</script>