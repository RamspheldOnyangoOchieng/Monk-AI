import re
import os
import json
import asyncio
import time
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.ai_service import AIService
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

class SecurityAnalyzer:
    """Advanced Agent for analyzing code for security vulnerabilities with OWASP Top 10 categorization."""
    
    def __init__(self, db_session: Session = None):
        """Initialize the SecurityAnalyzer agent."""
        self.db_session = db_session or SessionLocal()
        self.ai_service = AIService(session=self.db_session)
        
        # OWASP Top 10 2023 categories with detailed descriptions
        self.owasp_categories = {
            "A01_broken_access_control": {
                "title": "A01:2023 – Broken Access Control",
                "description": "Failures related to authorization and access control",
                "severity_weight": 0.95,
                "common_issues": ["missing authorization", "privilege escalation", "CORS misconfiguration"]
            },
            "A02_cryptographic_failures": {
                "title": "A02:2023 – Cryptographic Failures",
                "description": "Failures related to cryptography and data protection",
                "severity_weight": 0.90,
                "common_issues": ["weak encryption", "hardcoded secrets", "insecure storage"]
            },
            "A03_injection": {
                "title": "A03:2023 – Injection",
                "description": "SQL, NoSQL, OS, and LDAP injection vulnerabilities",
                "severity_weight": 0.85,
                "common_issues": ["SQL injection", "NoSQL injection", "command injection"]
            },
            "A04_insecure_design": {
                "title": "A04:2023 – Insecure Design",
                "description": "Flaws in the application design and architecture",
                "severity_weight": 0.80,
                "common_issues": ["missing security controls", "threat modeling gaps"]
            },
            "A05_security_misconfiguration": {
                "title": "A05:2023 – Security Misconfiguration",
                "description": "Insecure default configurations and settings",
                "severity_weight": 0.75,
                "common_issues": ["default passwords", "unnecessary features", "verbose errors"]
            },
            "A06_vulnerable_components": {
                "title": "A06:2023 – Vulnerable and Outdated Components",
                "description": "Using components with known vulnerabilities",
                "severity_weight": 0.70,
                "common_issues": ["outdated libraries", "unpatched dependencies"]
            },
            "A07_identification_failures": {
                "title": "A07:2023 – Identification and Authentication Failures",
                "description": "Authentication and session management vulnerabilities",
                "severity_weight": 0.75,
                "common_issues": ["weak passwords", "session fixation", "credential stuffing"]
            },
            "A08_software_integrity_failures": {
                "title": "A08:2023 – Software and Data Integrity Failures",
                "description": "Code and infrastructure without integrity verification",
                "severity_weight": 0.65,
                "common_issues": ["unsigned updates", "insecure CI/CD", "dependency confusion"]
            },
            "A09_logging_failures": {
                "title": "A09:2023 – Security Logging and Monitoring Failures",
                "description": "Insufficient logging and monitoring capabilities",
                "severity_weight": 0.60,
                "common_issues": ["insufficient logging", "no alerting", "log tampering"]
            },
            "A10_ssrf": {
                "title": "A10:2023 – Server-Side Request Forgery (SSRF)",
                "description": "Fetching remote resources without validating URL",
                "severity_weight": 0.70,
                "common_issues": ["unvalidated URLs", "internal service access"]
            }
        }
        
        # Enhanced severity levels with CVSS-like scoring
        self.severity_levels = {
            "critical": {"score": 9.0, "color": "#D32F2F", "priority": 1},
            "high": {"score": 7.0, "color": "#F57C00", "priority": 2},
            "medium": {"score": 5.0, "color": "#FBC02D", "priority": 3},
            "low": {"score": 3.0, "color": "#388E3C", "priority": 4},
            "info": {"score": 1.0, "color": "#1976D2", "priority": 5}
        }
        
        # Security scan statistics for demo
        self.security_stats = {
            "total_scans_performed": 2847,
            "vulnerabilities_found": 18624,
            "critical_issues_fixed": 1247,
            "avg_scan_time_ms": 847,
            "security_score_improvement": "73%"
        }
    
    async def analyze_security(self, code: str, language: str, focus_areas: Optional[List[str]] = None, agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """Analyze code for security vulnerabilities with OWASP Top 10 categorization.
        
        Args:
            code: The source code to analyze
            language: The programming language of the code
            focus_areas: Optional list of specific security areas to focus on
            agent_id: The ID of the agent
            task_id: The ID of the task
            
        Returns:
            Dictionary containing comprehensive security analysis with OWASP mapping
        """
        start_time = time.time()
        
        # If no specific focus areas provided, analyze all OWASP categories
        if not focus_areas:
            focus_areas = list(self.owasp_categories.keys())
            
        # Perform static analysis and pattern matching
        static_analysis = self._perform_static_analysis(code, language)
        
        # Generate the security analysis prompt
        prompt = self._generate_security_prompt(code, language, focus_areas, static_analysis)
        
        # Get security analysis from AI
        security_content = await self._get_ai_analysis(
            prompt, language, agent_id=agent_id, task_id=task_id
        )
        
        # Parse and categorize vulnerabilities
        vulnerabilities = self._parse_security_response(security_content)
        
        # Calculate security scores and risk assessment
        security_score = self._calculate_security_score(vulnerabilities)
        risk_assessment = self._generate_risk_assessment(vulnerabilities, language)
        
        analysis_time = time.time() - start_time
        
        return {
            "status": "success",
            "message": "Comprehensive security analysis completed",
            "scan_timestamp": datetime.now().isoformat(),
            "analysis_time_ms": round(analysis_time * 1000, 2),
            "static_analysis": static_analysis,
            "security_score": security_score,
            "risk_assessment": risk_assessment,
            "vulnerabilities": vulnerabilities,
            "owasp_mapping": self._map_to_owasp_categories(vulnerabilities),
            "remediation_priority": self._prioritize_remediation(vulnerabilities),
            "compliance_status": {
                "owasp_top10_coverage": f"{len([v for v in vulnerabilities if v.get('owasp_category')])}/{len(self.owasp_categories)}",
                "critical_issues": len([v for v in vulnerabilities if v.get('severity') == 'critical']),
                "overall_risk_level": security_score["risk_level"],
                "remediation_urgency": "High" if security_score["overall_score"] < 60 else "Medium" if security_score["overall_score"] < 80 else "Low"
            }
        }
    
    def _perform_static_analysis(self, code: str, language: str) -> Dict[str, Any]:
        """Perform static code analysis for common security patterns."""
        analysis = {
            "lines_analyzed": len(code.splitlines()),
            "character_count": len(code),
            "potential_secrets": 0,
            "hardcoded_credentials": 0,
            "sql_patterns": 0,
            "url_patterns": 0,
            "file_operations": 0,
            "network_calls": 0,
            "encryption_usage": 0,
        }
        
        # Pattern matching for common security issues
        patterns = {
            "secrets": [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']'
            ],
            "sql": [
                r'SELECT\s+.*\s+FROM\s+',
                r'INSERT\s+INTO\s+',
                r'UPDATE\s+.*\s+SET\s+',
                r'DELETE\s+FROM\s+'
            ],
            "urls": [
                r'https?://[^\s"\']+',
                r'ftp://[^\s"\']+',
                r'file://[^\s"\']+'
            ],
            "file_ops": [
                r'open\s*\(',
                r'file\s*\(',
                r'read\s*\(',
                r'write\s*\('
            ]
        }
        
        for category, pattern_list in patterns.items():
            count = 0
            for pattern in pattern_list:
                count += len(re.findall(pattern, code, re.IGNORECASE))
            
            if category == "secrets":
                analysis["potential_secrets"] = count
                analysis["hardcoded_credentials"] = count
            elif category == "sql":
                analysis["sql_patterns"] = count
            elif category == "urls":
                analysis["url_patterns"] = count
            elif category == "file_ops":
                analysis["file_operations"] = count
        
        # Check for encryption/security libraries
        security_imports = [
            "cryptography", "hashlib", "ssl", "hmac", "secrets",
            "bcrypt", "jwt", "oauth", "crypto", "Crypto"
        ]
        analysis["encryption_usage"] = sum(1 for lib in security_imports if lib in code)
        
        return analysis
    
    def _calculate_security_score(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate comprehensive security score based on vulnerabilities."""
        if not vulnerabilities:
            return {
                "overall_score": 95,
                "grade": "A",
                "risk_level": "Low",
                "severity_breakdown": {},
                "improvement_areas": []
            }
        
        # Calculate weighted score based on severity
        total_deduction = 0
        severity_breakdown = {}
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "medium")
            if severity not in severity_breakdown:
                severity_breakdown[severity] = 0
            severity_breakdown[severity] += 1
            
            # Deduct points based on severity
            if severity == "critical":
                total_deduction += 25
            elif severity == "high":
                total_deduction += 15
            elif severity == "medium":
                total_deduction += 8
            elif severity == "low":
                total_deduction += 3
            else:  # info
                total_deduction += 1
        
        overall_score = max(0, 100 - total_deduction)
        
        # Determine grade and risk level
        if overall_score >= 90:
            grade, risk_level = "A", "Low"
        elif overall_score >= 80:
            grade, risk_level = "B", "Medium"
        elif overall_score >= 70:
            grade, risk_level = "C", "Medium"
        elif overall_score >= 60:
            grade, risk_level = "D", "High"
        else:
            grade, risk_level = "F", "Critical"
        
        return {
            "overall_score": overall_score,
            "grade": grade,
            "risk_level": risk_level,
            "severity_breakdown": severity_breakdown,
            "total_vulnerabilities": len(vulnerabilities),
            "improvement_areas": self._identify_improvement_areas(vulnerabilities)
        }
    
    def _generate_risk_assessment(self, vulnerabilities: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """Generate detailed risk assessment and recommendations."""
        critical_count = len([v for v in vulnerabilities if v.get("severity") == "critical"])
        high_count = len([v for v in vulnerabilities if v.get("severity") == "high"])
        
        business_impact = "Low"
        if critical_count > 0:
            business_impact = "Critical"
        elif high_count > 2:
            business_impact = "High"
        elif high_count > 0:
            business_impact = "Medium"
        
        return {
            "business_impact": business_impact,
            "attack_likelihood": "High" if critical_count > 0 else "Medium" if high_count > 0 else "Low",
            "data_sensitivity": "High",  # Assume high for demo
            "compliance_requirements": ["OWASP Top 10", "GDPR", "SOC 2"],
            "recommended_actions": [
                "Immediate remediation of critical vulnerabilities",
                "Implement secure coding practices",
                "Regular security testing and code reviews",
                "Security awareness training for development team"
            ],
            "estimated_remediation_time": f"{max(1, len(vulnerabilities) * 2)} hours",
            "next_scan_recommended": "Within 7 days"
        }
    
    def _map_to_owasp_categories(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Map vulnerabilities to OWASP Top 10 categories."""
        owasp_mapping = {}
        
        for category_key, category_info in self.owasp_categories.items():
            category_vulns = [v for v in vulnerabilities if v.get("owasp_category") == category_key]
            if category_vulns:
                owasp_mapping[category_key] = {
                    "title": category_info["title"],
                    "description": category_info["description"],
                    "vulnerability_count": len(category_vulns),
                    "max_severity": max([self.severity_levels[v.get("severity", "low")]["score"] for v in category_vulns]),
                    "vulnerabilities": category_vulns
                }
        
        return owasp_mapping
    
    def _prioritize_remediation(self, vulnerabilities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Prioritize vulnerabilities for remediation."""
        def priority_score(vuln):
            severity = vuln.get("severity", "low")
            return self.severity_levels[severity]["priority"]
        
        sorted_vulns = sorted(vulnerabilities, key=priority_score)
        
        return [
            {
                "title": vuln.get("title", "Security Issue"),
                "severity": vuln.get("severity", "medium"),
                "owasp_category": vuln.get("owasp_category", "unknown"),
                "estimated_fix_time": vuln.get("estimated_fix_time", "2-4 hours"),
                "business_impact": vuln.get("business_impact", "Medium")
            }
            for vuln in sorted_vulns[:10]  # Top 10 priorities
        ]
    
    def _identify_improvement_areas(self, vulnerabilities: List[Dict[str, Any]]) -> List[str]:
        """Identify key areas for security improvement."""
        areas = []
        severity_counts = {}
        
        for vuln in vulnerabilities:
            severity = vuln.get("severity", "medium")
            severity_counts[severity] = severity_counts.get(severity, 0) + 1
        
        if severity_counts.get("critical", 0) > 0:
            areas.append("Critical vulnerability remediation")
        if severity_counts.get("high", 0) > 2:
            areas.append("High-priority security fixes")
        if any("injection" in str(v).lower() for v in vulnerabilities):
            areas.append("Input validation and sanitization")
        if any("authentication" in str(v).lower() for v in vulnerabilities):
            areas.append("Authentication and authorization")
        if any("encryption" in str(v).lower() for v in vulnerabilities):
            areas.append("Data protection and encryption")
        
        return areas[:5]  # Top 5 areas
    
    def _generate_security_prompt(self, code: str, language: str, focus_areas: List[str], static_analysis: Dict[str, Any]) -> str:
        """Generate a prompt for the AI to analyze code for security vulnerabilities."""
        focus_areas_str = ", ".join(focus_areas)
        
        prompt = f"""Analyze the following {language} code for security vulnerabilities. 
        Focus on these security areas: {focus_areas_str}.
        
        For each vulnerability found:
        1. Identify the specific code section that is vulnerable
        2. Explain the vulnerability and its potential impact
        3. Assign a severity level (critical, high, medium, low, info)
        4. Provide specific remediation steps
        5. Include a code example showing the fix
        
        Format your response with clear sections for each vulnerability category.
        Include line numbers where possible to help locate the issues.
        
        CODE TO ANALYZE:
```{language}
{code}
```
        
        Additional context:
        - Lines of code: {static_analysis["lines_analyzed"]}
        - Character count: {static_analysis["character_count"]}
        - Potential secrets: {static_analysis["potential_secrets"]}
        - Hardcoded credentials: {static_analysis["hardcoded_credentials"]}
        - SQL patterns: {static_analysis["sql_patterns"]}
        - URL patterns: {static_analysis["url_patterns"]}
        - File operations: {static_analysis["file_operations"]}
        - Network calls: {static_analysis["network_calls"]}
        - Encryption usage: {static_analysis["encryption_usage"]}
        """.replace('{language}', language)
        
        return prompt
    
    async def _get_ai_analysis(self, prompt: str, language: str, agent_id: int, task_id: int) -> str:
        """Get security analysis from AI model."""
        logger.info(f"Getting AI security analysis for {language} code...")
        try:
            ai_result = await self.ai_service.generate_text(
                prompt=prompt,
                agent_id=agent_id,
                task_id=task_id,
                temperature=0.1,
                max_tokens=2000,
            )
            
            logger.info("Successfully received security analysis from AI.")
            return ai_result.get("content", "")
                    
        except Exception as e:
            logger.error(f"Error getting AI security analysis: {e}", exc_info=True)
            # Re-raise the exception to be handled by the main analyze_security function
            raise Exception(f"Error calling AI service for security analysis: {str(e)}")
    
    def _parse_security_response(self, content: str) -> Dict[str, Any]:
        """Parse the AI-generated security response into structured data."""
        # This regex is a placeholder and may need to be refined based on actual AI output
        result = {
            "summary": "",
            "vulnerabilities": [],
            "total_issues": 0,
            "severity_counts": {
                "critical": 0,
                "high": 0,
                "medium": 0,
                "low": 0,
                "info": 0
            }
        }
        
        # Extract summary
        summary_match = re.search(r'## Summary\n(.+?)\n\n', content, re.DOTALL)
        if summary_match:
            result["summary"] = summary_match.group(1).strip()
        
        # Extract vulnerability categories
        category_sections = re.findall(r'## ([\w\s]+)\n\n(.+?)(?=\n## |$)', content, re.DOTALL)
        
        for category_name, category_content in category_sections:
            # Skip the summary section as we've already processed it
            if category_name.lower() == "summary":
                continue
                
            # Extract individual vulnerabilities
            vulnerabilities = re.split(r'### \d+\.\s+', category_content)
            if vulnerabilities and not vulnerabilities[0].strip():
                vulnerabilities = vulnerabilities[1:]
                
            for vuln in vulnerabilities:
                if not vuln.strip():
                    continue
                    
                vulnerability = {
                    "title": "",
                    "category": category_name.strip(),
                    "vulnerable_code": "",
                    "severity": "",
                    "impact": "",
                    "remediation": "",
                    "secure_code": "",
                    "line_numbers": []
                }
                
                # Extract title
                title_match = re.match(r'^([^\n]+)', vuln)
                if title_match:
                    vulnerability["title"] = title_match.group(1).strip()
                
                # Extract vulnerable code
                code_match = re.search(r'\*\*Vulnerable Code(?:\s*\(Lines\s+([\d\-,\s]+)\))?:\*\*\s*```[^\n]*\n(.+?)```', vuln, re.DOTALL)
                if code_match:
                    line_info = code_match.group(1)
                    vulnerability["vulnerable_code"] = code_match.group(2).strip()
                    
                    # Extract line numbers if available
                    if line_info:
                        # Parse line numbers (e.g., "45-47" or "112" or "45, 47, 50")
                        line_numbers = []
                        for part in line_info.split(','):
                            part = part.strip()
                            if '-' in part:
                                start, end = map(int, part.split('-'))
                                line_numbers.extend(range(start, end + 1))
                            else:
                                line_numbers.append(int(part))
                        vulnerability["line_numbers"] = line_numbers
                
                # Extract severity
                severity_match = re.search(r'\*\*Severity:\*\*\s*([^\n]+)', vuln)
                if severity_match:
                    severity = severity_match.group(1).strip().lower()
                    vulnerability["severity"] = severity
                    # Increment severity count
                    if severity in result["severity_counts"]:
                        result["severity_counts"][severity] += 1
                
                # Extract impact
                impact_match = re.search(r'\*\*Impact:\*\*\s*([^\n]+(?:\n[^\n*]+)*)', vuln)
                if impact_match:
                    vulnerability["impact"] = impact_match.group(1).strip()
                
                # Extract remediation
                remediation_match = re.search(r'\*\*Remediation:\*\*\s*(.+?)(?=\*\*Secure Code Example:|$)', vuln, re.DOTALL)
                if remediation_match:
                    # Extract bullet points if present
                    remediation_text = remediation_match.group(1).strip()
                    remediation_items = re.findall(r'^-\s*(.+)$', remediation_text, re.MULTILINE)
                    
                    if remediation_items:
                        vulnerability["remediation"] = remediation_items
                    else:
                        vulnerability["remediation"] = [remediation_text]
                
                # Extract secure code example
                secure_code_match = re.search(r'\*\*Secure Code Example:\*\*\s*```[^\n]*\n(.+?)```', vuln, re.DOTALL)
                if secure_code_match:
                    vulnerability["secure_code"] = secure_code_match.group(1).strip()
                
                result["vulnerabilities"].append(vulnerability)
        
        # Update total issues count
        result["total_issues"] = len(result["vulnerabilities"])
        
        return result
    
    def _determine_cwe_category(self, vulnerability_title: str, category: str) -> str:
        """Map the vulnerability to a CWE (Common Weakness Enumeration) category."""
        # This is a simplified mapping - in a real implementation, this would be more comprehensive
        cwe_mapping = {
            "sql injection": "CWE-89: SQL Injection",
            "command injection": "CWE-77: Command Injection",
            "xss": "CWE-79: Cross-site Scripting",
            "csrf": "CWE-352: Cross-Site Request Forgery",
            "open redirect": "CWE-601: URL Redirection to Untrusted Site",
            "path traversal": "CWE-22: Path Traversal",
            "file inclusion": "CWE-98: File Inclusion",
            "weak password": "CWE-521: Weak Password Requirements",
            "plaintext password": "CWE-256: Plaintext Storage of Password",
            "hardcoded credential": "CWE-798: Hardcoded Credentials",
            "sensitive data exposure": "CWE-200: Information Exposure",
            "missing encryption": "CWE-311: Missing Encryption",
            "insecure deserialization": "CWE-502: Deserialization of Untrusted Data",
            "xxe": "CWE-611: XML External Entity Reference",
            "security misconfiguration": "CWE-1004: Security Misconfiguration",
            "missing authentication": "CWE-306: Missing Authentication",
            "broken authentication": "CWE-287: Improper Authentication",
            "broken access control": "CWE-284: Improper Access Control",
            "insufficient logging": "CWE-778: Insufficient Logging"
        }
        
        # Try to match based on the title (case insensitive)
        title_lower = vulnerability_title.lower()
        for key, cwe in cwe_mapping.items():
            if key in title_lower:
                return cwe
        
        # If no match in title, try to match based on category
        category_lower = category.lower()
        if "injection" in category_lower:
            return "CWE-74: Injection"
        elif "authentication" in category_lower:
            return "CWE-287: Improper Authentication"
        elif "data exposure" in category_lower:
            return "CWE-200: Information Exposure"
        elif "xxe" in category_lower:
            return "CWE-611: XML External Entity Reference"
        elif "access control" in category_lower:
            return "CWE-284: Improper Access Control"
        elif "security misconfig" in category_lower:
            return "CWE-1004: Security Misconfiguration"
        elif "xss" in category_lower:
            return "CWE-79: Cross-site Scripting"
        elif "insecure deserialization" in category_lower:
            return "CWE-502: Deserialization of Untrusted Data"
        elif "vulnerable component" in category_lower:
            return "CWE-1104: Use of Unmaintained Third Party Components"
        elif "logging" in category_lower:
            return "CWE-778: Insufficient Logging"
        
        # Default if no match found
        return "CWE-0: Unknown"