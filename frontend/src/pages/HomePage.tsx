import React, { useState, useEffect } from 'react';
import { NewsArticle } from '../types';
import { newsApi } from '../services/api';
import ArticleCard from '../components/ArticleCard';
import TopicSelector from '../components/TopicSelector';
import { RefreshCw, AlertCircle, Sparkles } from 'lucide-react';
import { clsx } from 'clsx';

const HomePage: React.FC = () => {
  const [articles, setArticles] = useState<NewsArticle[]>([]);
  const [selectedTopics, setSelectedTopics] = useState<string[]>(['AI', 'technology']);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [userId] = useState('user123'); // In a real app, this would come from auth
  const [favoritedArticles, setFavoritedArticles] = useState<Set<string>>(new Set());

  const fetchNews = async () => {
    if (selectedTopics.length === 0) {
      setError('Please select at least one topic');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const topicsString = selectedTopics.join(',');
      const newsData = await newsApi.getNews(userId, topicsString, 10);
      setArticles(newsData);
    } catch (err) {
      setError('Failed to fetch news. Please try again.');
      console.error('Error fetching news:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNews();
  }, [selectedTopics]);

  const handleFavorite = async (articleId: string) => {
    try {
      const isFavorited = favoritedArticles.has(articleId);
      
      if (isFavorited) {
        setFavoritedArticles(prev => {
          const newSet = new Set(prev);
          newSet.delete(articleId);
          return newSet;
        });
      } else {
        setFavoritedArticles(prev => new Set([...prev, articleId]));
      }

      await newsApi.recordInteraction(userId, 'favorite', articleId);
    } catch (err) {
      console.error('Error recording favorite:', err);
    }
  };

  const handleReadMore = async (article: NewsArticle) => {
    try {
      await newsApi.recordInteraction(userId, 'click', article.link);
      window.open(article.link, '_blank', 'noopener,noreferrer');
    } catch (err) {
      console.error('Error recording click:', err);
      // Still open the link even if recording fails
      window.open(article.link, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Sparkles className="h-8 w-8 text-primary-600" />
              <h1 className="ml-3 text-2xl font-bold text-gray-900">NewsGenie</h1>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={fetchNews}
                disabled={loading}
                className="btn-secondary flex items-center gap-2"
              >
                <RefreshCw
                  size={16}
                  className={clsx('transition-transform', loading && 'animate-spin')}
                />
                Refresh
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar - Topic Selection */}
          <div className="lg:col-span-1">
            <div className="card">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                Your Topics
              </h2>
              <TopicSelector
                selectedTopics={selectedTopics}
                onTopicsChange={setSelectedTopics}
              />
            </div>
          </div>

          {/* Main Content - News Feed */}
          <div className="lg:col-span-3">
            {/* Error Message */}
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <div className="flex items-center gap-2 text-red-800">
                  <AlertCircle size={20} />
                  <span>{error}</span>
                </div>
              </div>
            )}

            {/* Loading State */}
            {loading && (
              <div className="flex items-center justify-center py-12">
                <div className="flex items-center gap-3">
                  <RefreshCw className="animate-spin text-primary-600" size={24} />
                  <span className="text-gray-600">Loading your personalized news...</span>
                </div>
              </div>
            )}

            {/* News Articles */}
            {!loading && articles.length > 0 && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-xl font-semibold text-gray-900">
                    Your Personalized News
                  </h2>
                  <span className="text-sm text-gray-500">
                    {articles.length} articles found
                  </span>
                </div>
                
                <div className="grid gap-6">
                  {articles.map((article, index) => (
                    <ArticleCard
                      key={`${article.link}-${index}`}
                      article={article}
                      onFavorite={handleFavorite}
                      onReadMore={handleReadMore}
                      isFavorited={favoritedArticles.has(article.link)}
                      className="animate-fade-in"
                      style={{ animationDelay: `${index * 100}ms` }}
                    />
                  ))}
                </div>
              </div>
            )}

            {/* Empty State */}
            {!loading && articles.length === 0 && !error && (
              <div className="text-center py-12">
                <Sparkles className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  No articles found
                </h3>
                <p className="text-gray-500 mb-6">
                  Try selecting different topics or check back later for new content.
                </p>
                <button
                  onClick={fetchNews}
                  className="btn-primary"
                >
                  Refresh News
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage; 