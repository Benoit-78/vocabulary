
# Code quality
pylint src/ tests/ --recursive=yes

npx eslint src/static/scripts/**

# Test coverage
tests

# Number of lines of code
cd src && git ls-files | grep -v '\.jpg$' | xargs wc -l && cd ..
