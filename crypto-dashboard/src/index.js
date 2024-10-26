import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  typography: {
    fontFamily: 'Montserrat Regular, Arial, sans-serif',
    h1: {
      fontFamily: 'Montserrat Bold',
      fontWeight: 100,
    },
    h2: {
      fontFamily: 'Montserrat Bold',
      fontWeight: 80,
    },
    body1: {
      fontFamily: 'Montserrat Regular',
      fontWeight: 16,
    },
  },
});


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <App />
    </ThemeProvider>
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
