# Monk-AI Comprehensive Test Cycle Documentation

## Overview

This document outlines the comprehensive test cycle for the Monk-AI project, covering frontend presentation, agent functionality testing with multiple AI providers, integration testing, and documentation procedures.

## Test Cycle Structure

### 1. Test Environment Setup

#### Prerequisites
- Python 3.8+
- Node.js 16+
- FastAPI backend running on `http://localhost:8000`
- React frontend running on `http://localhost:3000`
- API keys for AI providers (OpenAI, Gemini, OpenRouter)

#### Required Dependencies
```bash
# Backend dependencies
pip install fastapi uvicorn aiohttp requests openai google-generativeai

# Frontend dependencies
cd frontend
npm install
```

### 2. AI Provider Configuration

#### OpenAI API
- **Status**: Pre-configured
- **API Key**: `your-openai-api-key-here`
- **Base URL**: `https://api.openai.com/v1`
- **Model**: `gpt-4`

#### Google Gemini API
- **Setup**: User-provided API key
- **Model**: `gemini-pro`
- **Integration**: Using `google-generativeai` SDK
- **Documentation**: [Google AI Studio](https://makersuite.google.com/app/apikey)

#### OpenRouter API
- **Setup**: User-provided API key
- **Base URL**: `https://openrouter.ai/api/v1`
- **Model**: `openai/gpt-4`
- **Integration**: Compatible with OpenAI SDK
- **Documentation**: [OpenRouter Docs](https://openrouter.ai/docs)

### 3. Test Cases

#### 3.1 AI Provider Connectivity Tests

| Test Case | Description | Expected Result |
|-----------|-------------|----------------|
| TC-001 | OpenAI API Connection | ✅ Connection successful |
| TC-002 | Gemini API Connection | ✅ Connection successful (if key provided) |
| TC-003 | OpenRouter API Connection | ✅ Connection successful (if key provided) |

#### 3.2 Backend Connectivity Tests

| Test Case | Description | Expected Result |
|-----------|-------------|----------------|
| TC-004 | Backend Health Check | ✅ HTTP 200, response time < 1000ms |
| TC-005 | API Root Endpoint | ✅ JSON response with message |

#### 3.3 Frontend Connectivity Tests

| Test Case | Description | Expected Result |
|-----------|-------------|----------------|
| TC-006 | Frontend App Loading | ✅ HTTP 200, React app loads |
| TC-007 | Frontend Response Time | ✅ Response time < 2000ms |

#### 3.4 Agent Functionality Tests

##### 3.4.1 Code Optimizer Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-008 | Python Code Optimization | Sample Python code with inefficiencies | Optimized code suggestions, performance metrics |
| TC-009 | JavaScript Code Optimization | Sample JS code | Optimized code with improvements |
| TC-010 | Multi-provider Testing | Same code across providers | Consistent optimization suggestions |

**Sample Input Code:**
```python
def fibonacci(n):
    """Calculate fibonacci sequence inefficiently"""
    if n <= 1:
        return n
    result = []
    a, b = 0, 1
    for i in range(n):
        result.append(a)
        temp = a + b
        a = b
        b = temp
    return result
```

**Expected Optimizations:**
- Generator function implementation
- Memoization suggestions
- Time complexity improvements
- Memory usage optimization

##### 3.4.2 Documentation Generator Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-011 | Python Documentation | Undocumented Python functions | Complete docstrings, type hints |
| TC-012 | Class Documentation | Python classes | Class and method documentation |
| TC-013 | API Documentation | Code with API endpoints | API documentation with examples |

##### 3.4.3 Security Analyzer Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-014 | SQL Injection Detection | Code with SQL vulnerabilities | Security warnings, fix suggestions |
| TC-015 | XSS Vulnerability Detection | JavaScript with XSS risks | Security alerts, mitigation strategies |
| TC-016 | Hardcoded Secrets Detection | Code with exposed credentials | Security violations, best practices |

**Sample Vulnerable Code:**
```python
def process_data(data):
    for item in data:
        # SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE id = {item}"
        # Execute query...
```

**Expected Security Findings:**
- SQL injection vulnerability identified
- Parameterized query suggestions
- Input validation recommendations

##### 3.4.4 Test Generator Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-017 | Unit Test Generation | Python functions | Comprehensive unit tests |
| TC-018 | Integration Test Generation | API endpoints | Integration test cases |
| TC-019 | Edge Case Testing | Complex functions | Edge case test scenarios |

##### 3.4.5 PR Reviewer Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-020 | Code Review | Pull request data | Review comments, suggestions |
| TC-021 | Best Practices Check | Code changes | Best practice recommendations |
| TC-022 | Performance Review | Performance-critical code | Performance optimization suggestions |

##### 3.4.6 Ideation Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-023 | Feature Ideation | Project requirements | Creative feature suggestions |
| TC-024 | Architecture Suggestions | System requirements | Architecture recommendations |
| TC-025 | Technology Stack Ideas | Project constraints | Technology stack suggestions |

##### 3.4.7 Orchestrator Agent

| Test Case | Description | Input | Expected Output |
|-----------|-------------|-------|----------------|
| TC-026 | Workflow Orchestration | Multi-step task | Coordinated agent workflow |
| TC-027 | Task Prioritization | Multiple tasks | Prioritized execution plan |
| TC-028 | Resource Management | Complex workflow | Optimized resource allocation |

#### 3.5 Frontend-Backend Integration Tests

| Test Case | Description | Endpoint | Expected Result |
|-----------|-------------|----------|----------------|
| TC-029 | Code Optimization API | `/api/agents/optimize` | ✅ HTTP 200, optimization results |
| TC-030 | Documentation API | `/api/agents/document` | ✅ HTTP 200, documentation output |
| TC-031 | Security Analysis API | `/api/agents/security-analyze` | ✅ HTTP 200, security findings |
| TC-032 | Test Generation API | `/api/agents/generate-tests` | ✅ HTTP 200, test cases |
| TC-033 | PR Review API | `/api/agents/review-pr` | ✅ HTTP 200, review comments |
| TC-034 | Ideation API | `/api/agents/ideate` | ✅ HTTP 200, ideas and suggestions |
| TC-035 | Orchestration API | `/api/agents/orchestrate` | ✅ HTTP 200, workflow results |

### 4. Performance Metrics

#### 4.1 Response Time Benchmarks

| Component | Target Response Time | Acceptable Range |
|-----------|---------------------|------------------|
| Backend API | < 500ms | < 1000ms |
| Frontend Loading | < 1000ms | < 2000ms |
| Agent Processing | < 10s | < 30s |
| AI Provider Calls | < 5s | < 15s |

#### 4.2 Quality Metrics

| Metric | Measurement | Target |
|--------|-------------|--------|
| Output Quality | Response length and relevance | > 200 characters, contextually relevant |
| Success Rate | Successful completions / Total tests | > 90% |
| Error Rate | Failed tests / Total tests | < 10% |
| Provider Consistency | Similar outputs across providers | Variance < 20% |

### 5. Test Execution Procedures

#### 5.1 Pre-Test Setup

1. **Start Backend Server**
   ```bash
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend Server**
   ```bash
   cd frontend
   npm start
   ```

3. **Verify Services**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

#### 5.2 Running Comprehensive Tests

1. **Execute Test Suite**
   ```bash
   cd tests
   python comprehensive_test_cycle.py
   ```

2. **Provide API Keys**
   - Enter Gemini API key when prompted (optional)
   - Enter OpenRouter API key when prompted (optional)

3. **Monitor Test Progress**
   - Watch console output for real-time results
   - Check for any error messages or failures

#### 5.3 Individual Test Execution

1. **Agent Integration Tests**
   ```bash
   python test_agents_integration.py
   ```

2. **Frontend-Backend Integration**
   ```bash
   python test_frontend_backend_integration.py
   ```

3. **Hackathon Demo Tests**
   ```bash
   python test_hackathon_demo.py
   ```

### 6. Test Results and Reporting

#### 6.1 Result Files

- **Location**: `tests/results/`
- **Format**: JSON files with timestamp
- **Naming**: `test_results_YYYYMMDD_HHMMSS.json`

#### 6.2 Result Structure

```json
{
  "timestamp": "2024-01-01T12:00:00",
  "test_cycle_name": "Comprehensive Monk-AI Test Cycle",
  "version": "1.0",
  "environment": {
    "backend_url": "http://localhost:8000",
    "frontend_url": "http://localhost:3000",
    "python_version": "3.9.0",
    "os": "nt"
  },
  "provider_status": {
    "openai": {"status": "connected", "available": true},
    "gemini": {"status": "connected", "available": true},
    "openrouter": {"status": "connected", "available": true}
  },
  "agent_tests": {
    "code_optimizer": {
      "openai": {
        "success": true,
        "execution_time": 2.5,
        "output_quality": "excellent"
      }
    }
  },
  "integration_tests": {
    "backend": {"status": "healthy", "response_time_ms": 45},
    "frontend": {"status": "healthy", "response_time_ms": 120}
  },
  "performance_metrics": {
    "average_execution_time": 3.2,
    "min_execution_time": 1.1,
    "max_execution_time": 8.7
  },
  "summary": {
    "total_tests": 35,
    "passed_tests": 32,
    "failed_tests": 3,
    "success_rate": 91.43
  }
}
```

### 7. Troubleshooting Guide

#### 7.1 Common Issues

| Issue | Symptoms | Solution |
|-------|----------|----------|
| Backend Not Running | Connection refused errors | Start FastAPI server |
| Frontend Not Loading | 404 errors on frontend tests | Start React development server |
| API Key Issues | Authentication errors | Verify API keys are correct |
| Import Errors | Module not found | Install required dependencies |
| Timeout Errors | Tests hanging | Check network connectivity |

#### 7.2 Debug Mode

To run tests with detailed debugging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run tests with verbose output
python comprehensive_test_cycle.py --debug
```

### 8. Continuous Integration

#### 8.1 GitHub Actions Integration

Create `.github/workflows/test-cycle.yml`:

```yaml
name: Monk-AI Test Cycle

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run comprehensive tests
      env:
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
      run: |
        cd tests
        python comprehensive_test_cycle.py
```

### 9. Test Maintenance

#### 9.1 Regular Updates

- **Weekly**: Run full test suite
- **Monthly**: Update test cases and expected results
- **Quarterly**: Review and optimize test performance

#### 9.2 Test Case Evolution

- Add new test cases for new features
- Update existing tests when APIs change
- Remove obsolete tests for deprecated features

### 10. Success Criteria

#### 10.1 Test Cycle Completion

- ✅ All AI providers tested successfully
- ✅ All 7 agents functional with primary provider (OpenAI)
- ✅ Frontend-backend integration working
- ✅ Performance metrics within acceptable ranges
- ✅ Success rate > 90%
- ✅ Test results documented and saved

#### 10.2 Ready for Production

- ✅ All critical tests passing
- ✅ No security vulnerabilities detected
- ✅ Performance benchmarks met
- ✅ Documentation complete and up-to-date
- ✅ Pull request created with test results

---

## Conclusion

This comprehensive test cycle ensures the Monk-AI project meets quality standards across all components, from individual agent functionality to full-stack integration. The test suite provides confidence in the system's reliability, performance, and security before deployment.

For questions or issues with the test cycle, please refer to the troubleshooting guide or contact the development team.