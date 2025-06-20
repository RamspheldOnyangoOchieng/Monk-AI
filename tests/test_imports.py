#!/usr/bin/env python3
"""
Test script to check if all imports work correctly
"""

try:
    print("Testing imports...")
    
    # Test basic FastAPI import
    from fastapi import FastAPI
    print("✅ FastAPI import successful")
    
    # Test agent imports
    from app.agents.code_optimizer import CodeOptimizer
    print("✅ CodeOptimizer import successful")
    
    from app.agents.doc_generator import DocGenerator
    print("✅ DocGenerator import successful")
    
    from app.agents.ideation import Ideation
    print("✅ Ideation import successful")
    
    from app.agents.orchestrator import AgentOrchestrator
    print("✅ AgentOrchestrator import successful")
    
    from app.agents.pr_reviewer import PRReviewer
    print("✅ PRReviewer import successful")
    
    from app.agents.security_analyzer import SecurityAnalyzer
    print("✅ SecurityAnalyzer import successful")
    
    from app.agents.test_generator import TestGenerator
    print("✅ TestGenerator import successful")
    
    # Test API router import
    from app.api.api import api_router
    print("✅ API router import successful")
    
    print("\n🎉 All imports successful!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc() 