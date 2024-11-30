import React from 'react';
import {
  Container,
  Grid,
  Paper,
  Typography,
  Box,
  LinearProgress,
  Card,
  CardContent,
  Button,
} from '@mui/material';

const Dashboard = () => {
  // This would normally come from your backend
  const mockData = {
    streak: 7,
    todayProgress: 65,
    totalPoints: 1250,
    nextLesson: 'Basic Greetings',
    recentAchievements: [
      'First Lesson Completed',
      '7-Day Streak',
      'Vocabulary Master',
    ],
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Welcome Section */}
        <Grid item xs={12}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h4" gutterBottom>
              Welcome back!
            </Typography>
            <Typography variant="subtitle1">
              You're on a {mockData.streak}-day streak! Keep it up!
            </Typography>
          </Paper>
        </Grid>

        {/* Daily Progress */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Today's Progress
            </Typography>
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              <Box sx={{ width: '100%', mr: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={mockData.todayProgress}
                  sx={{ height: 10, borderRadius: 5 }}
                />
              </Box>
              <Box sx={{ minWidth: 35 }}>
                <Typography variant="body2" color="text.secondary">
                  {mockData.todayProgress}%
                </Typography>
              </Box>
            </Box>
          </Paper>
        </Grid>

        {/* Points Display */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column' }}>
            <Typography variant="h6" gutterBottom>
              Total Points
            </Typography>
            <Typography variant="h3" component="div">
              {mockData.totalPoints}
            </Typography>
          </Paper>
        </Grid>

        {/* Next Lesson */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Next Lesson
              </Typography>
              <Typography variant="body1" paragraph>
                {mockData.nextLesson}
              </Typography>
              <Button variant="contained" color="primary">
                Start Lesson
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* Recent Achievements */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Achievements
              </Typography>
              {mockData.recentAchievements.map((achievement, index) => (
                <Typography key={index} variant="body1" paragraph>
                  🏆 {achievement}
                </Typography>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard;
