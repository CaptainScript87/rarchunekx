# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Quick Start Commands

### Running the Application
```bash
# Start with diagnostic mode (recommended first run)
python run.py

# Start full application (after confirming everything works)
python main.py

# Test PDF generation capabilities
python test_pdf.py
```

### Development and Testing
```bash
# Install dependencies (optional - app works without them)
pip install -r requirements.txt

# Alternative installation for problematic pip
python -m pip install reportlab num2words
```

### Windows Installation
```cmd
# Run automated installer (Windows)
install.bat

# Or PowerShell version
.\install.ps1
```

## Architecture Overview

This is a Polish invoice generation application with a fallback architecture that works with or without external dependencies.

### Core Components

**Application Entry Points:**
- `main.py` - Full application entry point (requires all dependencies)
- `run.py` - Diagnostic/safe entry point with fallback capabilities

**Business Logic Layer:**
- `rachunek_manager.py` - Main business logic coordinator
- `database.py` - SQLite database operations for invoice storage
- `walidacja.py` - Data validation utilities

**User Interface:**
- `rachunek_gui.py` - Full tkinter-based GUI application
- `run.py` also contains `SimpleRachunekApp` for basic testing

**PDF Generation (Dual Architecture):**
- `pdf_generator.py` - Full PDF generation using reportlab (optional dependency)
- `simple_pdf_generator.py` - Text-based fallback generator (.txt files)

### Database Schema

The application uses SQLite with two main tables:
- `sprzedawca` - Default seller information storage
- `rachunki` - Invoice records with full transaction details

### Fallback Strategy

The application implements graceful degradation:
1. If `reportlab` is available: generates proper PDF files
2. If `reportlab` is missing: generates .txt files with same content structure
3. If GUI fails: `run.py` provides a minimal diagnostic interface

## Key Configuration

**Database:** `rachunki.db` (created automatically in project root)
**Dependencies:** All optional - app works without any pip installations
**File Output:** PDF files (with reportlab) or TXT files (fallback mode)

## Development Notes

### Adding New Features
- Business logic goes in `rachunek_manager.py`
- UI changes go in `rachunek_gui.py`
- Database changes require updates in `database.py`
- Always maintain fallback compatibility in `simple_pdf_generator.py`

### Testing Strategy
- Use `python run.py` for basic functionality verification
- Use `python test_pdf.py` to verify PDF generation capabilities
- Test both with and without reportlab installed

### Polish Language Support
- All text and UI elements are in Polish
- Database stores Polish characters correctly (UTF-8)
- PDF generation supports Polish characters through font configuration

## Important Files

**Never modify:**
- `num2words-0.5.12-py3-none-any.whl` - Offline installer wheel
- `reportlab-4.0.7-py3-none-any.whl` - Offline installer wheel
- `rachunki.db` - User's invoice database

**Configuration:**
- `config.py` - Application configuration
- `requirements.txt` - Optional dependencies list

## Data Analysis Guidelines

When working with data analysis, visualization, or Jupyter Notebook development in this project:

### Key Principles
- Write concise, technical responses with accurate Python examples
- Prioritize readability and reproducibility in data analysis workflows
- Use functional programming where appropriate; avoid unnecessary classes
- Prefer vectorized operations over explicit loops for better performance
- Use descriptive variable names that reflect the data they contain
- Follow PEP 8 style guidelines for Python code

### Data Analysis and Manipulation
- Use pandas for data manipulation and analysis
- Prefer method chaining for data transformations when possible
- Use loc and iloc for explicit data selection
- Utilize groupby operations for efficient data aggregation

### Visualization
- Use matplotlib for low-level plotting control and customization
- Use seaborn for statistical visualizations and aesthetically pleasing defaults
- Create informative and visually appealing plots with proper labels, titles, and legends
- Use appropriate color schemes and consider color-blindness accessibility

### Jupyter Notebook Best Practices
- Structure notebooks with clear sections using markdown cells
- Use meaningful cell execution order to ensure reproducibility
- Include explanatory text in markdown cells to document analysis steps
- Keep code cells focused and modular for easier understanding and debugging
- Use magic commands like %matplotlib inline for inline plotting

### Error Handling and Data Validation
- Implement data quality checks at the beginning of analysis
- Handle missing data appropriately (imputation, removal, or flagging)
- Use try-except blocks for error-prone operations, especially when reading external data
- Validate data types and ranges to ensure data integrity

### Performance Optimization
- Use vectorized operations in pandas and numpy for improved performance
- Utilize efficient data structures (e.g., categorical data types for low-cardinality string columns)
- Consider using dask for larger-than-memory datasets
- Profile code to identify and optimize bottlenecks

### Data Analysis Dependencies
If working with data analysis features:
- pandas
- numpy
- matplotlib
- seaborn
- jupyter
- scikit-learn (for machine learning tasks)

### Data Analysis Conventions
1. Begin analysis with data exploration and summary statistics
2. Create reusable plotting functions for consistent visualizations
3. Document data sources, assumptions, and methodologies clearly
4. Use version control (e.g., git) for tracking changes in notebooks and scripts