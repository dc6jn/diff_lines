import sys

# ANSI escape codes for terminal coloring
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def highlight_consecutive_diffs(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
        
    if not lines:
        print("File is empty.")
        return

    # Print the very first line as the baseline
    print(f"Line 1: {lines[0]}")

    for idx in range(1, len(lines)):
        prev_tokens = lines[idx-1].split()
        curr_tokens = lines[idx].split()
        output_line = []

        # Compare up to the length of the shorter line
        max_len = max(len(prev_tokens), len(curr_tokens))
        
        for i in range(max_len):
            # If token exists in both and is identical
            if i < len(prev_tokens) and i < len(curr_tokens) and prev_tokens[i] == curr_tokens[i]:
                output_line.append(curr_tokens[i])
            # If token changed
            elif i < len(curr_tokens):
                token = curr_tokens[i]
                output_line.append(f"{RED}{token}{RESET}")
            # If token was removed/missing from current line
            else:
                pass 

        print(f"Line {idx+1}: {' '.join(output_line)}")

# Usage: python diff.py my_data_file.txt
if __name__ == "__main__":
    if len(sys.argv) > 1:
        highlight_consecutive_diffs(sys.argv[1])
    else:
        print("Please provide a path to your text file.")