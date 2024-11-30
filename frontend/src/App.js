import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Navigation from './components/Navigation';
import Dashboard from './pages/Dashboard';
import Lessons from './pages/Lessons';
import VocabularyBuilder from './pages/VocabularyBuilder';
import Profile from './pages/Profile';
import Community from './pages/Community';
import Practice from './pages/Practice';
import TestLessons from './pages/TestLessons';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Navigation />
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/lessons" element={<Lessons />} />
            <Route path="/test-lessons" element={<TestLessons />} />
            <Route path="/vocabulary" element={<VocabularyBuilder />} />
            <Route path="/practice" element={<Practice />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/community" element={<Community />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
