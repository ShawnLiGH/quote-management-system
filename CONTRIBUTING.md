# Contributing to Equipment Quote Management System

Thank you for your interest in contributing! 🎉

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python version, etc.)

### Suggesting Features

Feature requests are welcome! Please:
- Check existing issues first
- Describe the feature and its use case
- Explain why it would be valuable

### Code Contributions

#### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/quote-management-system.git
cd quote-management-system
```

#### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8
```

#### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bugfix-name
```

#### 4. Make Changes

- Write clean, readable code
- Follow existing code style
- Add comments for complex logic
- Update documentation if needed

#### 5. Test Your Changes

```bash
# Run the app locally
streamlit run app.py

# Test your specific changes thoroughly
# If adding tests (encouraged):
pytest tests/
```

#### 6. Commit Your Changes

```bash
git add .
git commit -m "Brief description of changes"
```

**Good commit messages:**
- "Add support for Excel file export"
- "Fix database connection timeout issue"
- "Update README with Docker instructions"

**Bad commit messages:**
- "fixed stuff"
- "update"
- "asdf"

#### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request with:
- Clear title
- Description of changes
- Reference to related issues (if any)

## Code Style Guidelines

### Python Code

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

Example:
```python
def process_quote(quote_text: str, use_ocr: bool = False) -> dict:
    """
    Process a quote from text.
    
    Args:
        quote_text: The quote text to process
        use_ocr: Whether to use OCR processing
        
    Returns:
        dict: Processed quote data
    """
    # Implementation
    pass
```

### Streamlit UI

- Keep UI clean and intuitive
- Use consistent styling
- Add helpful tooltips
- Provide clear error messages

### Documentation

- Update README.md for new features
- Add inline comments for complex logic
- Update type hints
- Keep examples up to date

## Project Structure

```
src/
├── pdf_processor.py    # PDF handling logic
├── claude_analyzer.py  # AI analysis logic
└── database.py         # Database operations

app.py                  # Main Streamlit app
```

When adding new functionality:
- Add core logic to appropriate module in `src/`
- Add UI in `app.py`
- Update documentation

## Testing

While the project doesn't currently have extensive tests, you can add them:

```python
# tests/test_database.py
from src.database import QuoteDatabase

def test_database_init():
    db = QuoteDatabase(':memory:')
    assert db is not None

def test_insert_quote():
    db = QuoteDatabase(':memory:')
    quote_id = db.insert_quote(
        filename="test.pdf",
        original_text="test",
        analysis_result={}
    )
    assert quote_id > 0
```

## What We're Looking For

### High Priority
- Bug fixes
- Performance improvements
- Better error handling
- Additional file format support
- UI/UX improvements

### Medium Priority
- New features
- Code refactoring
- Documentation improvements
- Test coverage

### Low Priority
- Style changes
- Minor optimizations

## Questions?

Feel free to:
- Open an issue for discussion
- Ask in Pull Request comments
- Reach out to maintainers

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers
- Focus on what's best for the project
- Accept constructive criticism

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing! 🙏**
