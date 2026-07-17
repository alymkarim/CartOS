function App() {
  const path = window.location.pathname;

  if (path === "/success") {
    const params = new URLSearchParams(window.location.search);
    const sessionId = params.get("session_id");

    return (
      <main>
        <h1>Payment successful</h1>
        <p>Your Stripe test payment was completed.</p>
        {sessionId && <p>Session: {sessionId}</p>}
        <a href="/">Return to store</a>
      </main>
    );
  }

  if (path === "/cancel") {
    return (
      <main>
        <h1>Payment cancelled</h1>
        <p>No payment was completed.</p>
        <a href="/">Return to store</a>
      </main>
    );
  }

  return (
    <main>
      <h1>PayForge</h1>
      <p>Your payment frontend is running.</p>
    </main>
  );
}

export default App;