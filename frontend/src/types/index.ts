export interface NewsArticle {
  title: string;
  summary: string;
  link: string;
  source: string;
  score: number;
  published_at?: string;
  content?: string;
}

export interface UserProfile {
  user_id: string;
  preferred_topics: string[];
  click_history_count: number;
  favorite_articles_count: number;
}

export interface SummarizationRequest {
  text: string;
  max_length: number;
}

export interface SummarizationResponse {
  summary: string;
  original_length: number;
  summary_length: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: boolean;
  message?: string;
}

export interface TopicOption {
  value: string;
  label: string;
  category: 'popular' | 'trending' | 'custom';
}

export interface UserPreferences {
  userId: string;
  topics: string[];
}

export interface ArticleInteraction {
  articleId: string;
  action: 'click' | 'favorite';
} 