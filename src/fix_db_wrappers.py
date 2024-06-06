import sys

def process_dump_file():
    # Read the entire input from stdin
    input_data = sys.stdin.read()
    
    # Split the input into lines
    lines = input_data.split('\n')
    
    # Remove the first two lines
    lines = lines[2:]
    
    # Define the new lines to add
    new_lines_top = [
        "set autocommit=0;",
        "set unique_checks=0;",
        "set foreign_key_checks=0;"]
    new_lines_bottom = [
        "set autocommit=1;",
        "set unique_checks=1;",
        "set foreign_key_checks=1;"]
    
    # Add new lines to the top and bottom
    lines = new_lines_top + lines + new_lines_bottom
    
    # Join the lines back into a single string
    output_data = '\n'.join(lines)
    
    # Write the output to stdout
    sys.stdout.write(output_data)

if __name__ == "__main__":
    process_dump_file()
