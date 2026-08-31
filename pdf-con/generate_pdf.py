#!/usr/bin/env python3
import os
import re
import html
import subprocess

def parse_markdown(md_content):
    lines = md_content.splitlines()
    assessments = []
    
    current_assessment = None
    current_item = None
    current_type = None
    current_lines = []
    
    def flush():
        nonlocal current_item, current_type, current_lines
        if current_item and current_assessment:
            current_assessment["items"].append({
                "type": current_type,
                "title": current_item,
                "lines": [l for l in current_lines]
            })
        current_item = None
        current_type = None
        current_lines = []

    for line in lines:
        stripped = line.strip()
        
        # Check Assessment title
        m_assess = re.match(r"^Assessment\s+(\d+):\s*(.*)$", stripped)
        if m_assess:
            flush()
            current_assessment = {
                "num": m_assess.group(1),
                "title": m_assess.group(2).strip(),
                "items": []
            }
            assessments.append(current_assessment)
            continue
            
        if stripped in ("⸻", "---", "***"):
            flush()
            continue
            
        m_mcq = re.match(r"^MCQ\s+(\d+)\b", stripped)
        if m_mcq:
            flush()
            current_item = f"MCQ {m_mcq.group(1)}"
            current_type = "mcq"
            continue
            
        m_lab = re.match(r"^Lab\s+(\d+):\s*(.*)$", stripped)
        if m_lab:
            flush()
            current_item = f"Lab {m_lab.group(1)}: {m_lab.group(2).strip()}"
            current_type = "lab"
            continue
            
        if current_assessment is not None:
            current_lines.append(line)
            
    flush()
    return assessments

def render_mcq(item):
    lines = [l.strip() for l in item["lines"] if l.strip()]
    question_lines = []
    options = []
    answer = None
    notes = []
    
    state = "question"
    for l in lines:
        m_opt = re.match(r"^([A-D])\.\s*(.*)$", l)
        m_ans = re.match(r"^Answer:\s*(.*)$", l, re.IGNORECASE)
        
        if m_ans:
            state = "answer"
            answer = m_ans.group(1).strip()
        elif m_opt and state in ("question", "options"):
            state = "options"
            options.append((m_opt.group(1), m_opt.group(2).strip()))
        elif state == "question":
            question_lines.append(l)
        elif state == "answer":
            notes.append(l)
            
    q_text = html.escape(" ".join(question_lines))
    
    html_out = f"""
    <div class="card mcq-card">
      <div class="card-header">
        <span class="badge mcq-badge">{html.escape(item['title'])}</span>
      </div>
      <div class="question-text">{q_text}</div>
      <div class="options-grid">
    """
    
    # Extract correct option letter if present in answer
    correct_letter = None
    if answer:
        m_letter = re.match(r"^([A-D])\b", answer)
        if m_letter:
            correct_letter = m_letter.group(1)
            
    for letter, opt_text in options:
        is_correct = (letter == correct_letter)
        opt_class = "option-item correct-option" if is_correct else "option-item"
        html_out += f"""
        <div class="{opt_class}">
          <span class="option-letter">{letter}</span>
          <span class="option-text">{html.escape(opt_text)}</span>
          { '<span class="correct-check">✓</span>' if is_correct else '' }
        </div>
        """
        
    html_out += "</div>"
    
    if answer:
        html_out += f"""
        <div class="answer-box">
          <span class="answer-label">Correct Answer:</span>
          <span class="answer-value">{html.escape(answer)}</span>
        </div>
        """
        
    if notes:
        note_text = html.escape(" ".join(notes))
        html_out += f"""
        <div class="callout-box note-box">
          <span class="callout-icon">💡</span>
          <span class="callout-content">{note_text}</span>
        </div>
        """
        
    html_out += "</div>"
    return html_out

