import React, { useState } from 'react';
import { TopicOption } from '../types';
import { X, Plus } from 'lucide-react';
import { clsx } from 'clsx';

interface TopicSelectorProps {
  selectedTopics: string[];
  onTopicsChange: (topics: string[]) => void;
  className?: string;
}

const TopicSelector: React.FC<TopicSelectorProps> = ({
  selectedTopics,
  onTopicsChange,
  className,
}) => {
  const [customTopic, setCustomTopic] = useState('');

  const popularTopics: TopicOption[] = [
    { value: 'AI', label: 'AI', category: 'popular' },
    { value: 'technology', label: 'Technology', category: 'popular' },
    { value: 'politics', label: 'Politics', category: 'popular' },
    { value: 'sports', label: 'Sports', category: 'popular' },
    { value: 'health', label: 'Health', category: 'popular' },
    { value: 'science', label: 'Science', category: 'popular' },
    { value: 'business', label: 'Business', category: 'popular' },
    { value: 'entertainment', label: 'Entertainment', category: 'popular' },
  ];

  const trendingTopics: TopicOption[] = [
    { value: 'machine learning', label: 'Machine Learning', category: 'trending' },
    { value: 'climate change', label: 'Climate Change', category: 'trending' },
    { value: 'cryptocurrency', label: 'Cryptocurrency', category: 'trending' },
    { value: 'space exploration', label: 'Space Exploration', category: 'trending' },
    { value: 'renewable energy', label: 'Renewable Energy', category: 'trending' },
    { value: 'cybersecurity', label: 'Cybersecurity', category: 'trending' },
  ];

  const handleTopicToggle = (topic: string) => {
    const newTopics = selectedTopics.includes(topic)
      ? selectedTopics.filter(t => t !== topic)
      : [...selectedTopics, topic];
    onTopicsChange(newTopics);
  };

  const handleAddCustomTopic = () => {
    const trimmedTopic = customTopic.trim();
    if (trimmedTopic && !selectedTopics.includes(trimmedTopic)) {
      onTopicsChange([...selectedTopics, trimmedTopic]);
      setCustomTopic('');
    }
  };

  const handleRemoveTopic = (topic: string) => {
    onTopicsChange(selectedTopics.filter(t => t !== topic));
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddCustomTopic();
    }
  };

  return (
    <div className={clsx('space-y-6', className)}>
      {/* Selected Topics */}
      {selectedTopics.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-3">Selected Topics</h3>
          <div className="flex flex-wrap gap-2">
            {selectedTopics.map((topic) => (
              <span
                key={topic}
                className="badge badge-primary flex items-center gap-1"
              >
                {topic}
                <button
                  onClick={() => handleRemoveTopic(topic)}
                  className="ml-1 hover:text-red-600 transition-colors"
                >
                  <X size={12} />
                </button>
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Popular Topics */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">Popular Topics</h3>
        <div className="flex flex-wrap gap-2">
          {popularTopics.map((topic) => (
            <button
              key={topic.value}
              onClick={() => handleTopicToggle(topic.value)}
              className={clsx(
                'badge transition-colors',
                selectedTopics.includes(topic.value)
                  ? 'badge-primary'
                  : 'badge-secondary hover:bg-gray-200'
              )}
            >
              {topic.label}
            </button>
          ))}
        </div>
      </div>

      {/* Trending Topics */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">Trending Topics</h3>
        <div className="flex flex-wrap gap-2">
          {trendingTopics.map((topic) => (
            <button
              key={topic.value}
              onClick={() => handleTopicToggle(topic.value)}
              className={clsx(
                'badge transition-colors',
                selectedTopics.includes(topic.value)
                  ? 'badge-primary'
                  : 'badge-secondary hover:bg-gray-200'
              )}
            >
              {topic.label}
            </button>
          ))}
        </div>
      </div>

      {/* Custom Topic Input */}
      <div>
        <h3 className="text-sm font-medium text-gray-700 mb-3">Add Custom Topic</h3>
        <div className="flex gap-2">
          <input
            type="text"
            value={customTopic}
            onChange={(e) => setCustomTopic(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter a custom topic..."
            className="input-field flex-1"
          />
          <button
            onClick={handleAddCustomTopic}
            disabled={!customTopic.trim()}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Plus size={16} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default TopicSelector; 