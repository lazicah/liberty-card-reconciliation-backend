#!/usr/bin/env python3
"""
Test script to verify environment configuration.
Run this before deploying to verify everything is set up correctly.
"""

import os
import json
import base64
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

# Load .env if it exists
load_dotenv()


def print_header(text):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_warning(text):
    """Print warning message."""
    print(f"⚠️  {text}")


def print_error(text):
    """Print error message."""
    print(f"❌ {text}")


def test_openai():
    """Test OpenAI configuration."""
    print_header("Testing OpenAI Configuration")
    
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    
    if not api_key:
        print_warning("OPENAI_API_KEY is not set")
        return False
    
    if api_key == "your_openai_api_key_here" or api_key.startswith("sk-"):
        if len(api_key) > 20:
            print_success(f"OPENAI_API_KEY is configured (key starts with: {api_key[:10]}...)")
            return True
        else:
            print_error("OPENAI_API_KEY appears to be invalid")
            return False
    else:
        print_warning("OPENAI_API_KEY is set but may be invalid")
        return api_key != "your_openai_api_key_here"


def test_spreadsheet_id():
    """Test Google Sheets configuration."""
    print_header("Testing Google Sheets Configuration")
    
    sheet_id = os.getenv("SPREADSHEET_ID", "").strip()
    
    if not sheet_id:
        print_error("SPREADSHEET_ID is not set")
        return False
    
    if sheet_id == "1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI":
        print_success(f"SPREADSHEET_ID is set: {sheet_id[:30]}...")
        return True
    elif len(sheet_id) > 20:
        print_success(f"SPREADSHEET_ID is configured: {sheet_id[:30]}...")
        return True
    else:
        print_error(f"SPREADSHEET_ID appears invalid: {sheet_id}")
        return False


def test_google_credentials():
    """Test Google credentials in priority order."""
    print_header("Testing Google Credentials")
    
    # Check Base64
    base64_creds = os.getenv("GOOGLE_CREDENTIALS_BASE64", "").strip()
    if base64_creds:
        print("Found GOOGLE_CREDENTIALS_BASE64 (Method 1)...")
        try:
            decoded = base64.b64decode(base64_creds).decode('utf-8')
            creds_dict = json.loads(decoded)
            
            if "type" in creds_dict and creds_dict["type"] == "service_account":
                project_id = creds_dict.get("project_id", "unknown")
                print_success(f"✓ Valid Base64 encoded service account (Project: {project_id})")
                return True
            else:
                print_error("Base64 decodes to JSON but doesn't look like service account")
                return False
        except base64.binascii.Error:
            print_error("GOOGLE_CREDENTIALS_BASE64 is not valid Base64")
            return False
        except json.JSONDecodeError:
            print_error("GOOGLE_CREDENTIALS_BASE64 doesn't decode to valid JSON")
            return False
        except Exception as e:
            print_error(f"Error parsing GOOGLE_CREDENTIALS_BASE64: {e}")
            return False
    
    # Check JSON String
    json_creds = os.getenv("GOOGLE_CREDENTIALS_JSON", "").strip()
    if json_creds:
        print("Found GOOGLE_CREDENTIALS_JSON (Method 2)...")
        try:
            creds_dict = json.loads(json_creds)
            if "type" in creds_dict and creds_dict["type"] == "service_account":
                project_id = creds_dict.get("project_id", "unknown")
                print_success(f"✓ Valid JSON service account (Project: {project_id})")
                return True
            else:
                print_error("JSON doesn't look like service account")
                return False
        except json.JSONDecodeError as e:
            print_error(f"GOOGLE_CREDENTIALS_JSON is not valid JSON: {e}")
            return False
    
    # Check File Path
    file_path = os.getenv("SERVICE_ACCOUNT_FILE", "").strip()
    if file_path:
        print(f"Found SERVICE_ACCOUNT_FILE (Method 3): {file_path}...")
        if Path(file_path).exists():
            try:
                with open(file_path) as f:
                    creds_dict = json.load(f)
                
                if "type" in creds_dict and creds_dict["type"] == "service_account":
                    project_id = creds_dict.get("project_id", "unknown")
                    print_success(f"✓ Valid service account file (Project: {project_id})")
                    return True
                else:
                    print_error("File doesn't look like service account")
                    return False
            except json.JSONDecodeError:
                print_error(f"'{file_path}' is not valid JSON")
                return False
            except Exception as e:
                print_error(f"Error reading '{file_path}': {e}")
                return False
        else:
            print_warning(f"SERVICE_ACCOUNT_FILE path set but file not found: {file_path}")
            return False
    
    # No credentials found
    print_error("No Google credentials found!")
    print("\nPlease set ONE of these:")
    print("  1. GOOGLE_CREDENTIALS_BASE64 (recommended)")
    print("  2. GOOGLE_CREDENTIALS_JSON")
    print("  3. SERVICE_ACCOUNT_FILE")
    print("\nSee ENVIRONMENT_SETUP.md for instructions")
    return False


