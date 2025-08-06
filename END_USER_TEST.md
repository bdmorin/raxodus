# End User Testing Without PyPI

## Option 1: Test with uvx from Local Wheel (Recommended)

This simulates exactly what an end user would experience:

```bash
# Build the package
cd ~/src/raxodus
python -m build

# Test as a new user with uvx (from anywhere)
cd ~
uvx --from ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl raxodus --version

# Or install it as a tool
uv tool install ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl
raxodus --version
```

## Option 2: TestPyPI (Most Realistic)

Upload to TestPyPI for testing before real PyPI:

```bash
# Build the package
cd ~/src/raxodus
python -m build

# Upload to TestPyPI (requires account at test.pypi.org)
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ raxodus

# Or with uvx
uvx --index-url https://test.pypi.org/simple/ raxodus --version
```

## Option 3: Local Package Index

Create a local PyPI-like server:

```bash
# Install pypiserver
pip install pypiserver

# Create package directory
mkdir ~/local-pypi
cp ~/src/raxodus/dist/* ~/local-pypi/

# Start local PyPI server
pypi-server -p 8080 ~/local-pypi &

# Install from local server
pip install --index-url http://localhost:8080/simple/ raxodus

# Or with uvx
uvx --index-url http://localhost:8080/simple/ raxodus --version
```

## Option 4: Direct GitHub Install (After pushing)

```bash
# Install directly from GitHub
pip install git+https://github.com/bdmorin/raxodus.git

# Or with uvx
uvx --from git+https://github.com/bdmorin/raxodus.git raxodus --version
```

## Complete End User Test Script

```bash
#!/bin/bash
# Full end-user simulation

# 1. Clean environment
cd /tmp
rm -rf raxodus-user-test
mkdir raxodus-user-test
cd raxodus-user-test

# 2. Install from local wheel with uvx
echo "Testing uvx install..."
uvx --from ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl raxodus --version

# 3. Test without credentials
echo "Testing error handling..."
uvx --from ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl raxodus auth test

# 4. Test with credentials
echo "Testing with credentials..."
export RACKSPACE_USERNAME="your-username"
export RACKSPACE_API_KEY="your-api-key"
export RACKSPACE_ACCOUNT="your-account"

uvx --from ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl raxodus auth test
uvx --from ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl raxodus tickets list --format json | head -20

# 5. Test as installed tool
echo "Testing as installed tool..."
uv tool install --force ~/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl
raxodus --version
raxodus tickets list --days 7 --format table

# 6. Cleanup
uv tool uninstall raxodus
cd ..
rm -rf raxodus-user-test

echo "End user test complete!"
```