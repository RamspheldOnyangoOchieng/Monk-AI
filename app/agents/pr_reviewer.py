from typing import List, Dict, Any
import os
import re
import time
import httpx
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.ai_service import AIService
from app.core.database import SessionLocal

class PRReviewer:
    """Advanced Pull Request Reviewer with complexity scoring and impact assessment."""
    
    def __init__(self, db_session: Session = None):
        """Initialize the PRReviewer agent."""
        self.db_session = db_session or SessionLocal()
        self.ai_service = AIService(session=self.db_session)
        
        # PR complexity scoring weights
        self.complexity_weights = {
            "files_changed": 0.2,
            "lines_added": 0.15,
            "lines_deleted": 0.1,
            "cyclomatic_complexity": 0.25,
            "function_changes": 0.1,
            "test_coverage": 0.1,
            "dependency_changes": 0.1
        }
        
        # Review quality metrics for demo
        self.review_stats = {
            "total_prs_reviewed": 1847,
            "issues_caught": 9234,
            "avg_review_time_mins": 12.4,
            "critical_bugs_prevented": 847,
            "code_quality_improvement": "84%"
        }
        
        # Impact assessment categories
        self.impact_categories = {
            "breaking_changes": {"weight": 0.9, "color": "#D32F2F"},
            "feature_additions": {"weight": 0.7, "color": "#1976D2"},
            "bug_fixes": {"weight": 0.5, "color": "#388E3C"},
            "refactoring": {"weight": 0.6, "color": "#F57C00"},
            "documentation": {"weight": 0.2, "color": "#9C27B0"},
            "tests": {"weight": 0.4, "color": "#00796B"}
        }

    async def review_pr(self, pr_url: str, repository: str, branch: str = "main", agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """
        Review a pull request with advanced complexity scoring and impact assessment.
        """
        start_time = time.time()
        
        try:
            # TODO: Fetch PR details using GitHub API
            pr_details = await self._fetch_pr_details(pr_url)
            
            # Perform complexity analysis
            complexity_analysis = self._analyze_pr_complexity(pr_details)
            
            # Analyze code changes with advanced metrics
            code_analysis = await self._analyze_code_changes(pr_details, agent_id=agent_id, task_id=task_id)
            
            # Assess impact and risk
            impact_assessment = self._assess_pr_impact(pr_details, code_analysis)
            
            # Generate review comments with AI
            review_comments = await self._generate_review_comments(code_analysis, complexity_analysis, agent_id=agent_id, task_id=task_id)
            
            # Calculate overall review score
            review_score = self._calculate_review_score(complexity_analysis, code_analysis, impact_assessment)
            
            review_time = time.time() - start_time
            
            return {
                "status": "success",
                "message": "Comprehensive PR review completed",
                "review_timestamp": datetime.now().isoformat(),
                "review_time_mins": round(review_time / 60, 2),
                "pr_metadata": {
                    "url": pr_url,
                    "repository": repository,
                    "branch": branch,
                    "files_changed": pr_details.get("files_changed", 0),
                    "lines_added": pr_details.get("lines_added", 0),
                    "lines_deleted": pr_details.get("lines_deleted", 0)
                },
                "complexity_analysis": complexity_analysis,
                "impact_assessment": impact_assessment,
                "review_score": review_score,
                "review": {
                    "summary": review_comments["summary"],
                    "suggestions": review_comments["suggestions"],
                    "security_issues": review_comments["security_issues"],
                    "performance_issues": review_comments["performance_issues"],
                    "best_practices": review_comments.get("best_practices", []),
                    "testing_recommendations": review_comments.get("testing_recommendations", [])
                },
                "recommendations": {
                    "approve": review_score["overall_score"] >= 80,
                    "request_changes": review_score["overall_score"] < 60,
                    "merge_confidence": review_score["merge_confidence"],
                    "estimated_review_time": f"{max(15, complexity_analysis['complexity_score'] * 2)} minutes"
                }
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Error reviewing PR: {str(e)}",
                "review_timestamp": datetime.now().isoformat()
            }
    
    def _analyze_pr_complexity(self, pr_details: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze PR complexity using multiple metrics."""
        files_changed = pr_details.get("files_changed", 5)
        lines_added = pr_details.get("lines_added", 150)
        lines_deleted = pr_details.get("lines_deleted", 75)
        
        # Calculate complexity factors
        size_factor = min(100, (files_changed * 10 + lines_added * 0.1 + lines_deleted * 0.05))
        
        # Estimate cyclomatic complexity based on code patterns
        estimated_complexity = self._estimate_cyclomatic_complexity(pr_details.get("diff_content", ""))
        
        # Calculate weighted complexity score
        complexity_score = (
            files_changed * self.complexity_weights["files_changed"] * 10 +
            lines_added * self.complexity_weights["lines_added"] * 0.1 +
            lines_deleted * self.complexity_weights["lines_deleted"] * 0.1 +
            estimated_complexity * self.complexity_weights["cyclomatic_complexity"]
        )
        
        # Normalize to 0-100 scale
        normalized_score = min(100, complexity_score)
        
        # Determine complexity level
        if normalized_score < 20:
            level, grade = "Low", "A"
        elif normalized_score < 40:
            level, grade = "Medium", "B"
        elif normalized_score < 60:
            level, grade = "High", "C"
        elif normalized_score < 80:
            level, grade = "Very High", "D"
        else:
            level, grade = "Critical", "F"
        
        return {
            "complexity_score": round(normalized_score, 1),
            "complexity_level": level,
            "complexity_grade": grade,
            "size_metrics": {
                "files_changed": files_changed,
                "lines_added": lines_added,
                "lines_deleted": lines_deleted,
                "net_lines": lines_added - lines_deleted
            },
            "estimated_cyclomatic_complexity": estimated_complexity,
            "review_difficulty": "Easy" if normalized_score < 30 else "Medium" if normalized_score < 60 else "Hard",
            "factors": {
                "file_count_impact": files_changed > 10,
                "large_additions": lines_added > 200,
                "major_deletions": lines_deleted > 100,
                "complex_logic": estimated_complexity > 15
            }
        }
    
    def _estimate_cyclomatic_complexity(self, diff_content: str) -> int:
        """Estimate cyclomatic complexity from diff content."""
        if not diff_content:
            # Mock complexity for demo
            return 12
        
        complexity_patterns = [
            r'\bif\b', r'\belse\b', r'\belif\b',
            r'\bfor\b', r'\bwhile\b',
            r'\btry\b', r'\bexcept\b',
            r'\band\b', r'\bor\b',
            r'\?\s*:', r'case\s+',
            r'switch\s*\(', r'catch\s*\('
        ]
        
        complexity = 1  # Base complexity
        for pattern in complexity_patterns:
            complexity += len(re.findall(pattern, diff_content, re.IGNORECASE))
        
        return min(50, complexity)  # Cap at 50 for reasonableness
    
    def _assess_pr_impact(self, pr_details: Dict[str, Any], code_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Assess the impact and risk of the pull request."""
        # Analyze file types and changes
        files_changed = pr_details.get("files_changed", 5)
        lines_added = pr_details.get("lines_added", 150)
        
        # Determine change categories (mock analysis for demo)
        change_categories = []
        if "test" in str(pr_details).lower():
            change_categories.append("tests")
        if "fix" in str(pr_details).lower() or "bug" in str(pr_details).lower():
            change_categories.append("bug_fixes")
        if "add" in str(pr_details).lower() or "feature" in str(pr_details).lower():
            change_categories.append("feature_additions")
        if "refactor" in str(pr_details).lower():
            change_categories.append("refactoring")
        if "doc" in str(pr_details).lower():
            change_categories.append("documentation")
        if not change_categories:
            change_categories.append("feature_additions")  # Default
        
        # Calculate impact score
        impact_score = 0
        for category in change_categories:
            if category in self.impact_categories:
                weight = self.impact_categories[category]["weight"]
                impact_score += weight * min(1.0, files_changed / 10)
        
        impact_score = min(100, impact_score * 100)
        
        # Determine risk level
        risk_factors = []
        if files_changed > 15:
            risk_factors.append("High file change count")
        if lines_added > 300:
            risk_factors.append("Large code additions")
        if "breaking" in str(pr_details).lower():
            risk_factors.append("Potential breaking changes")
        
        risk_level = "High" if len(risk_factors) > 1 else "Medium" if risk_factors else "Low"
        
        return {
            "impact_score": round(impact_score, 1),
            "change_categories": change_categories,
            "risk_level": risk_level,
            "risk_factors": risk_factors,
            "business_impact": "High" if impact_score > 70 else "Medium" if impact_score > 40 else "Low",
            "deployment_risk": risk_level,
            "rollback_difficulty": "Easy" if files_changed < 5 else "Medium" if files_changed < 15 else "Hard",
            "estimated_testing_time": f"{max(30, files_changed * 5)} minutes"
        }
    
    def _calculate_review_score(self, complexity_analysis: Dict[str, Any], code_analysis: Dict[str, Any], impact_assessment: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate overall review score and recommendations."""
        complexity_score = complexity_analysis["complexity_score"]
        impact_score = impact_assessment["impact_score"]
        
        # Calculate overall score (inverse of complexity, positive impact)
        overall_score = max(0, 100 - (complexity_score * 0.6) + (impact_score * 0.2))
        overall_score = min(100, overall_score)
        
        # Determine merge confidence
        if overall_score >= 85:
            merge_confidence = "High"
            recommendation = "Approve"
        elif overall_score >= 70:
            merge_confidence = "Medium"
            recommendation = "Approve with minor comments"
        elif overall_score >= 55:
            merge_confidence = "Low"
            recommendation = "Request changes"
        else:
            merge_confidence = "Very Low"
            recommendation = "Reject - significant issues"
        
        return {
            "overall_score": round(overall_score, 1),
            "merge_confidence": merge_confidence,
            "recommendation": recommendation,
            "score_breakdown": {
                "complexity_impact": round(complexity_score * -0.6, 1),
                "positive_impact": round(impact_score * 0.2, 1),
                "base_score": 100
            },
            "quality_indicators": {
                "code_quality": "Good" if complexity_score < 50 else "Needs Improvement",
                "test_coverage": "Adequate" if "test" in str(impact_assessment).lower() else "Insufficient",
                "documentation": "Present" if "doc" in str(impact_assessment).lower() else "Missing"
            }
        }

    async def _fetch_pr_details(self, pr_url: str) -> Dict[str, Any]:
        """
        Fetch PR details from GitHub API.
        """
        # Parse PR URL to extract owner, repo, and PR number
        # Expected format: https://github.com/{owner}/{repo}/pull/{number}
        pattern = r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)"
        match = re.match(pattern, pr_url)
        
        if not match:
            raise ValueError(f"Invalid GitHub PR URL: {pr_url}")
            
        owner, repo, pr_number = match.groups()
        
        # GitHub API endpoints
        api_base = "https://api.github.com"
        pr_endpoint = f"{api_base}/repos/{owner}/{repo}/pulls/{pr_number}"
        files_endpoint = f"{api_base}/repos/{owner}/{repo}/pulls/{pr_number}/files"
        
        # Set up headers with GitHub token if available
        headers = {}
        github_token = os.getenv("GITHUB_TOKEN")
        if github_token:
            headers["Authorization"] = f"token {github_token}"
        
        async with httpx.AsyncClient() as client:
            # Fetch PR details
            pr_response = await client.get(pr_endpoint, headers=headers)
            if pr_response.status_code != 200:
                raise Exception(f"Failed to fetch PR details: {pr_response.status_code} {pr_response.text}")
                
            pr_data = pr_response.json()
            
            # Fetch PR files
            files_response = await client.get(files_endpoint, headers=headers)
            if files_response.status_code != 200:
                raise Exception(f"Failed to fetch PR files: {files_response.status_code} {files_response.text}")
                
            files_data = files_response.json()
        
        # Construct diff content
        diff_content = ""
        for file in files_data:
            diff_content += f"File: {file['filename']}\n"
            diff_content += f"Status: {file['status']}\n"
            diff_content += f"Changes: +{file['additions']} -{file['deletions']}\n"
            diff_content += f"Patch:\n{file.get('patch', 'No patch available')}\n\n"
        
        return {
            "title": pr_data["title"],
            "description": pr_data["body"] or "",
            "author": pr_data["user"]["login"],
            "branch": pr_data["head"]["ref"],
            "base_branch": pr_data["base"]["ref"],
            "diff": diff_content,
            "files_changed": [file["filename"] for file in files_data],
            "url": pr_url
        }

    async def _analyze_code_changes(self, pr_details: Dict[str, Any], agent_id: int, task_id: int) -> Dict[str, Any]:
        """
        Analyze code changes using AI models.
        """
        # Use centralized AI service
        analysis_prompt = f"""
        Analyze the following code changes and provide detailed feedback:
        {pr_details.get('diff', '')}
        
        Focus on:
        1. Code quality and best practices
        2. Potential bugs or issues
        3. Security concerns
        4. Performance implications
        5. Documentation needs
        """
        
        try:
            response = await self.ai_service.generate_text(
                prompt=analysis_prompt,
                agent_id=agent_id,
                task_id=task_id,
                max_tokens=1000,
                temperature=0.1
            )
            
            return {
                "analysis": response['content'],
                "raw_changes": pr_details.get('diff', '')
            }
        except Exception as e:
            print(f"Error analyzing code changes: {str(e)}")
            return {
                "analysis": "Basic analysis: Code changes detected. Manual review recommended.",
                "raw_changes": pr_details.get('diff', '')
            }

    async def _generate_review_comments(self, analysis: Dict[str, Any], complexity_analysis: Dict[str, Any], agent_id: int, task_id: int) -> Dict[str, Any]:
        """
        Generate review comments based on code analysis.
        """
        # Use AI for generating review comments
        review_prompt = f"""
        Based on the following code analysis, generate a structured PR review:
        {analysis['analysis']}
        
        Format the review as:
        1. Summary of changes
        2. Specific suggestions for improvement
        3. Security concerns
        4. Performance considerations
        """
        
        try:
            response = await self.ai_service.generate_text(
                prompt=review_prompt,
                agent_id=agent_id,
                task_id=task_id,
                max_tokens=1500,
                temperature=0.7
            )
            
            # Parse the response content
            content = response['content']
        except Exception as e:
            print(f"Error generating review comments: {str(e)}")
            content = "Basic review: Please manually review the changes for quality, security, and performance considerations."
        
        # Extract different sections from the response
        suggestions = self._extract_suggestions(content)
        security_issues = self._extract_security_issues(content)
        performance_issues = self._extract_performance_issues(content)
        
        return {
            "summary": content,
            "suggestions": suggestions,
            "security_issues": security_issues,
            "performance_issues": performance_issues
        }
    
    def _extract_suggestions(self, content: str) -> List[Dict[str, str]]:
        """Extract suggestions for improvement from the review content."""
        suggestions = []
        
        # Look for sections that might contain suggestions
        suggestion_patterns = [
            r"(?:Specific suggestions for improvement|Suggestions|Improvements):[\s\S]*?(?=\n\d+\.|$)",
            r"\d+\.\s+([^\n]+)(?:[\s\S]*?)(?=\d+\.|$)"
        ]
        
        for pattern in suggestion_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the suggestion text
                suggestion_text = match.strip()
                if suggestion_text and len(suggestion_text) > 10:  # Avoid empty or very short matches
                    # Try to identify the file it relates to
                    file_match = re.search(r"(?:in|file|path)\s+['\"]?([\w\./]+\.[\w]+)['\"]?", suggestion_text)
                    file_path = file_match.group(1) if file_match else ""
                    
                    suggestions.append({
                        "text": suggestion_text,
                        "file": file_path,
                        "type": "improvement"
                    })
        
        return suggestions
    
    def _extract_security_issues(self, content: str) -> List[Dict[str, str]]:
        """Extract security issues from the review content."""
        security_issues = []
        
        # Look for sections that might contain security issues
        security_patterns = [
            r"(?:Security concerns|Security issues|Security vulnerabilities):[\s\S]*?(?=\n\d+\.|$)",
            r"(?:security|vulnerability|exploit|injection|XSS|CSRF|authentication|authorization|encryption)([^\n.]+\.[^\n]+)"
        ]
        
        for pattern in security_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the issue text
                issue_text = match.strip()
                if issue_text and len(issue_text) > 10:  # Avoid empty or very short matches
                    # Try to identify the file it relates to
                    file_match = re.search(r"(?:in|file|path)\s+['\"]?([\w\./]+\.[\w]+)['\"]?", issue_text)
                    file_path = file_match.group(1) if file_match else ""
                    
                    security_issues.append({
                        "text": issue_text,
                        "file": file_path,
                        "severity": self._determine_severity(issue_text)
                    })
        
        return security_issues
    
    def _extract_performance_issues(self, content: str) -> List[Dict[str, str]]:
        """Extract performance issues from the review content."""
        performance_issues = []
        
        # Look for sections that might contain performance issues
        performance_patterns = [
            r"(?:Performance considerations|Performance issues|Performance optimizations):[\s\S]*?(?=\n\d+\.|$)",
            r"(?:performance|slow|optimization|efficient|complexity|O\([^)]+\)|memory|CPU|resource)([^\n.]+\.[^\n]+)"
        ]
        
        for pattern in performance_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                # Clean up the issue text
                issue_text = match.strip()
                if issue_text and len(issue_text) > 10:  # Avoid empty or very short matches
                    # Try to identify the file it relates to
                    file_match = re.search(r"(?:in|file|path)\s+['\"](\w\./]+\.[\w]+)['\"]?", issue_text)
                    file_path = file_match.group(1) if file_match else ""
                    
                    performance_issues.append({
                        "text": issue_text,
                        "file": file_path,
                        "impact": self._determine_impact(issue_text)
                    })
        
        return performance_issues
    
    def _determine_severity(self, text: str) -> str:
        """Determine the severity of a security issue based on its description."""
        high_keywords = ["critical", "severe", "high", "major", "important", "vulnerability", "exploit", "injection", "authentication"]
        medium_keywords = ["moderate", "medium", "warning", "potential", "possible"]
        
        text_lower = text.lower()
        
        for keyword in high_keywords:
            if keyword in text_lower:
                return "high"
                
        for keyword in medium_keywords:
            if keyword in text_lower:
                return "medium"
                
        return "low"
    
    def _determine_impact(self, text: str) -> str:
        """Determine the impact of a performance issue based on its description."""
        high_keywords = ["significant", "severe", "high", "major", "critical", "O(n²)", "O(n³)", "exponential"]
        medium_keywords = ["moderate", "medium", "noticeable", "O(n log n)", "could be improved"]
        
        text_lower = text.lower()
        
        for keyword in high_keywords:
            if keyword in text_lower:
                return "high"
                
        for keyword in medium_keywords:
            if keyword in text_lower:
                return "medium"
                
        return "low"