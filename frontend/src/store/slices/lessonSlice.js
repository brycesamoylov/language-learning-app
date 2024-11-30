import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const fetchLessons = createAsyncThunk(
  'lessons/fetchLessons',
  async (_, { rejectWithValue }) => {
    try {
      const response = await axios.get(`${API_URL}/lessons`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const startLesson = createAsyncThunk(
  'lessons/startLesson',
  async (lessonId, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/lessons/${lessonId}/start`);
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

export const completeLesson = createAsyncThunk(
  'lessons/completeLesson',
  async ({ lessonId, score }, { rejectWithValue }) => {
    try {
      const response = await axios.post(`${API_URL}/lessons/${lessonId}/complete`, { score });
      return response.data;
    } catch (error) {
      return rejectWithValue(error.response.data);
    }
  }
);

const lessonSlice = createSlice({
  name: 'lessons',
  initialState: {
    lessons: [],
    currentLesson: null,
    loading: false,
    error: null,
  },
  reducers: {
    setCurrentLesson: (state, action) => {
      state.currentLesson = action.payload;
    },
    clearError: (state) => {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchLessons.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchLessons.fulfilled, (state, action) => {
        state.loading = false;
        state.lessons = action.payload;
      })
      .addCase(fetchLessons.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.message || 'Failed to fetch lessons';
      })
      .addCase(startLesson.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(startLesson.fulfilled, (state, action) => {
        state.loading = false;
        state.currentLesson = action.payload;
      })
      .addCase(startLesson.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.message || 'Failed to start lesson';
      })
      .addCase(completeLesson.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(completeLesson.fulfilled, (state, action) => {
        state.loading = false;
        state.currentLesson = null;
        state.lessons = state.lessons.map((lesson) =>
          lesson.id === action.payload.id ? action.payload : lesson
        );
      })
      .addCase(completeLesson.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload?.message || 'Failed to complete lesson';
      });
  },
});

export const { setCurrentLesson, clearError } = lessonSlice.actions;
export default lessonSlice.reducer;
