from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from scanner import MalwareScanner
from scraper import ContentScraper
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Initialize Scanner and Scraper
scanner = MalwareScanner()
scraper = ContentScraper()

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def run_scan():
    """Endpoint to trigger a scan of the samples directory."""
    directory = request.form.get('directory', 'samples')
    try:
        results = scanner.scan_directory(directory)
        return render_template('results.html', report=results)
    except Exception as e:
        flash(f"Scan failed: {str(e)}", "danger")
        return redirect(url_for('index'))

@app.route('/scrape-and-scan', methods=['POST'])
def scrape_and_scan():
    """Endpoint to download a file from a URL and scan it."""
    url = request.form.get('url')
    if not url:
        flash("Please provide a valid URL.", "warning")
        return redirect(url_for('index'))

    filepath = scraper.download_file(url)
    if filepath:
        matches = scanner.scan_file(filepath)
        return render_template('single_result.html', filename=os.path.basename(filepath), matches=matches)
    else:
        flash("Failed to download file from URL.", "danger")
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
