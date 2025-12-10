import subprocess
import tempfile
import os
 
def run_python_code(code: str) -> dict:
    # Write the user's code into a temporary Python file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(code.encode())
        tmp_path = tmp.name  # Full path to temp script
 
    try:
        # Docker command with safety limits
        command = [
            "docker", "run", "--rm",
            "--network", "none",            # No internet
            "--memory=128m",                # Max 128 MB RAM
            "--cpus=0.5",                   # Limit CPU
            "--read-only",                  # Read-only filesystem
            "--tmpfs", "/tmp",              # Provide writable /tmp in RAM
            "-v", f"{tmp_path}:/app/script.py:ro",  # Mount script read-only
            "-w", "/app",
            "python:3.11-slim",
            "python", "script.py",
        ]
 
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=10  # 10-second timeout to stop infinite loops
        )
 
        return {
            "output": result.stdout.strip(),
            "errors": result.stderr.strip()
        }
 
    except subprocess.TimeoutExpired:
        # Code ran too long
        return {
            "output": "",
            "errors": "Execution timed out after 10 seconds"
        }
 
    finally:
        # Clean up temporary file
        if os.path.exists(tmp_path):
            os.remove(tmp_path)