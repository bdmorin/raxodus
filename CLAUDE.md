# Raxodus Development Guidelines

## Version 1.0 Release Criteria

**DO NOT release v1.0 until ALL of these criteria are met:**

### API Stability Requirements
- [ ] Rackspace has fixed their API inconsistencies (field naming, date formats)
- [ ] API documentation matches actual implementation
- [ ] Service catalog properly identifies production endpoints (not "demo")
- [ ] API response times are consistently under 2 seconds
- [ ] SSL certificates are valid on all API endpoints

### Feature Completeness
- [ ] Write operations work (update ticket status, add comments) OR Rackspace officially documents read-only status
- [ ] Pagination works correctly with standard patterns
- [ ] Error responses include meaningful details (not just 404s)
- [ ] All promised CLI commands work reliably

### Code Quality
- [ ] 90%+ test coverage with real API integration tests
- [ ] All models validated against actual API responses
- [ ] No workarounds for API bugs in the codebase
- [ ] Clean separation between API client and CLI layers
- [ ] Comprehensive error handling with user-friendly messages

### Documentation
- [ ] Complete API documentation from Rackspace
- [ ] All CLI commands documented with examples
- [ ] n8n integration guide with working examples
- [ ] Troubleshooting guide for common issues

### Production Readiness
- [ ] Used in production for at least 3 months without major issues
- [ ] No breaking changes needed for at least 6 months
- [ ] Performance benchmarks documented
- [ ] Rate limiting properly handled
- [ ] Caching strategy proven effective

### Community
- [ ] At least 100 downloads from PyPI
- [ ] No unresolved critical bugs for 30 days
- [ ] Feedback from at least 5 different organizations
- [ ] Clear migration path if Rackspace changes their API

## Why These Criteria Matter

**Version 1.0 implies stability and production readiness.** Given that:
- The Rackspace API is currently broken in multiple ways
- The documentation doesn't match reality
- Basic operations don't work as advertised
- We're using a "demo" endpoint in production

Releasing 1.0 would be misleading to users. We stay in 0.x to signal that:
- The tool works but has limitations
- Breaking changes may be necessary
- We're dependent on Rackspace fixing their infrastructure
- This is a workaround for a broken API, not a stable integration

## Version Numbering Strategy

### 0.x Releases (Current Phase)
- **0.1.x** - Bug fixes, documentation updates
- **0.2.0** - "Minax" - Add new feature that works around API limitations
- **0.3.0** - "Exodus" - Major workaround or significant feature
- **0.x.0** - Continue with Ultima antagonists for major features

### Post-1.0 (When Criteria Met)
- **1.0.0** - First stable release (keep same codename from 0.x)
- **1.x.0** - Minor releases: Ultima companions (Iolo, Shamino, Dupre, etc.)
- **2.0.0** - Major release: Move to Ultima IV virtues (Honesty, Compassion, etc.)

## Development Principles

1. **Don't hide API problems** - Document them clearly
2. **Fail loudly** - Better to error than silently return wrong data
3. **Keep it minimal** - Don't add features that might break
4. **Document everything** - Especially API quirks and workarounds
5. **Test with real API** - Mocks hide the actual problems

## Current API Issues Blocking 1.0

1. OPTIONS claims PATCH/PUT work but they return 404
2. Invalid dates in list responses (0001-01-01)
3. Inconsistent field names (ticketId vs id, created vs createdAt)
4. "Demo" endpoint in production
5. No write access despite documentation claiming otherwise
6. Service catalog missing documented services
7. 30+ second response times for simple queries
8. No proper error messages or status codes