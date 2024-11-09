import React, { useState, useEffect } from 'react';
import { Star } from 'lucide-react';

const BookRating = ({ isbn, user, onRatingUpdate }) => {
  const [userRating, setUserRating] = useState(0);
  const [hoveredRating, setHoveredRating] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchUserRating = async () => {
      if (!user) return;
      
      try {
        const response = await fetch(`/api/ratings/${isbn}`);
        if (response.ok) {
          const data = await response.json();
          setUserRating(data.rating || 0);
        }
      } catch (err) {
        console.error('Error fetching user rating:', err);
      }
    };

    fetchUserRating();
  }, [isbn, user]);

  const handleRating = async (rating) => {
    if (!user) return;
    
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`/api/ratings/${isbn}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ rating }),
      });

      if (response.ok) {
        setUserRating(rating);
        if (onRatingUpdate) onRatingUpdate();
      } else {
        const data = await response.json();
        setError(data.error);
      }
    } catch (err) {
      setError('Failed to submit rating');
    } finally {
      setLoading(false);
    }
  };

  if (!user) {
    return (
      <div className="text-sm text-gray-500 mt-2">
        Please log in to rate this book
      </div>
    );
  }

  return (
    <div className="mt-4">
      <div className="flex items-center gap-1">
        {[1, 2, 3, 4, 5].map((rating) => (
          <button
            key={rating}
            disabled={loading}
            onClick={() => handleRating(rating)}
            onMouseEnter={() => setHoveredRating(rating)}
            onMouseLeave={() => setHoveredRating(0)}
            className="p-1 hover:scale-110 transition-transform"
          >
            <Star
              size={24}
              className={`transition-colors ${
                rating <= (hoveredRating || userRating)
                  ? 'fill-yellow-400 text-yellow-400'
                  : 'text-gray-300'
              }`}
            />
          </button>
        ))}
      </div>
      
      {loading && (
        <div className="text-sm text-gray-500 mt-2">
          Submitting rating...
        </div>
      )}
      
      {error && (
        <div className="text-sm text-red-500 mt-2">
          {error}
        </div>
      )}
      
      {userRating > 0 && !loading && !error && (
        <div className="text-sm text-gray-600 mt-2">
          Your rating: {userRating} star{userRating !== 1 ? 's' : ''}
        </div>
      )}
    </div>
  );
};

export default BookRating;