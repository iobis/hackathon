import os
import subprocess
import nbformat
from nbconvert import HTMLExporter
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import re

# Directories
notebooks_dir = "notebooks"
screenshots_dir = os.path.join(notebooks_dir, "screenshots")

# Ensure screenshots directory exists
os.makedirs(screenshots_dir, exist_ok=True)

# Function to render Jupyter Notebook or Quarto file
def render_file(file_path):
    if file_path.endswith(".ipynb"):
        html_exporter = HTMLExporter()
        with open(file_path, "r", encoding="utf-8") as f:
            notebook_content = nbformat.read(f, as_version=4) 
        body, _ = html_exporter.from_notebook_node(notebook_content)
        return body
    elif file_path.endswith(".qmd"):
        subprocess.run(["quarto", "render", file_path, "--no-execute"])
        #subprocess.run(["quarto", "render", file_path])
        html_path = file_path.replace(".qmd", ".html")
        with open(html_path, "r", encoding="utf-8") as f:
            body = f.read()
        os.remove(html_path)  # Clean up
        return body

# Function to capture screenshot of HTML content
def capture_screenshot(html_content, output_path):
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # options.add_argument("--no-sandbox")
    # options.add_argument("--disable-dev-shm-usage")
    
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
     # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Ensure the WebDriver is passed the options only once
    driver = webdriver.Chrome(options=chrome_options)

    with open("temp.html", "w") as f:
        f.write(html_content)
    
    driver.get(f"file://{os.path.abspath('temp.html')}")
    time.sleep(2)  # Allow time for rendering
    driver.set_window_size(1200, 2000)
    driver.save_screenshot(output_path)
    driver.quit()
    os.remove("temp.html")

# Function to update README.md
def update_readme(section, file_name, file_path, screenshot_path):
    readme_path = os.path.join(notebooks_dir, "README.md")
    title = file_name.split(".")[0]  # Get title from file name
    title = title.replace("_", " ").title()  # Replace underscores with spaces and capitalize
    screenshot_rel_path = os.path.relpath(screenshot_path, notebooks_dir)
    file_rel_path = os.path.relpath(file_path, notebooks_dir)

    # Load the README.md content
    with open(readme_path, "r") as f:
        content = f.read()

    # Define the pattern to match an existing entry
    pattern = re.compile(rf"(## {title}\n\[.*\]\({re.escape(file_rel_path)}\)\n!\[.*\]\(.*\))", re.MULTILINE)

    # Create the new entry text
    new_entry = f"## {title}\n[{file_name}]({file_rel_path})\n![{title}]({screenshot_rel_path})\n"

    if pattern.search(content):
        # If the entry exists, update it with the new screenshot path
        content = pattern.sub(new_entry, content)
    else:
        # If no entry exists, add a new one under the correct section
        if section == "Python":
            content = re.sub(r"(# Python\n)", rf"\1{new_entry}\n", content)
        elif section == "R":
            content = re.sub(r"(# R\n)", rf"\1{new_entry}\n", content)

    # Write the updated content back to README.md
    with open(readme_path, "w") as f:
        f.write(content)

# Main function to process all new files
def process_notebooks():
    for root, _, files in os.walk(notebooks_dir):
        for file in files:
            if file.endswith(".ipynb") or file.endswith(".qmd"):
                file_path = os.path.join(root, file)
                section = "Python" if "Python" in root else "R"
                
                print(f"Processing {file_path}...")

                # Render file to HTML
                html_content = render_file(file_path)

                # Capture screenshot
                screenshot_name = file.replace(".ipynb", ".png").replace(".qmd", ".png")
                screenshot_path = os.path.join(screenshots_dir, screenshot_name)
                capture_screenshot(html_content, screenshot_path)

                # Update README
                update_readme(section, file, file_path, screenshot_path)

# Run the process
process_notebooks()
