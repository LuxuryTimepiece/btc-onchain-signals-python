<template>
  <div class="chart-container">
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import Chart from 'chart.js/auto';

export default {
  name: 'LineChart',
  props: {
    data: {
      type: Array,
      required: true,
      default: () => [],
      validator: (value) => {
        return Array.isArray(value) && value.every(item => typeof item === 'number');
      },
    },
    label: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null;

    const createChart = () => {
      if (!chartCanvas.value || props.data.length === 0) return;

      const ctx = chartCanvas.value.getContext('2d');
      if (chartInstance) {
        chartInstance.destroy();
      }

      chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels: Array.from({ length: props.data.length }, (_, i) => i + 1),
          datasets: [
            {
              label: props.label,
              data: props.data,
              borderColor: 'rgba(234, 179, 8, 1)', // Yellow-500
              backgroundColor: 'rgba(234, 179, 8, 0.2)',
              fill: true,
              tension: 0.4,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              title: {
                display: true,
                text: 'Data Points',
              },
            },
            y: {
              title: {
                display: true,
                text: props.label,
              },
              beginAtZero: false,
            },
          },
          plugins: {
            legend: {
              display: true,
            },
          },
        },
      });
    };

    onMounted(() => {
      if (props.data.length > 0) {
        createChart();
      }
    });

    watch(() => props.data, (newData) => {
      if (newData.length > 0) {
        createChart();
      }
    });

    onUnmounted(() => {
      if (chartInstance) {
        chartInstance.destroy();
      }
    });

    return {
      chartCanvas,
    };
  },
};
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>