import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TestLessons = () => {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lessons, setLessons] = useState([]);

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        setLoading(true);
        setError(null);
        
        const response = await axios.get('http://localhost:8000/lessons/el', {
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
          },
          withCredentials: false
        });
        
        console.log('Lessons data:', response.data);
        setLessons(response.data);
      } catch (error) {
        console.error('Error fetching lessons:', error);
        setError(error.message || 'Failed to fetch lessons');
      } finally {
        setLoading(false);
      }
    };
    
    fetchLessons();
  }, []);

  if (loading) {
    return <div>Loading lessons...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div>
      <h1>Test Lessons</h1>
      {lessons.length > 0 ? (
        <ul>
          {lessons.map(lesson => (
            <li key={lesson.id}>
              {lesson.title} - Level: {lesson.level}
            </li>
          ))}
        </ul>
      ) : (
        <p>No lessons found.</p>
      )}
    </div>
  );
};

export default TestLessons;
