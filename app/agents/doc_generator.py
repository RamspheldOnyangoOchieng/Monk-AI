from typing import Dict, Any, List
import os
import re
from sqlalchemy.orm import Session
from app.core.ai_service import AIService
from app.core.database import SessionLocal

class DocGenerator:
    def __init__(self, db_session: Session = None):
        """Initialize the DocGenerator agent."""
        self.db_session = db_session or SessionLocal()
        self.ai_service = AIService(session=self.db_session)

    async def generate_docs(self, code: str, language: str, context: str = None, agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """
        Generate documentation for the provided code.
        """
        try:
            # Analyze code structure
            code_analysis = await self._analyze_code(code, language, agent_id=agent_id, task_id=task_id)
            
            # Generate documentation
            documentation = await self._generate_documentation(code_analysis, context, agent_id=agent_id, task_id=task_id)
            
            return {
                "status": "success",
                "documentation": {
                    "overview": documentation["overview"],
                    "functions": documentation["functions"],
                    "classes": documentation["classes"],
                    "examples": documentation["examples"]
                }
            }
        except Exception as e:
            raise Exception(f"Error generating documentation: {str(e)}")

    async def _analyze_code(self, code: str, language: str, agent_id: int, task_id: int) -> Dict[str, Any]:
        """
        Analyze the code structure and identify key components.
        """
        # Use centralized AI service
        try:
            analysis_prompt = f"""
            Analyze the following {language} code and identify:
            1. Functions and their purposes
            2. Classes and their methods
            3. Key algorithms and data structures
            4. Dependencies and imports
            5. Main entry points
            
            Code:
            {code}
            """
            
            ai_result = await self.ai_service.generate_text(
                prompt=analysis_prompt,
                agent_id=agent_id,
                task_id=task_id,
                max_tokens=1000,
                temperature=0.3
            )

            return {
                "analysis": ai_result['content'],
                "raw_code": code
            }
        except Exception as e:
            # Re-raise exception to be handled by the main generate_docs function
            raise Exception(f"Error analyzing code: {str(e)}")

    async def _generate_documentation(self, analysis: Dict[str, Any], context: str = None, agent_id: int = 1, task_id: int = 1) -> Dict[str, Any]:
        """
        Generate comprehensive documentation based on code analysis.
        """
        # Use centralized AI service
        try:
            doc_prompt = f"""
            Generate comprehensive documentation based on the following code analysis:
            {analysis['analysis']}
            
            Additional context: {context if context else 'None provided'}
            
            Format the documentation as:
            1. Overview and purpose
            2. Function documentation (parameters, return values, examples)
            3. Class documentation (properties, methods, inheritance)
            4. Usage examples
            5. Best practices and notes
            """
            
            ai_result = await self.ai_service.generate_text(
                prompt=doc_prompt,
                agent_id=agent_id,
                task_id=task_id,
                max_tokens=2000,
                temperature=0.7
            )
            
            content = ai_result['content']
            
            # Extract different sections from the response
            overview = self._extract_overview(content)
            functions = self._extract_functions(content)
            classes = self._extract_classes(content)
            examples = self._extract_examples(content)
            
            return {
                "overview": overview,
                "functions": functions,
                "classes": classes,
                "examples": examples
            }
        except Exception as e:
            # Re-raise exception to be handled by the main generate_docs function
            raise Exception(f"Error generating documentation content: {str(e)}")
    
    def _extract_overview(self, content: str) -> str:
        """Extract the overview section from the documentation content."""
        # Look for sections that might contain overview information
        overview_patterns = [
            r"(?:Overview|Introduction|Summary|Description):\s*([\s\S]*?)(?=\n##|\n#|$)",
            r"^([\s\S]*?)(?=\n##|\n#|$)"
        ]
        
        for pattern in overview_patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
            if match:
                overview_text = match.group(1).strip()
                if overview_text:
                    return overview_text
        
        # If no specific overview section found, return the first paragraph
        paragraphs = content.split('\n\n')
        if paragraphs:
            return paragraphs[0].strip()
        
        return ""
    
    def _extract_functions(self, content: str) -> List[Dict[str, str]]:
        """Extract function documentation from the content."""
        functions = []
        
        # Look for function documentation sections
        # Pattern to match function headers with or without markdown formatting
        function_patterns = [
            r"###\s*(?:Function|Method):\s*`?([\w_]+)`?\s*(?:\(([^)]*)\))?[\s\S]*?(?=###|##|#|$)",
            r"(?:Function|Method):\s*`?([\w_]+)`?\s*(?:\(([^)]*)\))?[\s\S]*?(?=Function|Method|$)",
            r"```\w*\s*def\s+([\w_]+)\s*\(([^)]*)\)[^{]*(?:{[^}]*})?:\s*([\s\S]*?)```"
        ]
        
        for pattern in function_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                function_name = match.group(1).strip()
                
                # Extract parameters if available
                params = match.group(2).strip() if len(match.groups()) > 1 and match.group(2) else ""
                
                # Extract the full function documentation
                full_match = match.group(0).strip()
                
                # Try to extract description
                description_match = re.search(r"(?:Description|Summary):\s*([\s\S]*?)(?=Parameters|Returns|Example|```|$)", full_match, re.IGNORECASE)
                description = description_match.group(1).strip() if description_match else ""
                
                # Try to extract return value
                returns_match = re.search(r"(?:Returns|Return value):\s*([\s\S]*?)(?=Example|```|$)", full_match, re.IGNORECASE)
                returns = returns_match.group(1).strip() if returns_match else ""
                
                functions.append({
                    "name": function_name,
                    "params": params,
                    "description": description,
                    "returns": returns,
                    "full_doc": full_match
                })
        
        return functions
    
    def _extract_classes(self, content: str) -> List[Dict[str, str]]:
        """Extract class documentation from the content."""
        classes = []
        
        # Look for class documentation sections
        class_patterns = [
            r"###\s*Class:\s*`?([\w_]+)`?[\s\S]*?(?=###|##|#|$)",
            r"(?:Class):\s*`?([\w_]+)`?[\s\S]*?(?=Class|$)",
            r"```\w*\s*class\s+([\w_]+)(?:\([^)]*\))?:\s*([\s\S]*?)```"
        ]
        
        for pattern in class_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                class_name = match.group(1).strip()
                
                # Extract the full class documentation
                full_match = match.group(0).strip()
                
                # Try to extract description
                description_match = re.search(r"(?:Description|Summary):\s*([\s\S]*?)(?=Methods|Attributes|Example|```|$)", full_match, re.IGNORECASE)
                description = description_match.group(1).strip() if description_match else ""
                
                # Try to extract methods
                methods = []
                method_matches = re.finditer(r"(?:Method|Function):\s*`?([\w_]+)`?\s*(?:\(([^)]*)\))?[\s\S]*?(?=Method|Function|$)", full_match, re.IGNORECASE)
                for method_match in method_matches:
                    method_name = method_match.group(1).strip()
                    method_params = method_match.group(2).strip() if len(method_match.groups()) > 1 and method_match.group(2) else ""
                    methods.append({
                        "name": method_name,
                        "params": method_params
                    })
                
                classes.append({
                    "name": class_name,
                    "description": description,
                    "methods": methods,
                    "full_doc": full_match
                })
        
        return classes
    
    def _extract_examples(self, content: str) -> List[Dict[str, str]]:
        """Extract code examples from the content."""
        examples = []
        
        # Look for code examples
        example_patterns = [
            r"###\s*(?:Example|Usage)[\s\S]*?```([\w]*)\s*([\s\S]*?)```",
            r"(?:Example|Usage):[\s\S]*?```([\w]*)\s*([\s\S]*?)```",
            r"```([\w]*)\s*([\s\S]*?)```"
        ]
        
        for pattern in example_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                language = match.group(1).strip() if match.group(1) else "python"
                code = match.group(2).strip()
                
                # Try to extract description before the code block
                description = ""
                if match.start() > 0:
                    prev_text = content[:match.start()].strip()
                    last_paragraph = prev_text.split('\n\n')[-1]
                    if "example" in last_paragraph.lower() or "usage" in last_paragraph.lower():
                        description = last_paragraph
                
                examples.append({
                    "language": language,
                    "code": code,
                    "description": description
                })
        
        return examples
