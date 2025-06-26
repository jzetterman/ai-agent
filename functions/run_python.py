import os, subprocess

def run_python_file(working_directory, file_path):
    abs_file_path = os.path.realpath(os.path.join(os.path.realpath(working_directory), file_path))
    
    if not abs_file_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        execution = subprocess.run(['python3', abs_file_path], timeout=30, capture_output=True, cwd=working_directory)
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
    stdout_str = execution.stdout.decode('utf-8').strip()
    stderr_str = execution.stderr.decode('utf-8').strip()
    exit_code = execution.returncode
    return_str = ""
    if stdout_str != '':
        return_str += f'STDOUT: {stdout_str}\n'
    if stderr_str != '':
        return_str += f'STDERR: {stderr_str}\n'
    if exit_code != 0:
         return_str += f'Process exited with code {exit_code}\n'
        
    if return_str == '':
        return "No output produced."
    
    return return_str
