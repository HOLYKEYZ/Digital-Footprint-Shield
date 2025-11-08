"""
API Key Manager for Digital Footprint Shield.
Manages API key rotation, rate limiting, and quota handling.
"""

import json
import os
from typing import List, Dict, Optional, Tuple
from utils.display import print_warning, print_danger, print_info


class APIKeyManager:
    """Manages API key pools with rotation and error handling."""
    
    def __init__(self, keys_file: str = "keys.json"):
        """
        Initialize the API key manager.
        
        Args:
            keys_file: Path to the JSON file containing API keys
        """
        self.keys_file = keys_file
        self.keys_data = {}
        self.current_key_indices = {}  # Track current key index for each service
        self.failed_keys = {}  # Track failed keys (rate limited, quota exceeded)
        self.load_keys()
    
    def load_keys(self) -> bool:
        """
        Load API keys from the keys.json file.
        
        Returns:
            True if keys loaded successfully, False otherwise
        """
        keys_path = os.path.join(os.path.dirname(__file__), self.keys_file)
        
        # Try to load from current directory first
        if not os.path.exists(keys_path):
            keys_path = self.keys_file
        
        if not os.path.exists(keys_path):
            print_warning(f"⚠️  Keys file not found: {keys_path}")
            print_info("💡 Creating default keys.json file...")
            self._create_default_keys_file(keys_path)
            return False
        
        try:
            with open(keys_path, 'r') as f:
                self.keys_data = json.load(f)
            
            # Initialize current key indices for each service
            for service in self.keys_data.keys():
                self.current_key_indices[service] = 0
                self.failed_keys[service] = set()
            
            print_info(f"✅ Loaded API keys from {keys_path}")
            return True
        
        except json.JSONDecodeError as e:
            print_danger(f"❌ Error parsing keys.json: {str(e)}")
            return False
        except Exception as e:
            print_danger(f"❌ Error loading keys.json: {str(e)}")
            return False
    
    def _create_default_keys_file(self, keys_path: str):
        """Create a default keys.json file."""
        default_keys = {
            "google_custom_search": {
                "api_keys": [
                    {
                        "key": "YOUR_API_KEY_HERE",
                        "enabled": True,
                        "description": "Google Custom Search API key"
                    }
                ],
                "search_engine_id": "YOUR_SEARCH_ENGINE_ID_HERE"
            },
            "hibp": {
                "api_keys": [
                    {
                        "key": "",
                        "enabled": False,
                        "description": "Optional HIBP API key"
                    }
                ]
            },
            "grok": {
                "api_keys": [
                    {
                        "key": "",
                        "enabled": False,
                        "description": "Optional Grok API key"
                    }
                ]
            }
        }
        
        try:
            with open(keys_path, 'w') as f:
                json.dump(default_keys, f, indent=2)
            print_info(f"✅ Created default keys.json at {keys_path}")
        except Exception as e:
            print_danger(f"❌ Error creating keys.json: {str(e)}")
    
    def get_api_key(self, service: str) -> Optional[str]:
        """
        Get the next available API key for a service.
        
        Args:
            service: Service name (e.g., 'google_custom_search', 'hibp', 'grok')
        
        Returns:
            API key string, or None if no keys available
        """
        if service not in self.keys_data:
            print_warning(f"⚠️  Service '{service}' not found in keys.json")
            return None
        
        service_data = self.keys_data[service]
        api_keys = service_data.get('api_keys', [])
        
        if not api_keys:
            print_warning(f"⚠️  No API keys configured for service '{service}'")
            return None
        
        # Find next available key
        enabled_keys = [
            (i, key_data) for i, key_data in enumerate(api_keys)
            if key_data.get('enabled', True) and 
               key_data.get('key', '').strip() and
               key_data.get('key', '') != 'YOUR_API_KEY_HERE' and
               i not in self.failed_keys.get(service, set())
        ]
        
        if not enabled_keys:
            # All keys exhausted, reset failed keys and try again
            if self.failed_keys.get(service):
                print_warning(f"⚠️  All keys for '{service}' exhausted. Resetting failed keys...")
                self.failed_keys[service] = set()
                enabled_keys = [
                    (i, key_data) for i, key_data in enumerate(api_keys)
                    if key_data.get('enabled', True) and 
                       key_data.get('key', '').strip() and
                       key_data.get('key', '') != 'YOUR_API_KEY_HERE'
                ]
        
        if not enabled_keys:
            print_danger(f"❌ No available API keys for service '{service}'")
            return None
        
        # Get current index or start from 0
        current_idx = self.current_key_indices.get(service, 0)
        
        # Find next available key starting from current index
        for i in range(len(enabled_keys)):
            idx = (current_idx + i) % len(enabled_keys)
            key_index, key_data = enabled_keys[idx]
            
            # Return this key and update index
            self.current_key_indices[service] = (idx + 1) % len(enabled_keys)
            return key_data.get('key')
        
        return None
    
    def mark_key_failed(self, service: str, key: str):
        """
        Mark an API key as failed (rate limited or quota exceeded).
        
        Args:
            service: Service name
            key: The API key that failed
        """
        if service not in self.keys_data:
            return
        
        api_keys = self.keys_data[service].get('api_keys', [])
        for i, key_data in enumerate(api_keys):
            if key_data.get('key') == key:
                self.failed_keys.setdefault(service, set()).add(i)
                print_warning(f"⚠️  Marked key {i+1} for '{service}' as failed (rate limited/quota exceeded)")
                break
    
    def reset_failed_keys(self, service: str):
        """
        Reset failed keys for a service (useful after some time).
        
        Args:
            service: Service name
        """
        if service in self.failed_keys:
            self.failed_keys[service] = set()
            print_info(f"✅ Reset failed keys for '{service}'")
    
    def get_search_engine_id(self) -> Optional[str]:
        """
        Get the Google Custom Search Engine ID.
        
        Returns:
            Search Engine ID string, or None if not configured
        """
        if 'google_custom_search' not in self.keys_data:
            return None
        
        return self.keys_data['google_custom_search'].get('search_engine_id')
    
    def get_available_key_count(self, service: str) -> int:
        """
        Get the number of available API keys for a service.
        
        Args:
            service: Service name
        
        Returns:
            Number of available keys
        """
        if service not in self.keys_data:
            return 0
        
        api_keys = self.keys_data[service].get('api_keys', [])
        enabled_keys = [
            key_data for key_data in api_keys
            if key_data.get('enabled', True) and 
               key_data.get('key', '').strip() and
               key_data.get('key', '') != 'YOUR_API_KEY_HERE'
        ]
        
        return len(enabled_keys)
    
    def get_next_key_with_retry(self, service: str, max_retries: int = None) -> Optional[str]:
        """
        Get the next API key, automatically rotating through the pool.
        This is the main function to use for getting an API key.
        
        Args:
            service: Service name
            max_retries: Maximum number of keys to try (None = try all)
        
        Returns:
            API key string, or None if all keys exhausted
        """
        if max_retries is None:
            max_retries = self.get_available_key_count(service)
        
        tried_keys = set()
        for _ in range(max_retries):
            key = self.get_api_key(service)
            if key is None:
                break
            
            # Avoid infinite loop if we've tried all keys
            if key in tried_keys:
                break
            
            tried_keys.add(key)
            return key
        
        return None


def get_api_key_for_search(api_key_manager: APIKeyManager) -> Tuple[Optional[str], Optional[str]]:
    """
    Get an API key and Search Engine ID for Google Custom Search.
    Modular function for getting API credentials.
    
    Args:
        api_key_manager: APIKeyManager instance
    
    Returns:
        Tuple of (api_key, search_engine_id)
    """
    api_key = api_key_manager.get_next_key_with_retry('google_custom_search')
    search_engine_id = api_key_manager.get_search_engine_id()
    
    return api_key, search_engine_id

