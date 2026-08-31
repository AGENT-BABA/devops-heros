#!/usr/bin/env python3
import os
import markdown
import subprocess

input_path = "/Users/nensiravaliya/Desktop/devops_sst/devops-heros/pdf-con/questions.md"
html_path = "/Users/nensiravaliya/Desktop/devops_sst/devops-heros/pdf-con/simple_questions.html"
pdf_path = "/Users/nensiravaliya/Desktop/devops_sst/devops-heros/pdf-con/questions.pdf"

with open(input_path, "r", encoding="utf-8") as f:
    md_content = f.read()

# Convert markdown directly to HTML using python-markdown with standard extensions
html_body = markdown.markdown(
    md_content,
    extensions=['fenced_code', 'tables', 'nl2br', 'sane_lists']
)

simple_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Questions</title>
<style>
  @page {{
    size: A4;
    margin: 20mm 15mm 20mm 15mm;
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #111827;
    margin: 0;
    padding: 0;
  }}
  h1, h2, h3, h4 {{
    color: #111827;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    font-weight: 700;
  }}
  p {{
    margin: 0.6em 0;
  }}
  pre, code {{
    font-family: Menlo, Monaco, Consolas, "Courier New", monospace;
    font-size: 10pt;
    background-color: #f3f4f6;
  }}
  pre {{
    padding: 10px 14px;
    border-radius: 4px;
    border: 1px solid #e5e7eb;
    overflow-x: auto;
    white-space: pre-wrap;
    word-break: break-all;
    margin: 0.8em 0;
  }}
  code {{
    padding: 2px 4px;
    border-radius: 3px;
  }}
  pre code {{
    padding: 0;
    background: none;
  }}
  ol, ul {{
    padding-left: 24px;
    margin: 0.6em 0;
  }}
  li {{
    margin: 0.3em 0;
  }}
  hr {{
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.5em 0;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(simple_html)

chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={pdf_path}",
    f"file://{html_path}"
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode == 0:
    print("Successfully generated simple PDF:", pdf_path)
    print("Size:", os.path.getsize(pdf_path), "bytes")
else:
    print("Error:", res.stderr)
