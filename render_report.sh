#!/bin/bash

# Render Security Requirements Report with Quarto
# This script renders the most recent security requirements report to HTML and/or PDF

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored messages
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Check if Quarto is installed
if ! command -v quarto &> /dev/null; then
    print_error "Quarto is not installed. Please install it first:"
    echo "  macOS: brew install quarto"
    echo "  Linux: Download from https://quarto.org/docs/get-started/"
    echo "  Windows: Download from https://quarto.org/docs/get-started/"
    exit 1
fi

print_success "Quarto is installed: $(quarto --version)"

# Check if Python dependencies are installed
echo "Checking Python dependencies..."
if ! python -c "import plotly, pandas, numpy" 2>/dev/null; then
    print_warning "Some Python dependencies are missing. Installing..."
    uv pip install plotly pandas numpy kaleido
fi

# Find the most recent security requirements file
REPORT_FILE=$(ls -t outputs/security_requirements_*.qmd 2>/dev/null | head -1)

if [ -z "$REPORT_FILE" ]; then
    print_error "No security requirements reports found in outputs/ directory."
    echo "Please generate a report first using:"
    echo "  python -m security_requirements_system.main"
    exit 1
fi

print_success "Found report: $REPORT_FILE"

# Parse command line arguments
FORMAT="${1:-both}"  # Default to both formats

case "$FORMAT" in
    html)
        echo ""
        echo "Rendering to HTML (interactive)..."
        quarto render "$REPORT_FILE" --to html
        print_success "HTML report generated: ${REPORT_FILE%.md}.html"
        ;;
    pdf)
        echo ""
        echo "Rendering to PDF (static)..."
        quarto render "$REPORT_FILE" --to pdf
        print_success "PDF report generated: ${REPORT_FILE%.md}.pdf"
        ;;
    both|all)
        echo ""
        echo "Rendering to HTML (interactive)..."
        quarto render "$REPORT_FILE" --to html
        print_success "HTML report generated: ${REPORT_FILE%.md}.html"
        
        echo ""
        echo "Rendering to PDF (static)..."
        quarto render "$REPORT_FILE" --to pdf
        print_success "PDF report generated: ${REPORT_FILE%.md}.pdf"
        ;;
    *)
        print_error "Invalid format: $FORMAT"
        echo "Usage: $0 [html|pdf|both]"
        echo "  html - Generate interactive HTML report only"
        echo "  pdf  - Generate static PDF report only"
        echo "  both - Generate both HTML and PDF (default)"
        exit 1
        ;;
esac

echo ""
print_success "Rendering complete!"
echo ""
echo "Reports location:"
ls -lh "${REPORT_FILE%.md}".{html,pdf} 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
echo ""
echo "To view the HTML report:"
echo "  open ${REPORT_FILE%.md}.html"
echo ""

