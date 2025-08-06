# Fresh User Test Guide for raxodus

This guide simulates a new user installing and using raxodus for the first time.

## Test 1: Local Installation Test (Before PyPI)

```bash
# Create a fresh test environment
cd /tmp
mkdir raxodus-test && cd raxodus-test

# Create a clean virtual environment
python3 -m venv test-env
source test-env/bin/activate

# Install from the built wheel
pip install /Users/bdmorin/src/raxodus/dist/raxodus-0.1.0-py3-none-any.whl

# Test basic commands
raxodus --version
raxodus --help
raxodus auth --help
raxodus tickets --help

# Test with missing credentials (should error gracefully)
raxodus auth test

# Set credentials
export RACKSPACE_USERNAME="your-username"
export RACKSPACE_API_KEY="your-api-key"
export RACKSPACE_ACCOUNT="your-account"

# Test authentication
raxodus auth test

# Test listing tickets
raxodus tickets list --format json
raxodus tickets list --format table
raxodus tickets list --format csv

# Test searching
raxodus tickets search "backup"

# Cleanup
deactivate
cd ..
rm -rf raxodus-test
```

## Test 2: UVX Installation Test (After PyPI)

```bash
# Test with uvx (once published)
uvx raxodus --version
uvx raxodus --help

# Or install globally with uvx
uv tool install raxodus
raxodus --version

# Set credentials
export RACKSPACE_USERNAME="your-username"
export RACKSPACE_API_KEY="your-api-key"

# Use it
raxodus auth test
raxodus tickets list --days 7 --format json
```

## Test 3: n8n Integration Test

```bash
# Install and test JSON output
uvx raxodus tickets list --format json | jq '.'
uvx raxodus tickets list --format json | jq '.tickets[] | select(.status == "open")'

# Test with specific account
RACKSPACE_ACCOUNT=123456 uvx raxodus tickets list --format json
```

## Expected Behaviors

### Success Cases
- ✅ Clean JSON output for automation
- ✅ Human-readable table format
- ✅ CSV export for spreadsheets
- ✅ Clear error messages

### Error Cases
- ❌ Missing credentials → Clear error message
- ❌ Invalid credentials → Authentication error
- ❌ No account specified → Prompt for account
- ❌ Rate limited → Automatic retry with backoff

## Checklist

- [ ] Package installs cleanly
- [ ] CLI entry point works
- [ ] Help text is clear
- [ ] Authentication works
- [ ] JSON output is valid
- [ ] Table output is readable
- [ ] CSV output opens in Excel
- [ ] Error messages are helpful
- [ ] Cache works (second call is faster)
- [ ] Rate limiting works