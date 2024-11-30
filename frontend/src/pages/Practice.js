import React, { useState, useEffect } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  Typography,
} from '@mui/material';
import axios from 'axios';

const Practice = () => {
  const [phrases, setPhrases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchLessonContent = async () => {
      try {
        setLoading(true);
        const lessonId = localStorage.getItem('currentLessonId');
        const languageCode = localStorage.getItem('currentLanguageCode') || 'el';

        if (!lessonId) {
          throw new Error('No lesson ID found');
        }

        console.log('Fetching lesson:', languageCode, lessonId);
        const response = await axios.get(`/api/lessons/${languageCode}/${lessonId}`);
        console.log('Lesson response:', response.data);
        
        const content = response.data.content;
        if (!content) {
          throw new Error('No content found in lesson');
        }

        // Extract practice words based on the lesson content structure
        let practiceWords = [];
        if (content.practice_words) {
          if (Array.isArray(content.practice_words)) {
            // Handle array format
            practiceWords = content.practice_words.map(word => ({
              word: typeof word === 'object' ? word.word : word,
              explanation: typeof word === 'object' ? 
                (word.mnemonic || word.context || word.translation || word.explanation || 'No explanation available') 
                : 'No explanation available'
            }));
          } else if (typeof content.practice_words === 'string') {
            // Handle string format (word1:explanation1;word2:explanation2)
            practiceWords = content.practice_words.split(';').map(pair => {
              const [word, explanation] = pair.split(':');
              return { word, explanation: explanation || 'No explanation available' };
            });
          }
        }

        if (practiceWords.length === 0) {
          throw new Error('No practice words found in lesson content');
        }

        console.log('Setting phrases:', practiceWords);
        setPhrases(practiceWords);
      } catch (error) {
        console.error('Error fetching lesson content:', error);
        setError(error.message || 'Failed to load lesson content');
      } finally {
        setLoading(false);
      }
    };

    fetchLessonContent();
  }, []);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography>Loading practice content...</Typography>
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Typography color="error">{error}</Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Practice Mode
      </Typography>
      <Grid container spacing={3}>
        {phrases.map((phrase, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  {phrase.word}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {phrase.explanation}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
};

export default Practice;
