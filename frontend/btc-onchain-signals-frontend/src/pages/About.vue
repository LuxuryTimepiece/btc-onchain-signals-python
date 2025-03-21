<template>
  <div class="min-h-screen bg-gray-900">
    <NavBar />
    <div class="p-6 bg-gray-800 text-white rounded-lg shadow-lg max-w-4xl mx-auto my-8">
      <h1 class="text-3xl font-bold mb-4 text-yellow-500 border-b-2 border-yellow-500 pb-2">
        About Bitcoin On-Chain Signals Engine
      </h1>
      <p class="mb-4 text-lg leading-relaxed">
        The Bitcoin On-Chain Signals Engine is a web-based application designed to analyze Bitcoin’s on-chain data and price trends to generate trading signals. This project combines real-time blockchain metrics (e.g., active addresses, transaction volume) with technical indicators like the Relative Strength Index (RSI) to provide actionable insights for traders.
      </p>
      <h2 class="text-2xl font-semibold mb-2 text-yellow-400 mt-6">
        Inspiration
      </h2>
      <p class="mb-4 text-lg leading-relaxed">
        This app draws inspiration from the innovative work of Dr. Yves J. Hilpisch, founder and CEO of The Python Quants. Dr. Hilpisch is a renowned figure in the financial technology space, known for his contributions to quantitative finance through Python, including his book *Python for Finance* and the *dawp* (Data Analysis with Python) repository. His focus on leveraging Python for data-driven financial analysis and real-time market insights has been a guiding light for this project.
      </p>
      <h2 class="text-2xl font-semibold mb-2 text-yellow-400 mt-6">
        Project Details
      </h2>
      <ul class="list-disc pl-6 mb-4 space-y-2 text-lg">
        <li><strong class="text-yellow-300">Data Sources:</strong> CoinGecko API (price data) and Blockchain.com API (on-chain metrics).</li>
        <li><strong class="text-yellow-300">Technologies:</strong> Vue.js (frontend), Python (backend with Flask), Chart.js (visualizations), Tailwind CSS (styling).</li>
        <li><strong class="text-yellow-300">Features:</strong> Real-time dashboard, signal generation, backtesting, and responsive design.</li>
      </ul>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
  name: 'AboutView',
  components: {
    NavBar,
  },
};
</script>