from pyngrok import ngrok
import subprocess
import time

print("🚀 Starting Fruit Freshness Detection System...")
print("=" * 50)

# Start Flask app in background
print("⏳ Starting Flask app...")
flask_process = subprocess.Popen(['python', 'app.py'])
time.sleep(3)

# Start ngrok tunnel
print("⏳ Starting ngrok tunnel...")
public_url = ngrok.connect(5000)

print("=" * 50)
print(f"✅ Flask app running at: http://localhost:5000")
print(f"🌐 Public URL: {public_url}")
print("=" * 50)
print("📌 Share the Public URL with anyone!")
print("📌 Press Ctrl+C to stop the server\n")

try:
    flask_process.wait()
except KeyboardInterrupt:
    print("\n🛑 Shutting down...")
    ngrok.kill()
    flask_process.terminate()
    print("✅ Server stopped successfully!")