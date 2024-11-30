import React, { useState } from 'react';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardHeader,
  Typography,
  Button,
  TextField,
  Avatar,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  Box,
  Tab,
  Tabs,
  Paper,
  IconButton,
} from '@mui/material';
import {
  Send as SendIcon,
  Favorite as FavoriteIcon,
  Comment as CommentIcon,
  Share as ShareIcon,
  VideoCall as VideoCallIcon,
} from '@mui/icons-material';

const mockPosts = [
  {
    id: 1,
    user: {
      name: 'Sarah Johnson',
      avatar: 'https://source.unsplash.com/random/100x100/?portrait,woman',
      language: 'French',
      level: 'Intermediate',
    },
    content: 'Just completed my first French conversation with a native speaker! 🎉',
    likes: 15,
    comments: 3,
    timestamp: '2 hours ago',
  },
  {
    id: 2,
    user: {
      name: 'Michael Chen',
      avatar: 'https://source.unsplash.com/random/100x100/?portrait,man',
      language: 'Spanish',
      level: 'Advanced',
    },
    content: 'Looking for a language exchange partner for daily practice. Anyone interested?',
    likes: 8,
    comments: 5,
    timestamp: '4 hours ago',
  },
];

const mockPartners = [
  {
    id: 1,
    name: 'Emma Laurent',
    avatar: 'https://source.unsplash.com/random/100x100/?portrait,woman',
    nativeLanguage: 'French',
    learningLanguage: 'English',
    online: true,
  },
  {
    id: 2,
    name: 'Carlos Rodriguez',
    avatar: 'https://source.unsplash.com/random/100x100/?portrait,man',
    nativeLanguage: 'Spanish',
    learningLanguage: 'French',
    online: false,
  },
];

const Community = () => {
  const [tabValue, setTabValue] = useState(0);
  const [newPost, setNewPost] = useState('');

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handlePostSubmit = () => {
    // Handle post submission
    setNewPost('');
  };

  const PostCard = ({ post }) => (
    <Card sx={{ mb: 2 }}>
      <CardHeader
        avatar={
          <Avatar src={post.user.avatar} />
        }
        title={post.user.name}
        subheader={`${post.user.language} • ${post.user.level} • ${post.timestamp}`}
      />
      <CardContent>
        <Typography variant="body1" paragraph>
          {post.content}
        </Typography>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <IconButton>
              <FavoriteIcon />
            </IconButton>
            {post.likes}
            <IconButton>
              <CommentIcon />
            </IconButton>
            {post.comments}
            <IconButton>
              <ShareIcon />
            </IconButton>
          </Box>
          <Button
            variant="outlined"
            size="small"
            startIcon={<CommentIcon />}
          >
            Comment
          </Button>
        </Box>
      </CardContent>
    </Card>
  );

  const PartnerCard = ({ partner }) => (
    <ListItem>
      <ListItemAvatar>
        <Avatar src={partner.avatar} />
      </ListItemAvatar>
      <ListItemText
        primary={partner.name}
        secondary={`${partner.nativeLanguage} → ${partner.learningLanguage}`}
      />
      <Box>
        <Button
          variant="contained"
          startIcon={<VideoCallIcon />}
          color="primary"
          size="small"
          sx={{ mr: 1 }}
        >
          Call
        </Button>
        <Button
          variant="outlined"
          size="small"
        >
          Message
        </Button>
      </Box>
    </ListItem>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Paper sx={{ mb: 3 }}>
        <Tabs
          value={tabValue}
          onChange={handleTabChange}
          centered
          indicatorColor="primary"
          textColor="primary"
        >
          <Tab label="Community Feed" />
          <Tab label="Language Partners" />
        </Tabs>
      </Paper>

      {tabValue === 0 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            {/* New Post Input */}
            <Card sx={{ mb: 3 }}>
              <CardContent>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  placeholder="Share your language learning journey..."
                  value={newPost}
                  onChange={(e) => setNewPost(e.target.value)}
                  variant="outlined"
                  sx={{ mb: 2 }}
                />
                <Box display="flex" justifyContent="flex-end">
                  <Button
                    variant="contained"
                    startIcon={<SendIcon />}
                    onClick={handlePostSubmit}
                  >
                    Post
                  </Button>
                </Box>
              </CardContent>
            </Card>

            {/* Posts Feed */}
            {mockPosts.map((post) => (
              <PostCard key={post.id} post={post} />
            ))}
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader title="Community Stats" />
              <CardContent>
                <Typography variant="body1" paragraph>
                  👥 Active Members: 1,234
                </Typography>
                <Typography variant="body1" paragraph>
                  🌍 Languages: 15
                </Typography>
                <Typography variant="body1" paragraph>
                  💬 Daily Conversations: 89
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {tabValue === 1 && (
        <Grid container spacing={3}>
          <Grid item xs={12} md={8}>
            <Card>
              <CardHeader title="Available Language Partners" />
              <List>
                {mockPartners.map((partner) => (
                  <React.Fragment key={partner.id}>
                    <PartnerCard partner={partner} />
                    <Divider component="li" />
                  </React.Fragment>
                ))}
              </List>
            </Card>
          </Grid>

          <Grid item xs={12} md={4}>
            <Card>
              <CardHeader title="Find Partners" />
              <CardContent>
                <TextField
                  fullWidth
                  label="Native Language"
                  select
                  SelectProps={{
                    native: true,
                  }}
                  sx={{ mb: 2 }}
                >
                  <option value="">Select language</option>
                  <option value="french">French</option>
                  <option value="spanish">Spanish</option>
                  <option value="german">German</option>
                </TextField>

                <TextField
                  fullWidth
                  label="Learning Language"
                  select
                  SelectProps={{
                    native: true,
                  }}
                  sx={{ mb: 2 }}
                >
                  <option value="">Select language</option>
                  <option value="english">English</option>
                  <option value="french">French</option>
                  <option value="spanish">Spanish</option>
                </TextField>

                <Button
                  variant="contained"
                  fullWidth
                >
                  Search Partners
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}
    </Container>
  );
};

export default Community;
