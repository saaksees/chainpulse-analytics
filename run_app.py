import os
import sys

# Set working directory to project root
project_root = os.path.dirname(os.path.abspath(__file__))
os.chdir(project_root)

# Add to Python path
sys.path.insert(0, project_root)

print(f"🔍 Running from: {project_root}")
print(f"🔍 Templates at: {os.path.join(project_root, 'app', 'templates')}")
print(f"🔍 home.html exists: {os.path.exists(os.path.join(project_root, 'app', 'templates', 'home.html'))}")

from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("╔══════════════════════════════════════════╗")
    print("║      ⚡ CHAINPULSE WEB APP STARTING      ║")
    print("╠══════════════════════════════════════════╣")
    print("║  URL: http://localhost:5000              ║")
    print("║  Press CTRL+C to stop                   ║")
    print("╚══════════════════════════════════════════╝")
    
    # Run with SocketIO support
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)