def render_lab(item):
    lines = item["lines"]
    
    html_out = f"""
    <div class="card lab-card">
      <div class="card-header">
        <span class="badge lab-badge">{html.escape(item['title'])}</span>
      </div>
      <div class="lab-body">
    """
    
    # Parse blocks within lab
    # We can identify:
    # 1. Directory tree / preformatted blocks
    # 2. Command blocks (lines starting with known commands or grouped commands)
    # 3. Numbered lists (1. Create...)
    # 4. Bullet lists (* What is...)
    # 5. Callouts / "Students should:", "Expected output:", "Ask students:", etc.
    
    idx = 0
    while idx < len(lines):
        line = lines[idx]
        stripped = line.strip()
        
        if not stripped:
            idx += 1
            continue
            
        # Check for directory tree or ascii structure
        if "├──" in stripped or "└──" in stripped or stripped.startswith("devops/"):
            tree_lines = []
            while idx < len(lines) and (lines[idx].strip().startswith("devops/") or "├──" in lines[idx] or "└──" in lines[idx] or "│" in lines[idx] or not lines[idx].strip()):
                if lines[idx].strip():
                    tree_lines.append(lines[idx])
                idx += 1
            html_out += f"""
            <div class="tree-container">
              <div class="code-header"><span class="code-title">📁 Directory Structure</span></div>
              <pre class="tree-block"><code>{html.escape(chr(10).join(tree_lines))}</code></pre>
            </div>
            """
            continue
            
        # Check for command block or script block
        # If line looks like bash code:
        is_code_start = (
            stripped.startswith("#!/bin/bash") or
            stripped.startswith("mkdir ") or
            stripped.startswith("touch ") or
            stripped.startswith("echo ") or
            stripped.startswith("cat ") or
            stripped.startswith("ls ") or
            stripped.startswith("rm ") or
            stripped.startswith("chmod ") or
            stripped.startswith("ip ") or
            stripped.startswith("ping ") or
            stripped.startswith("python3 -m ") or
            stripped.startswith("ss ") or
            stripped.startswith("git ") or
            stripped.startswith("docker ") or
            stripped.startswith("apk ") or
            stripped.startswith("curl ") or
            stripped.startswith("./check_number") or
            stripped.startswith("<h1>")
        )
        
        # Check if line is "Expected commands may include:", "Example:", "Commands:", etc.
        m_label = re.match(r"^(Expected commands may include|Possible command|Commands|Example|Create a script|Output|Expected permission|Expected output|Inside the container|Then exit|Then|Then verify the permission|Ask students|Expected concept|Students should explain|Students should identify|Students should|Bonus question):\s*(.*)$", stripped, re.IGNORECASE)
        
        if m_label:
            lbl_type = m_label.group(1).strip()
            rest = m_label.group(2).strip()
            
            if "Expected output" in lbl_type or "Expected permission" in lbl_type or "Output" in lbl_type:
                html_out += f'<div class="section-label output-label"><span class="label-badge">📋 Output</span> {html.escape(lbl_type)}'
                if rest:
                    html_out += f': <code>{html.escape(rest)}</code>'
                html_out += '</div>'
            elif "Ask students" in lbl_type or "Bonus question" in lbl_type or "Expected concept" in lbl_type:
                html_out += f'<div class="callout-box info-box"><span class="callout-icon">🎯</span><span class="callout-content"><strong>{html.escape(lbl_type)}:</strong> {html.escape(rest)}'
                idx += 1
                # grab immediate following lines if explanation
                while idx < len(lines) and lines[idx].strip() and not re.match(r"^(Lab|\d+\.|\*|mkdir|docker|git|touch|chmod)", lines[idx].strip()):
                    html_out += f' {html.escape(lines[idx].strip())}'
                    idx += 1
                html_out += '</span></div>'
                continue
            else:
                html_out += f'<div class="section-label"><span class="label-badge">⚡</span> {html.escape(lbl_type)}'
                if rest:
                    html_out += f' {html.escape(rest)}'
                html_out += '</div>'
            idx += 1
            continue

        # Numbered list item
        m_num = re.match(r"^(\d+)\.\s*(.*)$", stripped)
        if m_num:
            num_val = m_num.group(1)
            content = m_num.group(2)
            html_out += f"""
            <div class="step-item">
              <span class="step-num">{num_val}</span>
              <span class="step-text">{html.escape(content)}</span>
            </div>
            """
            idx += 1
            continue
            
        # Bullet list item
        m_bullet = re.match(r"^[\*\-]\s*(.*)$", stripped)
        if m_bullet:
            content = m_bullet.group(1)
            html_out += f"""
            <div class="bullet-item">
              <span class="bullet-dot">•</span>
              <span class="bullet-text">{html.escape(content)}</span>
            </div>
            """
            idx += 1
            continue
            
        # Code lines grouping
        if is_code_start or stripped.startswith("exit") or stripped.startswith("whoami") or stripped.startswith("pwd"):
            code_lines = []
            while idx < len(lines):
                cur = lines[idx].strip()
                if not cur:
                    # check if next is code
                    if idx + 1 < len(lines) and (lines[idx+1].strip().startswith("echo ") or lines[idx+1].strip().startswith("cat ") or lines[idx+1].strip().startswith("docker ") or lines[idx+1].strip().startswith("git ")):
                        code_lines.append("")
                        idx += 1
                        continue
                    else:
                        break
                if re.match(r"^(Lab|\d+\.|\*|Students should|Ask students|Expected|Then|Inside the container|Remove the container|Create another container|Check:|Build the image:|Run it:|Open:|Then open:|Bonus question)", cur):
                    break
                code_lines.append(lines[idx])
                idx += 1
                
            code_text = "\n".join(code_lines)
            html_out += f"""
            <div class="code-container">
              <div class="code-header">
                <span class="terminal-dots"><span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span></span>
                <span class="code-title">Terminal / Command</span>
              </div>
              <pre class="code-block"><code>{html.escape(code_text)}</code></pre>
            </div>
            """
            continue
            
        # Normal descriptive paragraph or single file name
        if stripped.endswith(".txt") or stripped.endswith(".sh") or stripped.endswith(".html") or stripped == "Dockerfile" or stripped == "README.md":
            html_out += f'<div class="file-target"><span class="file-icon">📄</span> <code>{html.escape(stripped)}</code></div>'
        elif stripped.startswith("http://"):
            html_out += f'<div class="url-box"><span class="url-icon">🌐</span> <a href="{html.escape(stripped)}">{html.escape(stripped)}</a></div>'
        else:
            html_out += f'<p class="lab-p">{html.escape(stripped)}</p>'
            
        idx += 1

    html_out += """
      </div>
    </div>
    """
    return html_out

