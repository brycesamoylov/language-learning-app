import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Collapse,
  FormControl,
  Grid,
  InputLabel,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  LinearProgress,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Select,
  MenuItem,
  Typography,
  CardMedia,
} from '@mui/material';
import {
  PlayArrow as PlayArrowIcon,
  NavigateBefore as NavigateBeforeIcon,
  NavigateNext as NavigateNextIcon,
  FiberManualRecord as CircleIcon,
  School as SchoolIcon,
  Language as LanguageIcon,
  Lightbulb as LightbulbIcon,
} from '@mui/icons-material';
import AlphabetLesson from '../components/AlphabetLesson';
import SpacedRepetitionLesson from '../components/SpacedRepetitionLesson';
import MnemonicsLesson from '../components/MnemonicsLesson';

const Lessons = () => {
  const [languages, setLanguages] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState('');  // Initialize as empty string
  const [lessons, setLessons] = useState([]);
  const [loading, setLoading] = useState(true);
  const [lessonContent, setLessonContent] = useState(null);

  useEffect(() => {
    // Fetch available languages
    const fetchLanguages = async () => {
      try {
        const response = await axios.get('http://localhost:8000/languages');
        setLanguages(response.data);
        // Set default language after languages are loaded
        if (response.data.length > 0) {
          setSelectedLanguage('el');  // Set default to Greek
        }
      } catch (error) {
        console.error('Error fetching languages:', error);
      }
    };
    fetchLanguages();
  }, []);

  useEffect(() => {
    // Fetch lessons for selected language
    const fetchLessons = async () => {
      if (selectedLanguage) {
        try {
          setLoading(true);
          const response = await axios.get(`http://localhost:8000/lessons/${selectedLanguage}`);
          setLessons(response.data);
        } catch (error) {
          console.error('Error fetching lessons:', error);
        } finally {
          setLoading(false);
        }
      }
    };
    fetchLessons();
  }, [selectedLanguage]);

  const handleLanguageChange = (event) => {
    setSelectedLanguage(event.target.value);
  };

  const handleStartLesson = async (lesson) => {
    try {
      setLoading(true);
      const response = await axios.get(`http://localhost:8000/lessons/${selectedLanguage}/${lesson.id}`);
      console.log('Full lesson response:', response.data);
      
      let newLessonContent = null;

      if (lesson.title === "Greek Alphabet") {
        console.log('Alphabet lesson content:', response.data.content);
        newLessonContent = {
          ...response.data,
          lesson_type: "alphabet"
        };
      } else if (lesson.title === "Spaced Repetition Practice") {
        newLessonContent = {
          ...response.data,
          lesson_type: "spaced_repetition"
        };
      } else if (lesson.title === "Mnemonic Devices for Greek") {
        console.log('Mnemonic lesson data:', response.data);
        console.log('Mnemonic lesson content:', response.data.content);
        newLessonContent = {
          ...response.data,
          lesson_type: "mnemonics"
        };
      } else if (lesson.title === "100 Most Popular Greek Words") {
        newLessonContent = response.data;
      } else if (lesson.title === "Basic Greetings and Farewells") {
        newLessonContent = {
          ...response.data,
          words: response.data.content.words || [],
          lesson_type: "greetings"
        };
      } else if (lesson.title === "Contextual Learning") {
        newLessonContent = {
          ...response.data,
          words: response.data.content.words || [],
          lesson_type: "contextual"
        };
      } else if (lesson.title === "Visual Association Learning") {
        console.log('Visual lesson data:', response.data);
        console.log('Visual lesson content:', response.data.content);
        console.log('Visual lesson words:', response.data.content.words);
        // Log the structure of the first word to debug
        console.log('Sample word structure:', response.data.content.words[0]);
        
        newLessonContent = {
          ...response.data,
          lesson_type: "visual",
          content: response.data.content
        };
      } else {
        newLessonContent = {
          ...response.data,
          words: response.data.content.words || response.data.content.practice_words || [],
          lesson_type: response.data.lesson_type
        };
      }

      // Only update state if the content has changed
      if (JSON.stringify(newLessonContent) !== JSON.stringify(lessonContent)) {
        setLessonContent(newLessonContent);
      }
    } catch (error) {
      console.error('Error fetching lesson:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseLesson = () => {
    setLessonContent(null);
  };

  const getLessonTypeIcon = (lessonType) => {
    const icons = {
      'alphabet': '🔤',
      'greetings': '👋',
      'spaced_repetition': '🔄',
      'mnemonics': '🧠',
      'contextual': '💭',
      'visual': '👁️'
    };
    return icons[lessonType] || '📚';
  };

  const getLessonImage = (category) => {
    const images = {
      'Fundamentals': 'https://via.placeholder.com/400x200/3f51b5/ffffff?text=Fundamentals',
      'Conversation': 'https://via.placeholder.com/400x200/009688/ffffff?text=Conversation',
      'Grammar': 'https://via.placeholder.com/400x200/ff5722/ffffff?text=Grammar',
      'Vocabulary': 'https://via.placeholder.com/400x200/4caf50/ffffff?text=Vocabulary',
      'Memory Techniques': 'https://via.placeholder.com/400x200/9c27b0/ffffff?text=Memory+Techniques'
    };
    return images[category] || 'https://via.placeholder.com/400x200/9c27b0/ffffff?text=Language+Learning';
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          <SchoolIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
          Available Lessons
        </Typography>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel id="language-select-label">
            <LanguageIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
            Select Language
          </InputLabel>
          <Select
            labelId="language-select-label"
            value={selectedLanguage}
            onChange={handleLanguageChange}
            label="Select Language"
          >
            {languages.map((language) => (
              <MenuItem key={language.code} value={language.code}>
                {language.flag} {language.name} ({language.native_name})
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {loading ? (
        <Box sx={{ width: '100%', mt: 4 }}>
          <LinearProgress />
        </Box>
      ) : (
        <Grid container spacing={3}>
          {lessons.map((lesson) => (
            <Grid item xs={12} md={6} key={lesson.id}>
              <Card>
                <CardMedia
                  component="img"
                  height="200"
                  image={getLessonImage(lesson.category)}
                  alt={lesson.title}
                />
                <CardContent>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Typography variant="h5" component="span">
                      {getLessonTypeIcon(lesson.lesson_type)}
                    </Typography>
                    <Typography variant="h5" component="span" ml={2}>
                      {lesson.title}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {lesson.description}
                  </Typography>
                  <Box display="flex" alignItems="center" mb={2}>
                    <Chip
                      label={`Level ${lesson.level}`}
                      color="primary"
                      size="small"
                      sx={{ mr: 1 }}
                    />
                    <Chip
                      label={lesson.category}
                      color="secondary"
                      size="small"
                    />
                  </Box>
                  <Button
                    variant="contained"
                    color="primary"
                    startIcon={<PlayArrowIcon />}
                    onClick={() => handleStartLesson(lesson)}
                    fullWidth
                  >
                    Start Lesson
                  </Button>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog
        open={lessonContent !== null}
        onClose={handleCloseLesson}
        maxWidth="lg"
        fullWidth
      >
        {lessonContent && (
          <>
            <DialogTitle>
              {getLessonTypeIcon(lessonContent.lesson_type)} {lessonContent.title}
            </DialogTitle>
            <DialogContent>
              {loading ? (
                <LinearProgress />
              ) : (
                <Box>
                  <Typography variant="body1" gutterBottom>
                    {lessonContent.content.description}
                  </Typography>

                  {lessonContent.lesson_type === "alphabet" && (
                    <AlphabetLesson content={lessonContent.content} />
                  )}

                  {lessonContent.lesson_type === "spaced_repetition" && (
                    <SpacedRepetitionLesson content={lessonContent.content} />
                  )}

                  {lessonContent.lesson_type === "mnemonics" && (
                    <MnemonicsLesson lesson={lessonContent} />
                  )}

                  {lessonContent.lesson_type === "visual" && (
                    <>
                      {/* Visualization Tips */}
                      {lessonContent.content.visualization_tips && (
                        <Box sx={{ 
                          bgcolor: 'rgba(33, 150, 243, 0.1)', 
                          p: 2, 
                          borderRadius: 2,
                          border: '1px solid rgba(33, 150, 243, 0.3)',
                          mb: 3
                        }}>
                          <Typography variant="h6" gutterBottom>
                            <LightbulbIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
                            Visualization Tips
                          </Typography>
                          <List>
                            {lessonContent.content.visualization_tips.map((tip, index) => (
                              <ListItem key={index}>
                                <ListItemIcon>
                                  <CircleIcon sx={{ fontSize: 8 }} />
                                </ListItemIcon>
                                <ListItemText primary={tip} />
                              </ListItem>
                            ))}
                          </List>
                        </Box>
                      )}

                      {/* Visual Word Grid */}
                      <VisualWordGrid 
                        words={lessonContent.content.words || []} 
                        visualizationTips={lessonContent.content.visualization_tips || []}
                      />
                    </>
                  )}

                  {(lessonContent.lesson_type === "greetings" || 
                    lessonContent.lesson_type === "contextual") && (
                    <>
                      <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                        {lessonContent.lesson_type === "greetings" ? 'Basic Greetings and Farewells' : 'Contextual Learning Words'}
                      </Typography>
                      <Grid container spacing={2}>
                        {lessonContent.words.map((word, index) => (
                          <Grid item xs={12} sm={6} md={4} key={index}>
                            <Card sx={{ height: '100%' }}>
                              <CardContent>
                                <Typography variant="h5" gutterBottom>
                                  {word.word}
                                </Typography>
                                <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                                  {word.transliteration}
                                </Typography>
                                <Typography variant="h6" gutterBottom>
                                  {word.translation}
                                </Typography>
                                <Box sx={{ 
                                  bgcolor: 'rgba(156, 39, 176, 0.1)', 
                                  p: 2, 
                                  borderRadius: 1,
                                  mt: 2
                                }}>
                                  <Typography variant="body2">
                                    {word.context}
                                  </Typography>
                                </Box>
                              </CardContent>
                            </Card>
                          </Grid>
                        ))}
                      </Grid>
                    </>
                  )}

                  {/* Display lesson content */}
                  <Box sx={{ mt: 3 }}>
                    {/* Introduction if available */}
                    {lessonContent.introduction && (
                      <>
                        <Typography variant="h6" gutterBottom>
                          Introduction
                        </Typography>
                        <Typography paragraph>
                          {lessonContent.introduction}
                        </Typography>
                      </>
                    )}

                    {/* Description if available */}
                    {lessonContent.description && (
                      <>
                        <Typography variant="h6" gutterBottom>
                          Description
                        </Typography>
                        <Typography paragraph>
                          {lessonContent.description}
                        </Typography>
                      </>
                    )}

                    {/* Benefits if available */}
                    {lessonContent.benefits && (
                      <>
                        <Typography variant="h6" gutterBottom>
                          Benefits
                        </Typography>
                        <Typography paragraph>
                          {lessonContent.benefits}
                        </Typography>
                      </>
                    )}

                    {/* Example if available */}
                    {lessonContent.example && (
                      <>
                        <Typography variant="h6" gutterBottom>
                          Example
                        </Typography>
                        <Typography paragraph>
                          {lessonContent.example}
                        </Typography>
                      </>
                    )}

                    {/* Activities if available */}
                    {lessonContent.activities && lessonContent.activities.length > 0 && (
                      <>
                        <Typography variant="h6" gutterBottom>
                          Activities
                        </Typography>
                        <List>
                          {lessonContent.activities.map((activity, index) => (
                            <ListItem key={index}>
                              <ListItemIcon>
                                <CircleIcon sx={{ fontSize: 8 }} />
                              </ListItemIcon>
                              <ListItemText primary={activity} />
                            </ListItem>
                          ))}
                        </List>
                      </>
                    )}

                    {/* Popular Words List */}
                    {lessonContent?.title === "100 Most Popular Greek Words" && lessonContent?.content?.practice_words && (
                      <>
                        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                          Most Common Greek Words
                        </Typography>
                        <Grid container spacing={2}>
                          {lessonContent.content.practice_words.map((word, index) => (
                            <Grid item xs={12} sm={6} md={4} key={index}>
                              <Card sx={{ height: '100%' }}>
                                <CardContent>
                                  <Typography variant="h6" gutterBottom>
                                    {word.word}
                                  </Typography>
                                  <Typography variant="body1" color="text.secondary" gutterBottom>
                                    {word.transliteration}
                                  </Typography>
                                  <Typography variant="body1">
                                    {word.translation}
                                  </Typography>
                                  <Typography variant="caption" color="text.secondary">
                                    Word #{index + 1}
                                  </Typography>
                                </CardContent>
                              </Card>
                            </Grid>
                          ))}
                        </Grid>
                      </>
                    )}

                    {/* Words section - Spaced Repetition */}
                    {lessonContent?.lesson_type === 'spaced_repetition' && lessonContent?.words && lessonContent.words.length > 0 && (
                      <>
                        <Box sx={{ 
                          minHeight: '400px', 
                          display: 'flex', 
                          flexDirection: 'column', 
                          alignItems: 'center', 
                          justifyContent: 'center',
                          gap: 3,
                          my: 4
                        }}>
                          {/* Progress indicator */}
                          <Typography variant="subtitle1" color="text.secondary">
                            Word 1 of {lessonContent.words.length}
                          </Typography>
                          
                          {/* Flashcard */}
                          <Card 
                            sx={{ 
                              width: '100%', 
                              maxWidth: 400, 
                              minHeight: 200,
                              cursor: 'pointer',
                              transition: 'transform 0.3s ease',
                              '&:hover': {
                                transform: 'scale(1.02)'
                              }
                            }}
                          >
                            <CardContent sx={{ 
                              height: '100%', 
                              display: 'flex', 
                              flexDirection: 'column', 
                              alignItems: 'center', 
                              justifyContent: 'center',
                              p: 4
                            }}>
                              <Typography variant="h4" gutterBottom align="center">
                                {lessonContent.words[0].word}
                              </Typography>
                              <Typography variant="subtitle1" color="text.secondary" gutterBottom align="center">
                                {lessonContent.words[0].transliteration}
                              </Typography>
                              <Box sx={{ 
                                mt: 3, 
                                p: 2, 
                                bgcolor: 'primary.light', 
                                color: 'primary.contrastText',
                                borderRadius: 2,
                                width: '100%'
                              }}>
                                <Typography variant="h5" align="center">
                                  {lessonContent.words[0].translation}
                                </Typography>
                              </Box>
                            </CardContent>
                          </Card>

                          {/* Navigation buttons */}
                          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                            <Button
                              variant="outlined"
                              disabled
                              startIcon={<NavigateBeforeIcon />}
                            >
                              Previous
                            </Button>
                            <Button
                              variant="contained"
                              disabled
                              endIcon={<NavigateNextIcon />}
                            >
                              Next
                            </Button>
                          </Box>
                        </Box>
                      </>
                    )}

                    {/* Words section - Other lesson types */}
                    {lessonContent?.lesson_type !== 'spaced_repetition' && lessonContent?.content?.practice_words && lessonContent.content.practice_words.length > 0 && (
                      <>
                        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                          {lessonContent.lesson_type === 'mnemonics' ? 'Mnemonic Devices' : 'Words to Learn'} ({lessonContent.content.practice_words.length} words)
                        </Typography>
                        <Grid container spacing={2}>
                          {lessonContent.content.practice_words.map((word, index) => (
                            <Grid item xs={12} key={index}>
                              <Card sx={{ mb: 2 }}>
                                <CardContent>
                                  <Grid container spacing={2} alignItems="center">
                                    <Grid item xs={12} md={4}>
                                      <Typography variant="h5" gutterBottom>
                                        {word.word}
                                      </Typography>
                                      <Typography variant="subtitle1" color="text.secondary">
                                        {word.transliteration}
                                      </Typography>
                                      <Typography variant="h6">
                                        {word.translation}
                                      </Typography>
                                    </Grid>
                                    <Grid item xs={12} md={8}>
                                      {lessonContent.lesson_type === 'mnemonics' && word.mnemonic && (
                                        <Box sx={{ 
                                          bgcolor: 'rgba(156, 39, 176, 0.1)', 
                                          p: 2, 
                                          borderRadius: 2,
                                          border: '1px solid rgba(156, 39, 176, 0.3)',
                                          mt: { xs: 2, md: 0 }
                                        }}>
                                          <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                                            <strong>Remember it:</strong> {word.mnemonic}
                                          </Typography>
                                        </Box>
                                      )}
                                      {word.context && (
                                        <Box sx={{ 
                                          bgcolor: 'rgba(156, 39, 176, 0.1)', 
                                          p: 2, 
                                          borderRadius: 2,
                                          border: '1px solid rgba(156, 39, 176, 0.3)',
                                          mt: { xs: 2, md: 0 }
                                        }}>
                                          <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                                            <strong>Usage Context:</strong> {word.context}
                                          </Typography>
                                        </Box>
                                      )}
                                      {word.visual && (
                                        <Box sx={{ 
                                          bgcolor: 'rgba(156, 39, 176, 0.1)', 
                                          p: 2, 
                                          borderRadius: 2,
                                          border: '1px solid rgba(156, 39, 176, 0.3)',
                                          mt: { xs: 2, md: 0 }
                                        }}>
                                          <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                                            <strong>Visualize it:</strong> {word.visual}
                                          </Typography>
                                        </Box>
                                      )}
                                    </Grid>
                                  </Grid>
                                </CardContent>
                              </Card>
                            </Grid>
                          ))}
                        </Grid>
                      </>
                    )}

                    {/* Contextual Learning */}
                    {lessonContent?.lesson_type === "contextual" && lessonContent?.content?.words && (
                      <>
                        <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
                          Contextual Learning Words
                        </Typography>
                        <Grid container spacing={2}>
                          {lessonContent.content.words.map((word, index) => (
                            <Grid item xs={12} sm={6} md={4} key={index}>
                              <Card sx={{ height: '100%' }}>
                                <CardContent>
                                  <Typography variant="h5" gutterBottom>
                                    {word.word}
                                  </Typography>
                                  <Typography variant="subtitle1" color="text.secondary" gutterBottom>
                                    {word.transliteration}
                                  </Typography>
                                  <Typography variant="h6" gutterBottom>
                                    {word.translation}
                                  </Typography>
                                  <Box sx={{ 
                                    bgcolor: 'rgba(156, 39, 176, 0.1)', 
                                    p: 2, 
                                    borderRadius: 1,
                                    mt: 2
                                  }}>
                                    <Typography variant="body2">
                                      {word.context}
                                    </Typography>
                                  </Box>
                                </CardContent>
                              </Card>
                            </Grid>
                          ))}
                        </Grid>
                      </>
                    )}

                    {/* Example Situations if available */}
                    {lessonContent.example_situations && lessonContent.example_situations.length > 0 && (
                      <>
                        <Typography variant="h6" sx={{ mt: 4 }} gutterBottom>
                          Example Situations
                        </Typography>
                        <List>
                          {lessonContent.example_situations.map((situation, index) => (
                            <ListItem key={index}>
                              <ListItemIcon>
                                <CircleIcon sx={{ fontSize: 8 }} />
                              </ListItemIcon>
                              <ListItemText primary={situation} />
                            </ListItem>
                          ))}
                        </List>
                      </>
                    )}
                  </Box>
                </Box>
              )}
            </DialogContent>
            <DialogActions>
              <Button onClick={handleCloseLesson} color="primary">
                Close
              </Button>
            </DialogActions>
          </>
        )}
      </Dialog>
    </Container>
  );
};

const VisualWordGrid = ({ words, visualizationTips }) => {
  const [expandedIndex, setExpandedIndex] = React.useState(-1);

  // Log the words to check for duplicates and structure
  React.useEffect(() => {
    console.log("VisualWordGrid words:", words);
    const uniqueWords = new Set(words.map(word => word.word));
    console.log("Unique words count:", uniqueWords.size);
    console.log("Total words count:", words.length);
  }, [words]);

  return (
    <Grid container spacing={2}>
      {words.map((word, index) => {
        const hasVisualization = word.visualization_text && word.visualization_text.length > 0;
        
        return (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card 
              sx={{ 
                height: '100%',
                cursor: hasVisualization ? 'pointer' : 'default',
                transition: 'transform 0.2s, box-shadow 0.2s',
                '&:hover': hasVisualization ? {
                  transform: 'translateY(-4px)',
                  boxShadow: 4,
                } : {}
              }}
              onClick={() => hasVisualization && setExpandedIndex(expandedIndex === index ? -1 : index)}
            >
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  {word.word}
                </Typography>
                <Typography variant="body1" color="text.secondary" gutterBottom>
                  {word.transliteration}
                </Typography>
                <Typography variant="body1" gutterBottom>
                  {word.translation}
                </Typography>
                
                {/* Visual Hint - Always visible */}
                {word.visual_hint && (
                  <Box sx={{ 
                    bgcolor: 'rgba(156, 39, 176, 0.1)', 
                    p: 2, 
                    borderRadius: 2,
                    border: '1px solid rgba(156, 39, 176, 0.3)',
                    mt: 2,
                    mb: 2
                  }}>
                    <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                      <strong>Quick Hint:</strong> {word.visual_hint}
                    </Typography>
                  </Box>
                )}
                
                {/* Detailed Visualization - Shown on click */}
                {hasVisualization && (
                  <Collapse in={expandedIndex === index}>
                    <Box sx={{ 
                      bgcolor: 'rgba(63, 81, 181, 0.1)', 
                      p: 2, 
                      borderRadius: 2,
                      border: '1px solid rgba(63, 81, 181, 0.3)',
                      mt: 2
                    }}>
                      <Typography variant="body1">
                        <strong>Visualization Exercise:</strong>
                      </Typography>
                      <Typography variant="body1" sx={{ mt: 1 }}>
                        {word.visualization_text}
                      </Typography>
                    </Box>
                  </Collapse>
                )}

                {/* Click indicator - Only show if there's visualization text */}
                {hasVisualization && (
                  <Box sx={{ 
                    display: 'flex', 
                    justifyContent: 'center', 
                    mt: 2,
                    color: 'text.secondary'
                  }}>
                    <Typography variant="caption">
                      {expandedIndex === index ? 'Click to hide visualization' : 'Click to show visualization'}
                    </Typography>
                  </Box>
                )}
              </CardContent>
            </Card>
          </Grid>
        );
      })}
      {visualizationTips && (
        <Grid item xs={12}>
          <Box sx={{ 
            bgcolor: 'rgba(33, 150, 243, 0.1)', 
            p: 2, 
            borderRadius: 2,
            border: '1px solid rgba(33, 150, 243, 0.3)',
            mb: 3
          }}>
            <Typography variant="h6" gutterBottom>
              <LightbulbIcon sx={{ mr: 1, verticalAlign: 'bottom' }} />
              Visualization Tips
            </Typography>
            <List>
              {visualizationTips.map((tip, index) => (
                <ListItem key={index}>
                  <ListItemIcon>
                    <CircleIcon sx={{ fontSize: 8 }} />
                  </ListItemIcon>
                  <ListItemText primary={tip} />
                </ListItem>
              ))}
            </List>
          </Box>
        </Grid>
      )}
    </Grid>
  );
};

export default Lessons;
