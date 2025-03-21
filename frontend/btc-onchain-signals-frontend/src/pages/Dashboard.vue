<template>
  <div class="min-h-screen bg-gray-900">
    <NavBar />
    <div class="p-6">
      <h1 class="text-3xl font-bold text-white mb-6">Bitcoin On-Chain Signals Engine</h1>
      <div v-if="error" class="text-red-500 mb-6">
        {{ error }}
      </div>
      <div v-else-if="loading" class="text-white">Loading...</div>
      <div v-else>
        <!-- Summary Section -->
        <div class="bg-gray-800 p-4 rounded-lg shadow-lg mb-6">
          <p class="text-lg text-white">
            Block Height: {{ data.block_height || 'N/A' }} | 
            Fee Rate: {{ data.fastest_fee || 'N/A' }} sat/byte | 
            Latest Price: ${{ data.price ? data.price.toFixed(2) : 'N/A' }} | 
            Signal: 
            <span :class="`signal-${data.signal ? data.signal.toLowerCase() : 'undefined'}`">
              {{ data.signal || 'N/A' }}
            </span>
          </p>
        </div>
        <!-- Metrics Panels -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
          <div class="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 class="text-xl font-semibold text-yellow-500">Price (USD)</h2>
            <p class="text-2xl text-white">{{ data.price ? data.price.toFixed(2) : 'N/A' }}</p>
            <p class="text-sm text-gray-400">
              24h Change: 
              <span :class="data.price_change_24h >= 0 ? 'text-green-500' : 'text-red-500'">
                {{ data.price_change_24h ? data.price_change_24h.toFixed(2) : 'N/A' }}%
              </span>
            </p>
          </div>
          <div class="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 class="text-xl font-semibold text-yellow-500">Transaction Volume (tx/s)</h2>
            <p class="text-2xl text-white">{{ data.tx_volume ? data.tx_volume.toFixed(2) : 'N/A' }}</p>
          </div>
          <div class="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 class="text-xl font-semibold text-yellow-500">Active Addresses</h2>
            <p class="text-2xl text-white">{{ data.active_addresses || 'N/A' }}</p>
          </div>
          <div class="bg-gray-800 p-4 rounded-lg shadow-lg">
            <h2 class="text-xl font-semibold text-yellow-500">RSI (14)</h2>
            <p class="text-2xl text-white">{{ data.rsi ? data.rsi.toFixed(2) : 'N/A' }}</p>
            <p class="text-sm text-gray-400">
              {{ data.rsi ? (data.rsi > 70 ? 'Overbought' : data.rsi < 30 ? 'Oversold' : 'Neutral') : '' }}
            </p>
          </div>
        </div>
        <!-- Graph Section -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg mb-6">
          <h2 class="text-2xl font-semibold text-yellow-500 mb-4">Bitcoin Price and RSI (Last 30 Days)</h2>
          <div v-if="loading" class="text-white">Loading chart...</div>
          <div v-else-if="!historicalData || historicalData.length === 0" class="text-red-500">
            No historical data available to display the chart.
          </div>
          <div v-else class="chart-container">
            <Chart type="line" :data="chartData" :options="chartOptions" />
          </div>
        </div>
        <!-- Historical Data Table -->
        <div class="bg-gray-800 p-6 rounded-lg shadow-lg">
          <h2 class="text-2xl font-semibold text-yellow-500 mb-4">Historical Data</h2>
          <div v-if="!historicalData || historicalData.length === 0" class="text-red-500">
            No historical data available.
          </div>
          <div v-else class="overflow-x-auto">
            <table class="w-full text-white">
              <thead>
                <tr class="border-b border-gray-600">
                  <th class="p-2 text-left">Timestamp</th>
                  <th class="p-2 text-left">Close ($)</th>
                  <th class="p-2 text-left">RSI</th>
                  <th class="p-2 text-left">Signal</th>
                  <th class="p-2 text-left">Transactions</th>
                  <th class="p-2 text-left">Unique Addresses</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in historicalData" :key="index" class="border-b border-gray-700">
                  <td class="p-2">{{ row.timestamp }}</td>
                  <td class="p-2">{{ row.close ? row.close.toFixed(2) : 'N/A' }}</td>
                  <td class="p-2">{{ row.rsi ? row.rsi.toFixed(2) : 'N/A' }}</td>
                  <td :class="`signal-${row.signal ? row.signal.toLowerCase() : 'undefined'}`">
                    {{ row.signal || 'N/A' }}
                  </td>
                  <td class="p-2">{{ row['n-transactions'] ? row['n-transactions'].toFixed(2) : 'N/A' }}</td>
                  <td class="p-2">{{ row['n-unique-addresses'] || 'N/A' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { io } from 'socket.io-client';
import NavBar from '../components/NavBar.vue';
import { Chart } from 'vue-chartjs';
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  TimeScale,
  CategoryScale,
} from 'chart.js';
import 'chartjs-adapter-date-fns';

// Register Chart.js components
ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, LinearScale, TimeScale, CategoryScale);

