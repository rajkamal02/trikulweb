with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()
# Find script tag content
script_start = html.rfind("<script>")
script_end = html.rfind("</script>")
if script_start > 0 and script_end > 0:
    before_script = html[:script_start + len("<script>")]
    script_content = html[script_start + len("<script>"):script_end]
    after_script = html[script_end:]
    # Remove duplicate DATE and PROFILE blocks - keep only last occurrence
    # Split by the marker and take unique
    marker = "// DATE"
    parts = script_content.split(marker)
    if len(parts) > 2:
        # Keep only: everything before first DATE block + last DATE block onwards
        script_content = parts[0] + marker + parts[-1]
    html = before_script + script_content + after_script
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done!")
