import React from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
} from '@mui/material';

const GreetingsLesson = ({ content }) => {
  if (!content || !content.greetings) {
    console.error('Missing greetings content:', content);
    return <Typography>No greetings content available</Typography>;
  }

  return (
    <Box sx={{ p: 2 }}>
      <Typography variant="h4" gutterBottom>
        {content.introduction || "Basic Greetings and Farewells"}
      </Typography>
      <Typography variant="body1" paragraph>
        {content.description || "Learn common Greek expressions for greeting people and saying goodbye."}
      </Typography>

      <Grid container spacing={2}>
        {content.greetings.map((greeting, index) => (
          <Grid item xs={12} sm={6} key={index}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs={12}>
                    <Typography variant="h5" gutterBottom>
                      {greeting.word}
                    </Typography>
                    <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                      {greeting.transliteration}
                    </Typography>
                    <Typography variant="h6" gutterBottom>
                      {greeting.translation}
                    </Typography>
                    <Box sx={{ 
                      bgcolor: 'rgba(156, 39, 176, 0.1)', 
                      p: 2, 
                      borderRadius: 2,
                      border: '1px solid rgba(156, 39, 176, 0.3)',
                      mt: 2
                    }}>
                      <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                        <strong>{greeting.category.charAt(0).toUpperCase() + greeting.category.slice(1)}</strong>
                        <br />
                        {greeting.context}
                      </Typography>
                    </Box>
                  </Grid>
                </Grid>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Example Situations */}
      {content.example_situations && content.example_situations.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h5" gutterBottom>
            Practice Scenarios
          </Typography>
          <Grid container spacing={2}>
            {content.example_situations.map((situation, index) => (
              <Grid item xs={12} sm={6} md={3} key={index}>
                <Card sx={{ height: '100%', bgcolor: 'primary.light' }}>
                  <CardContent>
                    <Typography variant="body1" color="primary.contrastText">
                      {situation}
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Box>
  );
};

export default GreetingsLesson;
