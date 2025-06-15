import re
import os
import json
import asyncio
import time
import ast
import httpx
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict
from sqlalchemy.orm import Session
from app.core.ai_service import AIService
from app.core.database import SessionLocal
import logging

logger = logging.getLogger(__name__)

class CodeOptimizer:
    """Advanced Agent for analyzing code and providing optimization suggestions with performance metrics."""
    
    def __init__(self, db_session: Session = None):
        """Initialize the CodeOptimizer agent."""
        self.db_session = db_session or SessionLocal()
        self.ai_service = AIService(session=self.db_session)
        
        # Enhanced optimization categories with scoring
        self.categories = {
            "performance": {"weight": 0.3, "description": "Runtime efficiency and speed"},
            "memory_usage": {"weight": 0.25, "description": "Memory allocation and usage"},
            "code_quality": {"weight": 0.2, "description": "Readability and maintainability"},
            "algorithm_complexity": {"weight": 0.15, "description": "Big O complexity analysis"},
            "resource_utilization": {"weight": 0.1, "description": "CPU and I/O efficiency"}
        }
        
        # Performance improvement benchmarks for demo
        self.benchmark_improvements = {
            "python": {"avg_speedup": 2.3, "memory_reduction": 18},
            "javascript": {"avg_speedup": 1.8, "memory_reduction": 15},
            "java": {"avg_speedup": 2.1, "memory_reduction": 22},
            "typescript": {"avg_speedup": 1.9, "memory_reduction": 16},
            "go": {"avg_speedup": 1.6, "memory_reduction": 12},
        }
    
    async def analyze_file_and_get_optimizations(self, file_path: str, file_content: str, agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """
        Analyzes a single file and returns optimization suggestions.
        """
        language = self._detect_language(file_path)
        prompt = self._construct_optimization_prompt(file_content, language)
        
        try:
            ai_result = await self.ai_service.generate_text(
                prompt=prompt,
                agent_id=agent_id,
                task_id=task_id,
                temperature=0.2,
                max_tokens=2000
            )
            
            response_content = ai_result.get("content", "")
            
            try:
                # Assuming the AI returns a JSON string with suggestions
                optimizations = json.loads(response_content)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from AI response for {file_path}. Using raw content.")
                optimizations = {"raw_suggestions": response_content}

            # Post-process and add metadata
            optimizations["file_path"] = file_path
            optimizations["language"] = language
            
            return optimizations

        except Exception as e:
            logger.error(f"Error getting optimizations for {file_path}: {e}", exc_info=True)
            return {
                "error": f"Failed to get AI optimizations: {e}",
                "file_path": file_path,
                "language": language
            }

    def _construct_optimization_prompt(self, code: str, language: str) -> str:
        """Construct the optimization prompt for the AI."""
        # Implementation of _construct_optimization_prompt method
        # This method should return a properly formatted prompt string
        # based on the code and language.
        # For now, we'll return a placeholder string.
        return "Placeholder prompt"

    def _detect_language(self, file_path: str) -> str:
        """Detect the programming language of the code."""
        # Implementation of _detect_language method
        # This method should return the detected programming language
        # based on the file path.
        # For now, we'll return a placeholder string.
        return "Placeholder language"

    def _analyze_code_complexity(self, code: str, language: str) -> Dict[str, Any]:
        """Analyze code complexity and generate metrics."""
        metrics = {
            "lines_of_code": len(code.splitlines()),
            "character_count": len(code),
            "estimated_cyclomatic_complexity": "Medium",
            "function_count": 0,
            "class_count": 0,
            "complexity_score": 0,
        }
        
        # Language-specific analysis
        if language.lower() == "python":
            try:
                tree = ast.parse(code)
                metrics["function_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)])
                metrics["class_count"] = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
            except:
                pass
        
        # Simple heuristic complexity scoring
        complexity_indicators = [
            code.count("for "), code.count("while "), code.count("if "),
            code.count("elif "), code.count("else:"), code.count("try:"),
            code.count("except"), code.count("with "), code.count("def ")
        ]
        
        metrics["complexity_score"] = min(sum(complexity_indicators) * 2, 100)
        
        if metrics["complexity_score"] < 20:
            metrics["estimated_cyclomatic_complexity"] = "Low"
        elif metrics["complexity_score"] < 50:
            metrics["estimated_cyclomatic_complexity"] = "Medium"
        else:
            metrics["estimated_cyclomatic_complexity"] = "High"
            
        return metrics
    
    def _calculate_optimization_score(self, optimizations: Dict[str, List], focus_areas: List[str]) -> Dict[str, Any]:
        """Calculate weighted optimization score based on found issues."""
        total_score = 0
        category_scores = {}
        
        for category in focus_areas:
            if category in optimizations and category in self.categories:
                issue_count = len(optimizations[category])
                weight = self.categories[category]["weight"]
                # Score: 100 - (issues * 10), weighted by category importance
                category_score = max(0, 100 - (issue_count * 10))
                category_scores[category] = category_score
                total_score += category_score * weight
        
        return {
            "overall_score": round(total_score, 1),
            "category_scores": category_scores,
            "grade": self._get_optimization_grade(total_score),
            "improvement_potential": round(100 - total_score, 1)
        }
    
    def _get_optimization_grade(self, score: float) -> str:
        """Convert numerical score to letter grade."""
        if score >= 90: return "A+"
        elif score >= 85: return "A"
        elif score >= 80: return "B+"
        elif score >= 75: return "B"
        elif score >= 70: return "C+"
        elif score >= 65: return "C"
        elif score >= 60: return "D"
        else: return "F"
    
    def _generate_performance_projections(self, language: str, optimization_score: Dict[str, Any]) -> Dict[str, Any]:
        """Generate realistic performance improvement projections."""
        lang_key = language.lower()
        base_improvements = self.benchmark_improvements.get(lang_key, {"avg_speedup": 2.0, "memory_reduction": 15})
        
        # Adjust projections based on optimization score
        improvement_factor = (100 - optimization_score["overall_score"]) / 100
        
        return {
            "estimated_speedup": round(1 + (base_improvements["avg_speedup"] - 1) * improvement_factor, 1),
            "memory_reduction": round(base_improvements["memory_reduction"] * improvement_factor),
            "confidence_level": "High" if improvement_factor > 0.3 else "Medium" if improvement_factor > 0.1 else "Low",
            "optimization_impact": {
                "performance": f"{round(improvement_factor * 100)}% improvement potential",
                "maintainability": "Enhanced" if improvement_factor > 0.2 else "Maintained",
                "scalability": "Improved" if improvement_factor > 0.25 else "Maintained"
            }
        }
    
    def _count_critical_issues(self, optimizations: Dict[str, List]) -> int:
        """Count critical optimization issues."""
        critical_keywords = ["memory leak", "performance bottleneck", "inefficient", "O(n²)", "blocking"]
        critical_count = 0
        
        for category, issues in optimizations.items():
            for issue in issues:
                issue_text = str(issue).lower()
                if any(keyword in issue_text for keyword in critical_keywords):
                    critical_count += 1
        
        return critical_count
        
    def _generate_optimization_prompt(self, code: str, language: str, focus_areas: List[str], complexity_metrics: Dict[str, Any]) -> str:
        focus_areas_str = ", ".join(focus_areas)
        
        prompt = f"""Analyze the following {language} code and provide detailed optimization suggestions. 
        Focus on these areas: {focus_areas_str}.
        
        For each suggestion:
        1. Identify the specific code section that can be optimized
        2. Explain why it's suboptimal
        3. Provide a specific, implementable improvement
        4. Quantify the expected benefit where possible
        
        Format your response with clear sections for each optimization category.
        Include code examples for before and after implementation.
        
        **Code Complexity Metrics:**
        Lines of Code: {complexity_metrics["lines_of_code"]}
        Character Count: {complexity_metrics["character_count"]}
        Estimated Cyclomatic Complexity: {complexity_metrics["estimated_cyclomatic_complexity"]}
        Function Count: {complexity_metrics["function_count"]}
        Class Count: {complexity_metrics["class_count"]}
        Complexity Score: {complexity_metrics["complexity_score"]}
        
        **Code to Analyze:**
        ```{language}
        {code}
        ```
        """.replace('{language}', language)
        
        return prompt
    
    def _parse_optimization_response(self, content: str) -> Dict[str, Any]:
        """Parse the AI's optimization response into a structured format."""
        optimizations = defaultdict(list)
        
        # Extract summary (first paragraph)
        summary_match = re.search(r'^(.*?)\n\n', content, re.DOTALL)
        if summary_match:
            optimizations["summary"] = summary_match.group(1).strip()
        
        # Extract performance optimizations
        optimizations["performance_optimizations"] = self._extract_optimizations(
            content, r'## Performance Optimizations\n\n(.*?)(?:\n##|$)', 'performance'
        )
        
        # Extract memory optimizations
        optimizations["memory_optimizations"] = self._extract_optimizations(
            content, r'## Memory Usage Optimizations\n\n(.*?)(?:\n##|$)', 'memory'
        )
        
        # Extract code quality improvements
        optimizations["code_quality_improvements"] = self._extract_optimizations(
            content, r'## Code Quality Improvements\n\n(.*?)(?:\n##|$)', 'quality'
        )
        
        # Extract algorithm improvements
        optimizations["algorithm_improvements"] = self._extract_optimizations(
            content, r'## Algorithm Complexity\n\n(.*?)(?:\n##|$)', 'algorithm'
        )
        
        # Extract resource optimizations
        optimizations["resource_optimizations"] = self._extract_optimizations(
            content, r'## Resource Utilization\n\n(.*?)(?:\n##|$)', 'resource'
        )
        
        return optimizations
    
    def _extract_optimizations(self, content: str, pattern: str, category: str) -> List[Dict[str, str]]:
        """Extract optimization suggestions for a specific category.
        
        Args:
            content: The AI-generated content
            pattern: Regex pattern to extract the category section
            category: The optimization category name
            
        Returns:
            List of optimization suggestions for the category
        """
        optimizations = []
        
        # Extract the section for this category
        section_match = re.search(pattern, content, re.DOTALL)
        if not section_match:
            return optimizations
            
        section_content = section_match.group(1)
        
        # Extract individual optimization items
        optimization_items = re.split(r'### \d+\.\s+', section_content)
        if optimization_items and not optimization_items[0].strip():
            optimization_items = optimization_items[1:]
            
        for item in optimization_items:
            if not item.strip():
                continue
                
            optimization = {
                "title": "",
                "description": "",
                "original_code": "",
                "optimized_code": "",
                "benefit": "",
                "category": category
            }
            
            # Extract title
            title_match = re.match(r'^([^\n]+)', item)
            if title_match:
                optimization["title"] = title_match.group(1).strip()
                
            # Extract original code
            original_code_match = re.search(r'\*\*Original Code:\*\*\s*```[^\n]*\n(.+?)```', item, re.DOTALL)
            if original_code_match:
                optimization["original_code"] = original_code_match.group(1).strip()
                
            # Extract optimized code
            optimized_code_match = re.search(r'\*\*Suggested Optimization:\*\*\s*```[^\n]*\n(.+?)```', item, re.DOTALL)
            if optimized_code_match:
                optimization["optimized_code"] = optimized_code_match.group(1).strip()
                
            # Extract benefit
            benefit_match = re.search(r'\*\*Benefit:\*\*\s*([^\n]+)', item)
            if benefit_match:
                optimization["benefit"] = benefit_match.group(1).strip()
                
            # Extract description (everything between title and Original Code)
            description_match = re.search(r'^[^\n]+\n\n(.*?)\n\n\*\*Original Code:', item, re.DOTALL)
            if description_match:
                optimization["description"] = description_match.group(1).strip()
            else:
                # If no description found between title and Original Code, use everything before Original Code
                description_match = re.search(r'^[^\n]+\n\n(.*?)\*\*Original Code:', item, re.DOTALL)
                if description_match:
                    optimization["description"] = description_match.group(1).strip()
            
            optimizations.append(optimization)
            
        return optimizations