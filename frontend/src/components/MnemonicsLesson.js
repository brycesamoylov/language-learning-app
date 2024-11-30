import React, { useState } from 'react';
import {
  Box,
  Container,
  Paper,
  Typography,
  Button,
  LinearProgress,
} from '@mui/material';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';

const MnemonicsLesson = ({ lesson }) => {
  const [currentWordIndex, setCurrentWordIndex] = useState(0);

  const words = lesson?.content?.words || [];
  const currentWord = words[currentWordIndex];

  const handleNext = () => {
    setCurrentWordIndex((prev) => (prev + 1) % words.length);
  };

  const handlePrevious = () => {
    setCurrentWordIndex((prev) => (prev - 1 + words.length) % words.length);
  };

  if (!lesson || !currentWord) {
    return <LinearProgress />;
  }

  return (
    <Container maxWidth="md" sx={{ py: 4 }}>
      <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
        <Typography variant="h4" gutterBottom align="center" color="primary">
          {lesson.title}
        </Typography>
        
        <Typography variant="body1" paragraph align="center">
          {lesson.content.description}
        </Typography>

        <Box sx={{ my: 4, textAlign: 'center' }}>
          <Typography variant="h2" gutterBottom color="primary">
            {currentWord.word}
          </Typography>
          
          <Typography variant="h5" gutterBottom color="text.secondary">
            {currentWord.transliteration}
          </Typography>
          
          <Typography variant="h6" gutterBottom>
            {currentWord.translation}
          </Typography>

          <Paper 
            elevation={1} 
            sx={{ 
              p: 2, 
              my: 2, 
              backgroundColor: 'primary.light',
              color: 'primary.contrastText'
            }}
          >
            <Typography variant="body1">
              {currentWord.mnemonic}
            </Typography>
          </Paper>
        </Box>

        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 4 }}>
          <Button
            variant="contained"
            onClick={handlePrevious}
            startIcon={<NavigateBeforeIcon />}
          >
            Previous
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            endIcon={<NavigateNextIcon />}
          >
            Next
          </Button>
        </Box>

        <Box sx={{ mt: 4 }}>
          <Typography variant="body2" color="text.secondary" align="center">
            Word {currentWordIndex + 1} of {words.length}
          </Typography>
        </Box>
      </Paper>
    </Container>
  );
};

export default MnemonicsLesson;
