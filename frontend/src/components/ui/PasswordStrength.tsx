interface PasswordStrengthProps {
  password: string;
}

export default function PasswordStrength({ password }: PasswordStrengthProps) {
  const checks = [
    { label: "At least 8 characters", met: password.length >= 8 },
    { label: "One uppercase letter", met: /[A-Z]/.test(password) },
    { label: "One lowercase letter", met: /[a-z]/.test(password) },
    { label: "One number", met: /\d/.test(password) },
  ];

  const score = checks.filter((c) => c.met).length;

  if (!password) return null;

  return (
    <div className="space-y-2">
      <div className="flex gap-1">
        {[1, 2, 3, 4].map((i) => (
          <div
            key={i}
            className={`h-1 flex-1 rounded-full transition-colors ${
              i <= score
                ? score <= 1
                  ? "bg-error"
                  : score <= 2
                  ? "bg-warning"
                  : "bg-success"
                : "bg-black/10"
            }`}
          />
        ))}
      </div>
      <ul className="space-y-1">
        {checks.map((check) => (
          <li
            key={check.label}
            className={`text-xs ${
              check.met ? "text-success" : "text-text-muted"
            }`}
          >
            {check.met ? "✓" : "○"} {check.label}
          </li>
        ))}
      </ul>
    </div>
  );
}
