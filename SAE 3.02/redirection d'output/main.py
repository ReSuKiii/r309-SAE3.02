import subprocess
import sys
import traceback

def divide(a, b):
    return a / b

def main():
    try:
        # Redirect stdout and stderr to a file
        with open("output.txt", "w") as stdout_file, open("errors.txt", "w") as stderr_file:
            # Use subprocess to run a command and capture output
            process = subprocess.Popen(["python", "-c", "print('')"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            stdout_decoded = stdout.decode()
            stderr_decoded = stderr.decode()
            
            # Print to terminal
            print(stdout_decoded)
            print(stderr_decoded, file=sys.stderr)
            
            # Write to files
            stdout_file.write(stdout_decoded)
            stderr_file.write(stderr_decoded)
        
        a = int(input("Enter a number: "))  
        b = int(input("Enter another number: "))
        result = divide(a, b)
        result_message = f"The result of {a} divided by {b} is {result}\n"
        
        # Print to terminal
        print(result_message)
        
        # Write to file
        with open("output.txt", "a") as stdout_file:
            stdout_file.write(result_message)
        
    except ZeroDivisionError as e:
        error_message = f"Error: {e}\n"
        print(error_message, file=sys.stderr)
        with open("errors.txt", "a") as stderr_file:
            stderr_file.write(error_message)
            traceback.print_exc(file=stderr_file)
    except ValueError as e:
        error_message = f"Invalid input: {e}\n"
        print(error_message, file=sys.stderr)
        with open("errors.txt", "a") as stderr_file:
            stderr_file.write(error_message)
            traceback.print_exc(file=stderr_file)
    except Exception as e:
        error_message = f"Unexpected error: {e}\n"
        print(error_message, file=sys.stderr)
        with open("errors.txt", "a") as stderr_file:
            stderr_file.write(error_message)
            traceback.print_exc(file=stderr_file)
        
if __name__ == "__main__":
    main()
