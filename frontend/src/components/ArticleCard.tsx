import React from 'react';
import { NewsArticle } from '../types';
import { ExternalLink, Heart, Bookmark } from 'lucide-react';
import { clsx } from 'clsx';

interface ArticleCardProps {
  article: NewsArticle;
  onFavorite?: (articleId: string) => void;
  onReadMore?: (article: NewsArticle) => void;
  isFavorited?: boolean;
  className?: string;
}

const ArticleCard: React.FC<ArticleCardProps> = ({
  article,
  onFavorite,
  onReadMore,
  isFavorited = false,
  className,
}) => {
  const handleReadMore = () => {
    if (onReadMore) {
      onReadMore(article);
    } else {
      window.open(article.link, '_blank', 'noopener,noreferrer');
    }
  };

  const handleFavorite = () => {
    if (onFavorite) {
      onFavorite(article.link); // Using link as article ID
    }
  };

  const formatScore = (score: number) => {
    return Math.round(score * 100);
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return '';
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      });
    } catch {
      return '';
    }
  };

  return (
    <div className={clsx('card group', className)}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <span className="badge badge-primary">
              {formatScore(article.score)}% match
            </span>
            <span className="text-sm text-gray-500">
              {article.source}
            </span>
          </div>
          
          <h3 className="text-lg font-semibold text-gray-900 mb-3 line-clamp-2 group-hover:text-primary-600 transition-colors">
            {article.title}
          </h3>
        </div>
        
        <div className="flex items-center gap-2 ml-4">
          {onFavorite && (
            <button
              onClick={handleFavorite}
              className={clsx(
                'p-2 rounded-lg transition-colors',
                isFavorited
                  ? 'text-red-500 hover:text-red-600'
                  : 'text-gray-400 hover:text-red-500'
              )}
              title={isFavorited ? 'Remove from favorites' : 'Add to favorites'}
            >
              <Heart
                size={20}
                className={clsx(
                  'transition-all',
                  isFavorited && 'fill-current'
                )}
              />
            </button>
          )}
        </div>
      </div>

      <div className="mb-4">
        <p className="text-gray-600 text-sm leading-relaxed line-clamp-3">
          {article.summary}
        </p>
      </div>

      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4 text-sm text-gray-500">
          {article.published_at && (
            <span>{formatDate(article.published_at)}</span>
          )}
        </div>
        
        <button
          onClick={handleReadMore}
          className="btn-secondary flex items-center gap-2 text-sm"
        >
          <span>Read More</span>
          <ExternalLink size={16} />
        </button>
      </div>
    </div>
  );
};

export default ArticleCard; 