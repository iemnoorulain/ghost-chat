import subprocess
import os
import tempfile
import sys

def execute_code(code_str):
    """
    Safely executes python code in a temporary environment and returns stdout/stderr.
    """
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
            f.write(code_str)
            temp_path = f.name
            
        # Run the script with a timeout to prevent infinite loops
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.dirname(os.path.abspath(__file__))
        
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=10,
            cwd=os.path.dirname(os.path.abspath(__file__)),
            env=env
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\nErrors:\n{result.stderr}"
            
        os.remove(temp_path)
        return output if output.strip() else "Script executed successfully with no output."
        
    except subprocess.TimeoutExpired:
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return "Error: Execution timed out (exceeded 10 seconds)."
    except Exception as e:
        return f"Error executing code: {e}"