def generate_html(assessments):
    content_html = ""
    
    total_mcqs = sum(len([i for i in a["items"] if i["type"] == "mcq"]) for a in assessments)
    total_labs = sum(len([i for i in a["items"] if i["type"] == "lab"]) for a in assessments)
    
    # Header Banner
    content_html += f"""
    <div class="document-header">
      <div class="badge-row">
        <span class="hero-badge">DevOps Practice & Assessment Series</span>
        <span class="meta-badge">7 Modules</span>
        <span class="meta-badge">{total_mcqs} MCQs</span>
        <span class="meta-badge">{total_labs} Hands-on Labs</span>
      </div>
      <h1 class="main-title">DevOps Engineering Assessments & Labs</h1>
      <p class="main-subtitle">Core competency review covering Linux Administration, Networking, Bash Scripting, Git Version Control, and Docker Containerization.</p>
      
      <div class="toc-grid">
    """
    
    for a in assessments:
        content_html += f"""
        <div class="toc-chip">
          <span class="toc-num">#{a['num']}</span>
          <span class="toc-name">{html.escape(a['title'])}</span>
        </div>
        """
        
    content_html += """
      </div>
    </div>
    """
    
    for a in assessments:
        content_html += f"""
        <section class="assessment-section" id="assessment-{a['num']}">
          <div class="assessment-header">
            <div class="assessment-number-badge">Module {a['num']}</div>
            <h2 class="assessment-title">{html.escape(a['title'])}</h2>
          </div>
          <div class="assessment-grid">
        """
        
        # MCQs first
        mcq_items = [item for item in a["items"] if item["type"] == "mcq"]
        if mcq_items:
            content_html += '<div class="mcq-section-title"><span>📝 Multiple Choice Questions</span></div><div class="mcqs-wrapper">'
            for item in mcq_items:
                content_html += render_mcq(item)
            content_html += '</div>'
            
        # Labs next
        lab_items = [item for item in a["items"] if item["type"] == "lab"]
        if lab_items:
            content_html += '<div class="lab-section-title"><span>🛠️ Hands-on Lab Exercises</span></div><div class="labs-wrapper">'
            for item in lab_items:
                content_html += render_lab(item)
            content_html += '</div>'
            
        content_html += """
          </div>
        </section>
        """

    # Full HTML wrapper with CSS
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>DevOps Assessments & Labs</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

  @page {{
    size: A4 portrait;
    margin: 14mm 12mm 14mm 12mm;
    @bottom-right {{
      content: "Page " counter(page);
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      font-size: 8pt;
      color: #94a3b8;
    }}
  }}

  * {{
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }}

  body {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    font-size: 9.5pt;
    line-height: 1.5;
  }}

  /* Document Header */
  .document-header {{
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #1e293b 100%);
    color: #ffffff;
    padding: 24px 28px;
    border-radius: 12px;
    margin-bottom: 24px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
  }}

  .badge-row {{
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 12px;
  }}

  .hero-badge {{
    background: #3b82f6;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 3px 9px;
    border-radius: 6px;
  }}

  .meta-badge {{
    background: rgba(255, 255, 255, 0.12);
    color: #e2e8f0;
    font-size: 7.5pt;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 6px;
  }}

  .main-title {{
    font-size: 20pt;
    font-weight: 800;
    margin: 0 0 8px 0;
    color: #ffffff;
    letter-spacing: -0.5px;
  }}

  .main-subtitle {{
    font-size: 9pt;
    color: #94a3b8;
    margin: 0 0 16px 0;
    line-height: 1.4;
    max-width: 90%;
  }}

  .toc-grid {{
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 6px;
    margin-top: 14px;
    padding-top: 14px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
  }}

  .toc-chip {{
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 5px 8px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .toc-num {{
    color: #60a5fa;
    font-weight: 700;
    font-size: 7.5pt;
  }}

  .toc-name {{
    color: #f1f5f9;
    font-size: 7.5pt;
    font-weight: 600;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }}

  /* Assessment Section */
  .assessment-section {{
    margin-bottom: 24px;
    page-break-inside: auto;
  }}

  .assessment-header {{
    display: flex;
    align-items: center;
    gap: 10px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-left: 5px solid #2563eb;
    padding: 8px 14px;
    border-radius: 8px;
    margin-bottom: 12px;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .assessment-number-badge {{
    background: #2563eb;
    color: #ffffff;
    font-size: 7.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    padding: 2px 8px;
    border-radius: 4px;
  }}

  .assessment-title {{
    font-size: 12pt;
    font-weight: 700;
    color: #0f172a;
    margin: 0;
  }}

  .mcq-section-title, .lab-section-title {{
    font-size: 8.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #64748b;
    margin: 10px 0 6px 0;
    page-break-after: avoid;
    break-after: avoid;
  }}

  .mcqs-wrapper {{
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 12px;
  }}

  .labs-wrapper {{
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-bottom: 12px;
  }}

  /* Cards Common */
  .card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 8px;
    padding: 10px 12px;
    page-break-inside: avoid;
    break-inside: avoid;
  }}

  .card-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
  }}

  .badge {{
    display: inline-block;
    font-size: 7pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    padding: 2px 7px;
    border-radius: 4px;
  }}

  .mcq-badge {{
    background: #e0f2fe;
    color: #0369a1;
    border: 1px solid #bae6fd;
  }}

  .lab-badge {{
    background: #ede9fe;
    color: #5b21b6;
    border: 1px solid #ddd6fe;
  }}

  /* MCQ Card Specifics */
  .mcq-card {{
    background: #ffffff;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .question-text {{
    font-weight: 600;
    font-size: 8.5pt;
    color: #1e293b;
    margin-bottom: 8px;
    line-height: 1.35;
  }}

  .options-grid {{
    display: flex;
    flex-direction: column;
    gap: 4px;
    margin-bottom: 8px;
  }}

  .option-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 4px 7px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 5px;
    font-size: 8pt;
    color: #334155;
  }}

  .correct-option {{
    background: #f0fdf4;
    border-color: #86efac;
    color: #166534;
    font-weight: 600;
  }}

  .option-letter {{
    font-weight: 700;
    color: #64748b;
    font-size: 7.5pt;
    min-width: 14px;
  }}

  .correct-option .option-letter {{
    color: #16a34a;
  }}

  .option-text {{
    flex: 1;
  }}

  .correct-check {{
    color: #16a34a;
    font-weight: 700;
    font-size: 8pt;
  }}

  .answer-box {{
    background: #f0fdf4;
    border: 1px solid #bbf7d0;
    border-radius: 5px;
    padding: 4px 8px;
    font-size: 7.5pt;
    display: flex;
    gap: 5px;
    align-items: center;
  }}

  .answer-label {{
    font-weight: 700;
    color: #166534;
  }}

  .answer-value {{
    color: #15803d;
    font-weight: 600;
  }}

  /* Lab Card Specifics */
  .lab-card {{
    border-left: 4px solid #6366f1;
    background: #fafafa;
  }}

  .lab-body {{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }}

  .lab-p {{
    margin: 0;
    font-size: 8.5pt;
    color: #334155;
  }}

  .section-label {{
    font-weight: 700;
    font-size: 8pt;
    color: #1e293b;
    margin-top: 4px;
    display: flex;
    align-items: center;
    gap: 4px;
  }}

  .output-label {{
    color: #0369a1;
  }}

  .step-item {{
    display: flex;
    align-items: flex-start;
    gap: 8px;
    font-size: 8pt;
    color: #334155;
  }}

  .step-num {{
    background: #6366f1;
    color: #ffffff;
    font-weight: 700;
    font-size: 7pt;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 1px;
  }}

  .step-text {{
    flex: 1;
    line-height: 1.35;
  }}

  .bullet-item {{
    display: flex;
    align-items: flex-start;
    gap: 6px;
    font-size: 8pt;
    color: #334155;
    margin-left: 4px;
  }}

  .bullet-dot {{
    color: #6366f1;
    font-weight: bold;
  }}

  .file-target {{
    font-size: 8pt;
    color: #0f172a;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #f1f5f9;
    padding: 2px 6px;
    border-radius: 4px;
    border: 1px solid #e2e8f0;
    width: fit-content;
  }}

  .url-box {{
    font-size: 8pt;
    color: #2563eb;
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: #eff6ff;
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid #bfdbfe;
    width: fit-content;
  }}

  .url-box a {{
    color: #2563eb;
    text-decoration: none;
    font-family: 'JetBrains Mono', monospace;
    font-size: 7.5pt;
  }}

  /* Code & Terminal Blocks */
  .code-container, .tree-container {{
    margin: 4px 0;
    border-radius: 6px;
    overflow: hidden;
    border: 1px solid #1e293b;
    background: #0f172a;
  }}

  .code-header {{
    background: #1e293b;
    padding: 3px 8px;
    display: flex;
    align-items: center;
    gap: 6px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
  }}

  .terminal-dots {{
    display: flex;
    gap: 4px;
  }}

  .dot {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
  }}

  .dot.red {{ background: #ef4444; }}
  .dot.yellow {{ background: #f59e0b; }}
  .dot.green {{ background: #10b981; }}

  .code-title {{
    color: #94a3b8;
    font-size: 6.5pt;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-family: 'JetBrains Mono', monospace;
  }}

  pre.code-block, pre.tree-block {{
    margin: 0;
    padding: 8px 10px;
    font-family: 'JetBrains Mono', "SFMono-Regular", Consolas, monospace;
    font-size: 7.5pt;
    line-height: 1.4;
    color: #38bdf8;
    background: #0f172a;
    overflow-x: hidden;
    white-space: pre-wrap;
    word-break: break-all;
  }}

  pre.tree-block {{
    color: #a5f3fc;
  }}

  code {{
    font-family: 'JetBrains Mono', "SFMono-Regular", Consolas, monospace;
    font-size: 8pt;
    background: #f1f5f9;
    color: #0f172a;
    padding: 1px 4px;
    border-radius: 3px;
    border: 1px solid #e2e8f0;
  }}

  pre code {{
    background: transparent;
    padding: 0;
    border: none;
    color: inherit;
  }}

  /* Callouts */
  .callout-box {{
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 8pt;
    display: flex;
    gap: 8px;
    align-items: flex-start;
    margin-top: 4px;
  }}

  .note-box {{
    background: #fffbeb;
    border: 1px solid #fde68a;
    color: #92400e;
    margin-top: 6px;
  }}

  .info-box {{
    background: #f0fdfa;
    border: 1px solid #99f6e4;
    color: #115e59;
  }}

  .callout-icon {{
    font-size: 9pt;
    line-height: 1.2;
    flex-shrink: 0;
  }}

  .callout-content {{
    flex: 1;
    line-height: 1.35;
  }}

  /* Print Media Rules */
  @media print {{
    body {{
      background: #ffffff;
    }}
    .assessment-section {{
      page-break-inside: auto;
    }}
    .card {{
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    .mcq-section-title, .lab-section-title {{
      page-break-after: avoid;
      break-after: avoid;
    }}
  }}
</style>
</head>
<body>
{content_html}
</body>
</html>
"""
    return full_html

def main():
    input_path = "/Users/nensiravaliya/Desktop/devops_sst/devops-heros/pdf-con/questions.md"
    html_path = "/Users/nensiravaliya/Desktop/devops_sst/devops-heros/pdf-con/questions.html"
    pdf_path = "/Users/nensiravaliya/Desktop/devops_sst/devops-heros/pdf-con/questions.pdf"
    
    with open(input_path, "r", encoding="utf-8") as f:
        md_content = f.read()
        
    assessments = parse_markdown(md_content)
    html_rendered = generate_html(assessments)
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_rendered)
    print(f"Generated HTML at: {html_path}")
    
    # Chrome headless command
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_path}",
        f"file://{html_path}"
    ]
    
    print("Converting HTML to PDF via Chrome headless...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Successfully generated PDF at: {pdf_path}")
        print(f"PDF Size: {os.path.getsize(pdf_path)} bytes")
    else:
        print("Chrome error:", result.stderr)

if __name__ == "__main__":
    main()
