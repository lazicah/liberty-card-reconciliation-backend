"""
Configuration module for the Liberty Card Reconciliation API.
"""
import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    ai_model: str = "gpt-4"
    
    # Google Sheets Configuration
    service_account_file: str = os.getenv("SERVICE_ACCOUNT_FILE", "streamlit-analytics-488117-db0b145f8c2a.json")
    spreadsheet_id: str = os.getenv("SPREADSHEET_ID", "1La0dpzzo2yZQTOe3DJk11uapbgF4kk2fqQ6fblck8TI")
    
    # Google Sheets Tab Names
    sheet_card_transaction: str = "CardTransaction"
    sheet_nibss_settlement: str = "NIBSS SETT FROM NIBSS"
    sheet_isw_settlement: str = "ISW SETT REPORT"
    sheet_parallex_nibss: str = "LIBERTYPAY_Pos_Acquired_Detail_"
    sheet_bank_unity: str = "BANK STMT UNITY"
    sheet_bank_parallex: str = "BANK STMT PARALLEX"
    sheet_ai_summary: str = "AI Summary"
    
    # Google Scopes
    google_scopes: list = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # API Configuration
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_reload: bool = os.getenv("API_RELOAD", "true").lower() == "true"
    
    # Merchant IDs
    merchant_id_interswitch_unity: str = "2LBP87654321988"
    merchant_id_nibss_unity: str = "2215LA525653900"
    merchant_id_nibss_parallex: float = 210000000000000.0
    
    # Output paths
    output_dir: str = "outputs/metrics"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
