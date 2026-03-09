"""Minimal Jekyll-like preview server. Compiles SCSS, processes templates, serves on port 4000."""
import http.server
import os
import re
import socketserver
import yaml

PORT = 4000
BASE = os.path.dirname(os.path.abspath(__file__))

def load_config():
    with open(os.path.join(BASE, "_config.yml"), encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_layout(name):
    path = os.path.join(BASE, "_layouts", f"{name}.html")
    with open(path, encoding="utf-8") as f:
        return f.read()

def read_page(filepath):
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    # Split front matter
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            fm = yaml.safe_load(parts[1]) or {}
            content = parts[2]
            return fm, content
    return {}, text

def render_template(template, site, page, content):
    html = template

    # Process {% for link in site.navigation %}...{% endfor %}
    for_pattern = r'\{%\s*for\s+(\w+)\s+in\s+site\.navigation\s*%\}(.*?)\{%\s*endfor\s*%\}'
    match = re.search(for_pattern, html, re.DOTALL)
    if match:
        var_name = match.group(1)
        loop_body = match.group(2)
        result_parts = []
        for item in site.get("navigation", []):
            rendered = loop_body
            for key, val in item.items():
                rendered = rendered.replace("{{ " + var_name + "." + key + " }}", str(val))
            # Handle external check
            if item.get("external"):
                rendered = re.sub(r'\{%\s*if\s+' + var_name + r'\.external\s*%\}(.*?)\{%\s*else\s*%\}.*?\{%\s*endif\s*%\}', r'\1', rendered, flags=re.DOTALL)
                rendered = re.sub(r'\{%\s*if\s+' + var_name + r'\.external\s*%\}(.*?)\{%\s*endif\s*%\}', r'\1', rendered, flags=re.DOTALL)
            else:
                rendered = re.sub(r'\{%\s*if\s+' + var_name + r'\.external\s*%\}.*?\{%\s*else\s*%\}(.*?)\{%\s*endif\s*%\}', r'\1', rendered, flags=re.DOTALL)
                rendered = re.sub(r'\{%\s*if\s+' + var_name + r'\.external\s*%\}.*?\{%\s*endif\s*%\}', '', rendered, flags=re.DOTALL)

            # Active class
            page_url = page.get("url", "/")
            link_url = item.get("url", "")
            if page_url == link_url:
                rendered = rendered.replace('class="nav-link "', 'class="nav-link active"')

            # Prepend baseurl for non-external
            if not item.get("external"):
                url_val = site.get("baseurl", "") + item["url"]
                rendered = rendered.replace("{{ " + var_name + ".url | prepend: site.baseurl }}", url_val)
                rendered = rendered.replace("{{ " + var_name + ".url | relative_url }}", url_val)

            result_parts.append(rendered)
        html = html[:match.start()] + "".join(result_parts) + html[match.end():]

    # Replace simple variables
    html = html.replace("{{ content }}", content)
    html = html.replace("{{ page.title | default: site.title }}", page.get("title", site.get("title", "")))
    html = html.replace("{{ page.description | default: site.description }}", page.get("description", site.get("description", "")))

    # Replace relative_url filters
    baseurl = site.get("baseurl", "")
    html = re.sub(r"\{\{\s*'([^']+)'\s*\|\s*relative_url\s*\}\}", lambda m: baseurl + m.group(1), html)
    html = re.sub(r"\{\{\s*\"([^\"]+)\"\s*\|\s*relative_url\s*\}\}", lambda m: baseurl + m.group(1), html)

    # Date filter for copyright
    from datetime import datetime
    html = re.sub(r"\{\{\s*'now'\s*\|\s*date:\s*\"%Y\"\s*\}\}", datetime.now().strftime("%Y"), html)

    # Clean up any remaining liquid tags
    html = re.sub(r'\{%.*?%\}', '', html)
    html = re.sub(r'\{\{.*?\}\}', '', html)

    return html

def compile_scss():
    """Recursive SCSS to CSS compiler with full nesting support."""
    scss_path = os.path.join(BASE, "_sass", "main.scss")
    with open(scss_path, encoding="utf-8") as f:
        scss = f.read()

    # Remove single-line comments
    scss = re.sub(r'//.*$', '', scss, flags=re.MULTILINE)

    # Collect and replace variables
    variables = {}
    for m in re.finditer(r'^\$([a-zA-Z0-9_-]+)\s*:\s*([^;]+);', scss, re.MULTILINE):
        variables[m.group(1)] = m.group(2).strip()
    scss = re.sub(r'^\$[a-zA-Z0-9_-]+\s*:[^;]+;\n?', '', scss, flags=re.MULTILINE)

    # Resolve variable references in values (iterate to handle chained refs)
    for _ in range(3):
        for name, val in list(variables.items()):
            for ref_name, ref_val in variables.items():
                if f'${ref_name}' in val:
                    val = val.replace(f'${ref_name}', ref_val)
            variables[name] = val

    for name, val in variables.items():
        scss = scss.replace(f'${name}', val)

    # Handle rgba with hex colors
    scss = re.sub(r'rgba\(#([0-9a-fA-F]{6}),\s*([\d.]+)\)',
                  lambda m: f'rgba({int(m.group(1)[:2],16)},{int(m.group(1)[2:4],16)},{int(m.group(1)[4:6],16)},{m.group(2)})', scss)
    scss = re.sub(r'darken\(([^,]+),\s*\d+%?\)', r'\1', scss)

    def find_matching_brace(text, start):
        depth = 1
        i = start
        while i < len(text) and depth > 0:
            if text[i] == '{': depth += 1
            elif text[i] == '}': depth -= 1
            i += 1
        return i

    def parse_blocks(text):
        """Parse text into a list of (selector, body) tuples and bare properties."""
        results = []
        i = 0
        while i < len(text):
            # Skip whitespace
            while i < len(text) and text[i] in ' \t\n\r':
                i += 1
            if i >= len(text):
                break

            # Try to find a block: selector { ... }
            brace_pos = text.find('{', i)
            semi_pos = text.find(';', i)

            if brace_pos == -1 and semi_pos == -1:
                remaining = text[i:].strip()
                if remaining:
                    results.append(('prop', remaining))
                break
            elif brace_pos == -1 or (semi_pos != -1 and semi_pos < brace_pos):
                # Property before next block
                prop = text[i:semi_pos].strip()
                if prop and ':' in prop:
                    results.append(('prop', prop + ';'))
                i = semi_pos + 1
            else:
                selector = text[i:brace_pos].strip()
                body_start = brace_pos + 1
                body_end = find_matching_brace(text, body_start)
                body = text[body_start:body_end - 1]
                if selector:
                    results.append(('block', selector, body))
                i = body_end
        return results

    def resolve_selector(parent, child):
        if '&' in child:
            return child.replace('&', parent)
        return parent + ' ' + child

    def flatten(selector, body):
        """Recursively flatten nested SCSS into flat CSS rules."""
        output = []
        parsed = parse_blocks(body)
        props = [item[1] for item in parsed if item[0] == 'prop']
        if props:
            output.append(f'{selector} {{\n  ' + '\n  '.join(props) + '\n}')
        for item in parsed:
            if item[0] == 'block':
                child_sel = item[1]
                child_body = item[2]
                # Handle comma-separated selectors
                child_sels = [s.strip() for s in child_sel.split(',')]
                for cs in child_sels:
                    if selector == '@media':
                        # Should not happen at this level
                        pass
                    full = resolve_selector(selector, cs)
                    output.extend(flatten(full, child_body))
        return output

    def process_top_level(text):
        output = []
        parsed = parse_blocks(text)
        for item in parsed:
            if item[0] == 'prop':
                pass  # top-level props are unusual, skip
            elif item[0] == 'block':
                sel = item[1]
                body = item[2]
                if sel.startswith('@media'):
                    # For @media, flatten inner blocks within the media query
                    inner_parsed = parse_blocks(body)
                    inner_rules = []
                    for inner in inner_parsed:
                        if inner[0] == 'block':
                            inner_rules.extend(flatten(inner[1], inner[2]))
                        elif inner[0] == 'prop':
                            inner_rules.append(inner[1])
                    output.append(f'{sel} {{\n' + '\n\n'.join('  ' + r.replace('\n', '\n  ') for r in inner_rules) + '\n}')
                else:
                    output.extend(flatten(sel, body))
        return '\n\n'.join(output)

    css = process_top_level(scss)

    os.makedirs(os.path.join(BASE, "_site", "assets", "css"), exist_ok=True)
    with open(os.path.join(BASE, "_site", "assets", "css", "style.css"), "w", encoding="utf-8") as f:
        f.write(css)

def build_site():
    config = load_config()
    layout = load_layout("default")
    baseurl = config.get("baseurl", "")

    # Build output dir
    site_dir = os.path.join(BASE, "_site")
    os.makedirs(site_dir, exist_ok=True)

    # Copy media
    import shutil
    media_src = os.path.join(BASE, "media")
    media_dst = os.path.join(site_dir, "media")
    if os.path.exists(media_dst):
        try:
            shutil.rmtree(media_dst)
        except PermissionError:
            pass  # OneDrive lock, just overwrite files
    if not os.path.exists(media_dst):
        os.makedirs(media_dst, exist_ok=True)
    for f in os.listdir(media_src):
        src_file = os.path.join(media_src, f)
        dst_file = os.path.join(media_dst, f)
        if os.path.isfile(src_file):
            shutil.copy2(src_file, dst_file)

    # Compile SCSS
    compile_scss()

    # Override baseurl for local preview
    config["baseurl"] = ""

    # Build pages
    pages = [
        ("index.md", "index.html", "/"),
        ("projects.md", os.path.join("projects", "index.html"), "/projects/"),
        ("publications.md", os.path.join("publications", "index.html"), "/publications/"),
    ]

    for src, dst, url in pages:
        src_path = os.path.join(BASE, src)
        if not os.path.exists(src_path):
            continue
        fm, content = read_page(src_path)
        fm["url"] = url
        html = render_template(layout, config, fm, content)
        dst_path = os.path.join(site_dir, dst)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        with open(dst_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Built: {dst}")

    print(f"\nSite built to _site/")

def serve():
    site_dir = os.path.join(BASE, "_site")
    os.chdir(site_dir)

    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    print("Building site...")
    build_site()
    print(f"\nStarting server on port {PORT}...")
    serve()