// Store the socket instance globally to reuse it
let socketInstance = null;

export default {
  name: 'DashboardView',
  components: {
    NavBar,
    Chart,
  },
  data() {
    return {
      socket: null,
      data: {},
      historicalData: [],
      loading: true,
      error: null,
      chartData: {
        labels: [],
        datasets: [],
      }, // Initialize with default empty structure
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              color: '#fff',
              font: { size: 12 },
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: '#fff',
            bodyColor: '#fff',
            callbacks: {
              label: (context) => `${context.dataset.label}: ${context.parsed.y?.toFixed(2) || 'N/A'}`,
            },
          },
          title: {
            display: true,
            text: 'Bitcoin Price and RSI Over Time',
            color: '#fff',
            font: { size: 16 },
          },
        },
        scales: {
          x: {
            type: 'time',
            time: {
              unit: 'day',
              displayFormats: {
                day: 'MMM dd',
              },
            },
            title: {
              display: true,
              text: 'Date',
              color: '#fff',
            },
            ticks: {
              color: '#fff',
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)',
            },
          },
          y: {
            type: 'linear',
            position: 'left',
            title: {
              display: true,
              text: 'Close Price ($)',
              color: '#fff',
            },
            ticks: {
              color: '#fff',
              callback: (value) => (value ? `$${value.toLocaleString()}` : 'N/A'),
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)',
            },
          },
          y1: {
            type: 'linear',
            position: 'right',
            title: {
              display: true,
              text: 'RSI',
              color: '#fff',
            },
            ticks: {
              color: '#fff',
              min: 0,
              max: 100,
              stepSize: 10,
            },
            grid: {
              drawOnChartArea: false,
            },
          },
        },
      },
    };
  },
  methods: {
    updateChart() {
      if (!this.historicalData || this.historicalData.length === 0) {
        console.error('No historical data available for chart');
        this.chartData = {
          labels: [],
          datasets: [],
        };
        return;
      }

      this.chartData = {
        labels: this.historicalData.map((row) => new Date(row.timestamp)),
        datasets: [
          {
            label: 'Close Price ($)',
            data: this.historicalData.map((row) => (row.close ? row.close : null)),
            borderColor: '#FBBF24', // Yellow-500
            backgroundColor: 'rgba(251, 191, 36, 0.2)',
            fill: false,
            tension: 0.1,
            yAxisID: 'y',
          },
          {
            label: 'RSI (14)',
            data: this.historicalData.map((row) => (row.rsi ? row.rsi : null)),
            borderColor: '#60A5FA', // Blue-400
            backgroundColor: 'rgba(96, 165, 250, 0.2)',
            fill: false,
            tension: 0.1,
            yAxisID: 'y1',
          },
        ],
      };
    },
  },
  mounted() {
    if (!socketInstance) {
      socketInstance = io('http://localhost:5000', {
        reconnection: true,
        reconnectionAttempts: 5,
        reconnectionDelay: 1000,
      });

      socketInstance.on('connect', () => {
        console.log('Connected to WebSocket server');
        socketInstance.emit('start');
      });

      socketInstance.on('update', (data) => {
        console.log('Received WebSocket update:', data);
        if (data.error) {
          this.error = data.error;
          this.loading = false;
          return;
        }
        this.data = data;
        this.historicalData = data.historical_data || [];
        this.loading = false;
        this.error = null;
        this.updateChart();
      });

      socketInstance.on('connect_error', (error) => {
        console.error('WebSocket connection error:', error);
        this.error = 'Failed to connect to the server. Please try again later.';
        this.loading = false;
      });

      socketInstance.on('error', (error) => {
        console.error('WebSocket error:', error);
        this.error = 'An error occurred while fetching data.';
        this.loading = false;
      });
    }
    this.socket = socketInstance;

    // Fallback: If no data is received within 10 seconds, show an error
    setTimeout(() => {
      if (this.loading) {
        this.error = 'Failed to load data. Server may be down.';
        this.loading = false;
      }
    }, 10000);
  },
  beforeUnmount() {
    if (this.socket) {
      this.socket.off('connect');
      this.socket.off('update');
      this.socket.off('connect_error');
      this.socket.off('error');
    }
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 400px;
  width: 100%;
}
.signal-buy {
  color: #10B981; /* Green-500 */
}
.signal-sell {
  color: #EF4444; /* Red-500 */
}
.signal-hold {
  color: #6B7280; /* Gray-500 */
}
.signal-undefined {
  color: #6B7280; /* Gray-500 */
}
</style>