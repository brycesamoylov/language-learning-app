import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  IconButton,
  Stack,
} from '@mui/material';
import {
  NavigateBefore as NavigateBeforeIcon,
  NavigateNext as NavigateNextIcon,
  Visibility as VisibilityIcon,
} from '@mui/icons-material';

const SpacedRepetitionLesson = ({ content }) => {
  const [currentIndex, setCurrentIndex] = useState(0);
  const [showAnswer, setShowAnswer] = useState(false);

  if (!content || !content.words) {
    console.error('Missing spaced repetition content:', content);
    return <Typography>No practice content available</Typography>;
  }

  const words = content.words;

  const handleNext = () => {
    setCurrentIndex((prev) => (prev + 1) % words.length);
    setShowAnswer(false);
  };

  const handlePrevious = () => {
    setCurrentIndex((prev) => (prev - 1 + words.length) % words.length);
    setShowAnswer(false);
  };

  const handleToggleAnswer = () => {
    setShowAnswer(!showAnswer);
  };

  const currentWord = words[currentIndex];

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom align="center">
        Spaced Repetition Practice
      </Typography>
      <Typography variant="subtitle1" gutterBottom align="center" color="text.secondary">
        Card {currentIndex + 1} of {words.length}
      </Typography>

      <Card sx={{ maxWidth: 600, mx: 'auto', my: 4 }}>
        <CardContent>
          <Box sx={{ minHeight: 200, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            <Typography variant="h3" gutterBottom align="center">
              {currentWord.word}
            </Typography>
            
            {showAnswer && (
              <Box sx={{ mt: 4, textAlign: 'center' }}>
                <Typography variant="h5" color="text.secondary" gutterBottom>
                  {currentWord.translation}
                </Typography>
                <Typography variant="h6" color="text.secondary" gutterBottom>
                  {currentWord.transliteration}
                </Typography>
                <Typography variant="body1" color="text.secondary" gutterBottom>
                  Pronunciation: {currentWord.pronunciation}
                </Typography>
                {currentWord.example && (
                  <Typography variant="body1" color="text.secondary">
                    Example: {currentWord.example}
                  </Typography>
                )}
              </Box>
            )}
          </Box>

          <Stack direction="row" spacing={2} justifyContent="center" sx={{ mt: 2 }}>
            <Button
              variant="outlined"
              startIcon={<VisibilityIcon />}
              onClick={handleToggleAnswer}
            >
              {showAnswer ? 'Hide Answer' : 'Show Answer'}
            </Button>
          </Stack>
        </CardContent>
      </Card>

      <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2, mt: 2 }}>
        <IconButton 
          onClick={handlePrevious}
          size="large"
          sx={{ bgcolor: 'background.paper', boxShadow: 1 }}
        >
          <NavigateBeforeIcon />
        </IconButton>
        <IconButton 
          onClick={handleNext}
          size="large"
          sx={{ bgcolor: 'background.paper', boxShadow: 1 }}
        >
          <NavigateNextIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default SpacedRepetitionLesson;
