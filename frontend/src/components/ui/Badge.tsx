interface BadgeProps {
  status: string;
}

const statusStyles: Record<string, string> = {
  paid: "bg-success/10 text-success",
  complete: "bg-success/10 text-success",
  pending: "bg-warning/10 text-warning",
  failed: "bg-error/10 text-error",
  unpaid: "bg-error/10 text-error",
};

export default function Badge({ status }: BadgeProps) {
  const style = statusStyles[status.toLowerCase()] || "bg-black/5 text-text-muted";

  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${style}`}
    >
      {status}
    </span>
  );
}
