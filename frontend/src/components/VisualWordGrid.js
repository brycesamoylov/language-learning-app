import React, { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  Paper,
  IconButton,
  Collapse,
  List,
  ListItem,
  ListItemIcon,
  ListItemText
} from '@mui/material';
import NavigateBeforeIcon from '@mui/icons-material/NavigateBefore';
import NavigateNextIcon from '@mui/icons-material/NavigateNext';
import VisibilityIcon from '@mui/icons-material/Visibility';
import VisibilityOffIcon from '@mui/icons-material/VisibilityOff';
import LightbulbIcon from '@mui/icons-material/Lightbulb';
import CircleIcon from '@mui/icons-material/Circle';

const VisualWordGrid = ({ words }) => {
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [showVisualization, setShowVisualization] = useState(false);
  
  const currentWord = words[currentWordIndex];

  // Debug logging
  console.log("Current word structure:", currentWord);

  const handleNext = () => {
    setCurrentWordIndex((prev) => (prev + 1) % words.length);
    setShowVisualization(false);
  };

  const handlePrevious = () => {
    setCurrentWordIndex((prev) => (prev - 1 + words.length) % words.length);
    setShowVisualization(false);
  };

  const toggleVisualization = () => {
    setShowVisualization(!showVisualization);
  };

  if (!currentWord) {
    return null;
  }

  return (
    <Box sx={{ width: '100%', mb: 4 }}>
      <Card 
        elevation={3}
        sx={{
          position: 'relative',
          overflow: 'visible',
          mb: 4,
          background: 'linear-gradient(145deg, #ffffff 0%, #f5f5f5 100%)'
        }}
      >
        <CardContent>
          <Grid container spacing={2}>
            {/* Word Information */}
            <Grid item xs={12}>
              <Typography variant="h3" align="center" color="primary" gutterBottom>
                {currentWord.word}
              </Typography>
              <Typography variant="h5" align="center" color="text.secondary" gutterBottom>
                {currentWord.transliteration}
              </Typography>
              <Typography variant="h4" align="center" gutterBottom>
                {currentWord.translation}
              </Typography>
            </Grid>

            {/* Visual Hint */}
            <Grid item xs={12}>
              <Paper 
                elevation={1}
                sx={{ 
                  p: 3, 
                  bgcolor: 'primary.light',
                  color: 'primary.contrastText',
                  borderRadius: 2,
                  position: 'relative'
                }}
              >
                <Typography variant="h6" gutterBottom>
                  Visual Hint:
                </Typography>
                <Typography variant="body1">
                  {currentWord.visual_hint}
                </Typography>
                <IconButton
                  onClick={toggleVisualization}
                  sx={{
                    position: 'absolute',
                    top: 8,
                    right: 8,
                    color: 'inherit'
                  }}
                >
                  {showVisualization ? <VisibilityOffIcon /> : <VisibilityIcon />}
                </IconButton>
              </Paper>
            </Grid>

            {/* Detailed Visualization */}
            <Grid item xs={12}>
              <Collapse in={showVisualization}>
                <Paper 
                  elevation={1}
                  sx={{ 
                    p: 3, 
                    bgcolor: 'background.paper',
                    borderRadius: 2,
                    mt: 2
                  }}
                >
                  <Typography variant="h6" gutterBottom>
                    Detailed Visualization:
                  </Typography>
                  <Typography variant="body1">
                    {currentWord.visualization_text}
                  </Typography>
                </Paper>
              </Collapse>
            </Grid>

            {/* Navigation Controls */}
            <Grid item xs={12}>
              <Box 
                sx={{ 
                  display: 'flex', 
                  justifyContent: 'center',
                  gap: 2,
                  mt: 2 
                }}
              >
                <Button
                  variant="contained"
                  startIcon={<NavigateBeforeIcon />}
                  onClick={handlePrevious}
                >
                  Previous
                </Button>
                <Button
                  variant="contained"
                  endIcon={<NavigateNextIcon />}
                  onClick={handleNext}
                >
                  Next
                </Button>
              </Box>
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
};

export default VisualWordGrid;