def test_api_configuration():
    """Test API configuration."""
    print_header("Testing API Configuration")
    
    api_host = os.getenv("API_HOST", "0.0.0.0")
    api_port = os.getenv("API_PORT", "8000")
    api_reload = os.getenv("API_RELOAD", "true").lower() == "true"
    
    print_success(f"API_HOST: {api_host}")
    print_success(f"API_PORT: {api_port}")
    print_success(f"API_RELOAD: {api_reload}")
    
    return True


def test_imports():
    """Test Python imports."""
    print_header("Testing Python Imports")
    
    imports = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("pandas", "Pandas"),
        ("gspread", "Google Sheets client"),
        ("google.oauth2", "Google Auth"),
        ("dotenv", "Python-dotenv"),
        ("openai", "OpenAI"),
        ("pydantic", "Pydantic"),
    ]
    
    all_ok = True
    for module_name, display_name in imports:
        try:
            __import__(module_name)
            print_success(f"{display_name} ({module_name})")
        except ImportError:
            print_error(f"{display_name} ({module_name}) - NOT INSTALLED")
            all_ok = False
    
    if not all_ok:
        print("\n⚠️  Install missing packages:")
        print("   pip install -r requirements.txt")
    
    return all_ok


def test_config_module():
    """Test if config module works."""
    print_header("Testing Config Module")
    
    try:
        from config import settings
        print_success("config.py loaded successfully")
        
        # Try to get Google credentials
        try:
            creds = settings.get_google_credentials()
            project_id = creds.get("project_id", "unknown")
            print_success(f"Google credentials accessible (Project: {project_id})")
            return True
        except RuntimeError as e:
            print_error(f"Cannot get Google credentials: {e}")
            return False
    except Exception as e:
        print_error(f"Error loading config.py: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("  Liberty Card Reconciliation API - Setup Verification")
    print("="*60)
    
    results = {
        "Python Imports": test_imports(),
        "OpenAI Config": test_openai(),
        "Spreadsheet ID": test_spreadsheet_id(),
        "Google Credentials": test_google_credentials(),
        "API Configuration": test_api_configuration(),
        "Config Module": test_config_module(),
    }
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\n{passed}/{total} tests passed")
    
    if passed == total:
        print_success("\n🎉 All tests passed! Your setup is ready.")
        print("\nYou can now start the API:")
        print("  python main.py")
        print("\nOr using the start script:")
        print("  ./start.sh")
        return 0
    else:
        print_warning(f"\n⚠️  {total - passed} test(s) failed. See details above.")
        print("\nNext steps:")
        print("1. Review the errors above")
        print("2. Follow instructions in ENVIRONMENT_SETUP.md")
        print("3. Run this test again to verify fixes")
        return 1


if __name__ == "__main__":
    sys.exit(main())
