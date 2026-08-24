interface OrderTimelineProps {
  status: string;
  createdAt: string;
  statusUpdatedAt: string;
}

const steps = [
  { key: "pending", label: "Order Placed" },
  { key: "processing", label: "Processing" },
  { key: "shipped", label: "Shipped" },
  { key: "delivered", label: "Delivered" },
];

export default function OrderTimeline({
  status,
  createdAt,
  statusUpdatedAt,
}: OrderTimelineProps) {
  const currentIndex = steps.findIndex((s) => s.key === status);

  return (
    <div className="space-y-0">
      {steps.map((step, index) => {
        const isCompleted = index <= currentIndex;
        const isCurrent = index === currentIndex;

        return (
          <div key={step.key} className="flex gap-4">
            <div className="flex flex-col items-center">
              <div
                className={`h-8 w-8 rounded-full flex items-center justify-center text-sm font-medium ${
                  isCompleted
                    ? "bg-primary text-white"
                    : "bg-black/10 text-text-muted"
                } ${isCurrent ? "ring-2 ring-primary/30" : ""}`}
              >
                {isCompleted ? "✓" : index + 1}
              </div>
              {index < steps.length - 1 && (
                <div
                  className={`w-0.5 h-8 ${
                    index < currentIndex ? "bg-primary" : "bg-black/10"
                  }`}
                />
              )}
            </div>
            <div className="pb-8">
              <p
                className={`font-medium ${
                  isCompleted ? "text-text" : "text-text-muted"
                }`}
              >
                {step.label}
              </p>
              {isCompleted && (
                <p className="text-xs text-text-muted">
                  {new Date(
                    index === 0 ? createdAt : statusUpdatedAt
                  ).toLocaleDateString("en-IE", {
                    month: "short",
                    day: "numeric",
                    hour: "2-digit",
                    minute: "2-digit",
                  })}
                </p>
              )}
            </div>
          </div>
        );
      })}
    </div>
  );
}
