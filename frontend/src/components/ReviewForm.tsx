import { useState, type FormEvent } from "react";
import { api } from "../services/api";
import StarRating from "./StarRating";
import Button from "./ui/Button";
import Input from "./ui/Input";

interface ReviewFormProps {
  productId: string;
  onReviewAdded: () => void;
}

export default function ReviewForm({ productId, onReviewAdded }: ReviewFormProps) {
  const [rating, setRating] = useState(0);
  const [title, setTitle] = useState("");
  const [comment, setComment] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");

    if (rating === 0) {
      setError("Please select a rating");
      return;
    }

    setIsLoading(true);

    try {
      await api.post("/api/reviews", {
        product_id: productId,
        rating,
        title,
        comment,
      });
      setRating(0);
      setTitle("");
      setComment("");
      onReviewAdded();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to submit review");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-surface rounded-xl p-6 shadow-sm space-y-4">
      <h3 className="text-lg font-semibold">Write a Review</h3>

      {error && (
        <div className="bg-error/10 text-error text-sm p-3 rounded-lg">
          {error}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium mb-2">Rating</label>
        <StarRating rating={rating} onRate={setRating} size="lg" />
      </div>

      <Input
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="Summarize your experience"
        required
      />

      <div className="space-y-1">
        <label className="block text-sm font-medium">Comment</label>
        <textarea
          value={comment}
          onChange={(e) => setComment(e.target.value)}
          placeholder="Tell others what you think about this product"
          rows={4}
          className="w-full rounded-lg border border-black/10 bg-surface px-4 py-2.5 text-sm placeholder:text-text-muted focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary"
          required
        />
      </div>

      <Button type="submit" isLoading={isLoading}>
        Submit Review
      </Button>
    </form>
  );
}
