#!/usr/bin/env python3
"""
Simple test script to verify CloseAI API configuration
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from utils import openai_api_key, openai_api_base
    import openai
    
    # Configure API
    openai.api_key = openai_api_key
    openai.api_base = openai_api_base
    
    print("🔧 CloseAI API Configuration Test")
    print("=" * 50)
    print(f"API Base URL: {openai_api_base}")
    print(f"API Key: {openai_api_key[:20]}..." if openai_api_key else "API Key: Not set")
    print()
    
    # Test a simple ChatGPT request
    print("🧪 Testing API Connection...")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Say hello in one sentence."}],
            max_tokens=50
        )
        response = completion["choices"][0]["message"]["content"]
        print(f"✅ API Test Successful!")
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"❌ API Test Failed: {str(e)}")
        sys.exit(1)
    
    print("\n🎉 Configuration is working correctly!")
    print("You can now run the generative agents simulation.")
    
except ImportError as e:
    print(f"❌ Import Error: {str(e)}")
    print("Make sure utils.py is properly configured in the same directory.")
    sys.exit(1)
except Exception as e:
    print(f"❌ Configuration Error: {str(e)}")
    sys.exit(1)