import sys
import html

# HTML Template with styling for clean, aligned hex viewing
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hex Stream Diff Analysis</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f8f9fa;
            color: #212529;
            margin: 2rem;
        }}
        h1 {{
            font-size: 1.5rem;
            color: #495057;
            margin-bottom: 1.5rem;
        }}
        .diff-container {{
            background: #ffffff;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            overflow-x: auto;
        }}
        .line {{
            display: flex;
            align-items: center;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
            font-size: 13px;
            line-height: 1.6;
            white-space: pre;
            border-bottom: 1px solid #f1f3f5;
            padding: 0.2rem 0;
        }}
        .line:hover {{
            background-color: #f8f9fa;
        }}
        .line-number {{
            width: 60px;
            color: #adb5bd;
            user-select: none;
            flex-shrink: 0;
            border-right: 1px solid #e9ecef;
            margin-right: 15px;
        }}
        .tokens {{
            display: flex;
            flex-wrap: wrap;
            gap: 4px;
        }}
        .token {{
            padding: 1px 3px;
            border-radius: 3px;
            display: inline-block;
            min-width: 18px;
            text-align: center;
        }}
        .changed {{
            background-color: #ffe3e3;
            color: #c92a2a;
            font-weight: bold;
            position: relative;
            cursor: help;
        }}
        .changed::after {{
            content: attr(data-prev);
            position: absolute;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            background-color: #212529;
            color: #fff;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 11px;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.15s ease;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
            z-index: 10;
        }}
        .changed:hover::after {{
            opacity: 1;
        }}
        .added {{
            background-color: #e6fcf5;
            color: #0ca678;
            font-weight: bold;
        }}
    </style>
</head>
<body>
    <h1>Hex Stream Diff Analysis (Consecutive Lines)</h1>
    <div class="diff-container">
        {content}
    </div>
</body>
</html>
"""

def generate_html_diff(file_path, output_path="diff_result.html"):
    with open(file_path, 'r', encoding='utf-8') as f:
        # Split lines and filter out empty ones
        lines = [line.strip() for line in f if line.strip()]
        
    if not lines:
        print("Error: The input file is empty.")
        return

    html_lines = []

    # Process line 1 (baseline)
    first_tokens = lines[0].split()
    first_token_spans = []
    for token in first_tokens:
        escaped_token = html.escape(token)
        first_token_spans.append(f'<span class="token">{escaped_token}</span>')
        
    html_lines.append(
        f'<div class="line">'
        f'<span class="line-number">1</span>'
        f'<div class="tokens">{" ".join(first_token_spans)}</div>'
        f'</div>'
    )

    # Process subsequent lines comparison (i vs i-1)
    for idx in range(1, len(lines)):
        prev_tokens = lines[idx-1].split()
        curr_tokens = lines[idx].split()
        token_spans = []

        max_len = max(len(prev_tokens), len(curr_tokens))
        
        for i in range(max_len):
            if i < len(curr_tokens):
                curr_val = html.escape(curr_tokens[i])
                
                # Case 1: Token exists in both and is identical
                if i < len(prev_tokens) and curr_tokens[i] == prev_tokens[i]:
                    token_spans.append(f'<span class="token">{curr_val}</span>')
                
                # Case 2: Token exists in both but has changed value
                elif i < len(prev_tokens):
                    prev_val = html.escape(prev_tokens[i])
                    tooltip = f"was: {prev_val}"
                    token_spans.append(
                        f'<span class="token changed" data-prev="{tooltip}">{curr_val}</span>'
                    )
                
                # Case 3: Token is brand new (line extended)
                else:
                    token_spans.append(f'<span class="token added" title="New token">{curr_val}</span>')
            else:
                # Case 4: Token was truncated / missing in current line
                pass

        html_lines.append(
            f'<div class="line">'
            f'<span class="line-number">{idx+1}</span>'
            f'<div class="tokens">{" ".join(token_spans)}</div>'
            f'</div>'
        )

    # Write the completed HTML file
    rendered_html = HTML_TEMPLATE.format(content="\n".join(html_lines))
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(rendered_html)
        
    print(f"Success! HTML report generated at: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Default name is diff_result.html, but can be customized
        out_name = sys.argv[2] if len(sys.argv) > 2 else "diff_result.html"
        generate_html_diff(sys.argv[1], out_name)
    else:
        print("Usage: python script.py <input_file_path> [output_html_path]")