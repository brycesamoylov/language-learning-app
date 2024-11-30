import React, { useState, useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Container,
  Paper,
  Typography,
  TextField,
  Button,
  Box,
  Grid,
  CircularProgress,
} from '@mui/material';
import { updateProfile } from '../store/slices/profileSlice';

const Profile = () => {
  const dispatch = useDispatch();
  const { user, loading, error } = useSelector((state) => state.profile);
  const [formData, setFormData] = useState({
    nativeLanguage: '',
    learningGoals: '',
    dailyGoalMinutes: 30,
  });

  useEffect(() => {
    if (user) {
      setFormData({
        nativeLanguage: user.nativeLanguage || '',
        learningGoals: user.learningGoals || '',
        dailyGoalMinutes: user.dailyGoalMinutes || 30,
      });
    }
  }, [user]);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    dispatch(updateProfile(formData));
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="md">
      <Paper elevation={3} sx={{ p: 4, mt: 4 }}>
        <Typography variant="h4" gutterBottom>
          Profile Settings
        </Typography>
        {error && (
          <Typography color="error" sx={{ mb: 2 }}>
            {error}
          </Typography>
        )}
        <form onSubmit={handleSubmit}>
          <Grid container spacing={3}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Native Language"
                name="nativeLanguage"
                value={formData.nativeLanguage}
                onChange={handleChange}
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                multiline
                rows={4}
                label="Learning Goals"
                name="learningGoals"
                value={formData.learningGoals}
                onChange={handleChange}
                helperText="What do you want to achieve with language learning?"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                type="number"
                label="Daily Goal (minutes)"
                name="dailyGoalMinutes"
                value={formData.dailyGoalMinutes}
                onChange={handleChange}
                inputProps={{ min: 5, max: 240 }}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
                disabled={loading}
              >
                Save Changes
              </Button>
            </Grid>
          </Grid>
        </form>
      </Paper>
    </Container>
  );
};

export default Profile;
