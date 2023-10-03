// Import required modules
const express = require('express');
const mongoose = require('mongoose');

// Initialize Express app
const app = express();
const port = 3001;

// Enable JSON body parsing middleware for handling POST requests
app.use(express.json());

// MongoDB Connection
mongoose.connect('mongodb://localhost:27017/monbud', {
  useNewUrlParser: true,
  useUnifiedTopology: true
})
.then(() => console.log('Connected to MongoDB'))
.catch(err => console.log('Failed to connect to MongoDB', err));

// Example API endpoint (You'll replace this with your own endpoints)
app.get('/', (req, res) => {
  res.send('Hello, MonBud!');
});

// Starting the server
app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});