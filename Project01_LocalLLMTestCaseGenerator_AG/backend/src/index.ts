import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();
const port = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok', message: 'Local LLM Test Case Generator Backend is running.' });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
