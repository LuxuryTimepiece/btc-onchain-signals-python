import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import './index.css';  // Relative path, should work if index.css exists in src/

const app = createApp(App);
app.use(router);
app.mount('#app');