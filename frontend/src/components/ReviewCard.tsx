import type { Review } from "../types";
import StarRating from "./StarRating";

interface ReviewCardProps {
  review: Review;
  onDelete?: (id: number) => void;
  isOwnReview?: boolean;
}

export default function ReviewCard({ review, onDelete, isOwnReview }: ReviewCardProps) {
  const date = new Date(review.created_at).toLocaleDateString("en-IE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });

  return (
    <div className="border-b border-black/5 py-4 last:border-0">
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-primary/10 text-primary flex items-center justify-center text-sm font-medium">
            {review.user_email.charAt(0).toUpperCase()}
          </div>
          <div>
            <p className="text-sm font-medium">{review.user_email}</p>
            <p className="text-xs text-text-muted">{date}</p>
          </div>
        </div>
        {isOwnReview && onDelete && (
          <button
            onClick={() => onDelete(review.id)}
            className="text-xs text-error hover:text-error/80"
          >
            Delete
          </button>
        )}
      </div>
      <StarRating rating={review.rating} readonly size="sm" />
      <p className="font-medium mt-1">{review.title}</p>
      <p className="text-sm text-text-muted mt-1">{review.comment}</p>
    </div>
  );
}
