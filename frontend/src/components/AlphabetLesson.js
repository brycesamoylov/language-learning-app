import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material';

const AlphabetLesson = ({ content }) => {
  if (!content || !content.letters) {
    console.error('Missing alphabet content or letters:', content);
    return <Typography>No alphabet content available</Typography>;
  }

  // Convert flat letters array into rows of 6 letters each
  const rows = content.letters.reduce((acc, letter, index) => {
    const rowIndex = Math.floor(index / 6);
    if (!acc[rowIndex]) {
      acc[rowIndex] = [];
    }
    acc[rowIndex].push(letter);
    return acc;
  }, []);

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        {content.introduction || "Greek Alphabet"}
      </Typography>
      <Typography variant="body1" paragraph>
        {content.description || "Learn the Greek alphabet and its pronunciation."}
      </Typography>
      
      {rows.map((row, rowIndex) => (
        <Grid container spacing={2} key={rowIndex} sx={{ mb: 2 }}>
          {row.map((letter, letterIndex) => (
            <Grid item xs={12} sm={6} md={2} key={`${rowIndex}-${letterIndex}`}>
              <Card sx={{ height: '100%' }}>
                <CardContent>
                  <Typography variant="h3" component="div" gutterBottom align="center" sx={{ fontWeight: 'bold' }}>
                    {letter.letter}
                  </Typography>
                  <Typography variant="h6" color="text.secondary" align="center" gutterBottom>
                    {letter.name}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    Transliteration: {letter.transliteration}
                  </Typography>
                  <Typography variant="body1" sx={{ mb: 1 }}>
                    Pronunciation: {letter.pronunciation}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Example: {letter.example}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      ))}
    </Box>
  );
};

export default AlphabetLesson;
