import axios from 'axios';
import { NewsArticle, UserProfile, SummarizationRequest, SummarizationResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`API Request: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    console.error('API Request Error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    console.log(`API Response: ${response.status} ${response.config.url}`);
    return response;
  },
  (error) => {
    console.error('API Response Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const newsApi = {
  /**
   * Get personalized news articles
   */
  getNews: async (
    userId: string,
    preferredTopics: string,
    maxArticles: number = 10
  ): Promise<NewsArticle[]> => {
    try {
      const response = await api.get('/news', {
        params: {
          user_id: userId,
          preferred_topics: preferredTopics,
          max_articles: maxArticles,
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error fetching news:', error);
      throw error;
    }
  },

  /**
   * Summarize text using BART model
   */
  summarizeText: async (
    text: string,
    maxLength: number = 150
  ): Promise<SummarizationResponse> => {
    try {
      const response = await api.post('/summarize', {
        text,
        max_length: maxLength,
      });
      return response.data;
    } catch (error) {
      console.error('Error summarizing text:', error);
      throw error;
    }
  },

  /**
   * Get user profile
   */
  getUserProfile: async (userId: string): Promise<UserProfile> => {
    try {
      const response = await api.get(`/user/${userId}/profile`);
      return response.data;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      throw error;
    }
  },

  /**
   * Record user interaction
   */
  recordInteraction: async (
    userId: string,
    action: 'click' | 'favorite',
    articleId?: string
  ): Promise<void> => {
    try {
      await api.post(`/user/${userId}/interaction`, null, {
        params: {
          action,
          article_id: articleId,
        },
      });
    } catch (error) {
      console.error('Error recording interaction:', error);
      throw error;
    }
  },

  /**
   * Health check
   */
  healthCheck: async (): Promise<{ status: string; version: string }> => {
    try {
      const response = await api.get('/health');
      return response.data;
    } catch (error) {
      console.error('Error checking health:', error);
      throw error;
    }
  },
};

export default api; 