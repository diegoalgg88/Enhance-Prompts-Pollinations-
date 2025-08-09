import requests
import json
import time
import logging
from typing import Optional, Dict, Any

from config.config_manager import ConfigManager

class SecureAPIClient:
    """Secure API client that uses an externally loaded set of prompts."""

    def __init__(self, config: ConfigManager, logger: logging.Logger, prompts_data: Dict) -> None:
        """Initializes the API client.

        Args:
            config: The application's configuration manager.
            logger: The application's logger.
            prompts_data: The data for the prompts.
        """
        self.config = config
        self.logger = logger
        self.prompts_data = prompts_data
        self.base_url: str = config.get('API', 'base_url')
        self.endpoint: str = config.get('API', 'endpoint')
        self.timeout: int = config.getint('API', 'timeout', 30)
        self.max_retries: int = config.getint('API', 'max_retries', 3)
        self.validate_ssl: bool = config.getboolean('SECURITY', 'validate_ssl', True)
        self.last_request_time: float = 0
        self.rate_limit: int = config.getint('SECURITY', 'rate_limit', 10)
        self.min_interval: float = 60 / self.rate_limit if self.rate_limit > 0 else 0
        self.session: requests.Session = requests.Session()
        self.session.headers.update(
            {'Content-Type': 'application/json', 'User-Agent': 'PollinationsPromptEnhancer/2.5.0'})

    def _validate_input(self, prompt: str) -> bool:
        """Validates the user's input.

        Args:
            prompt: The user's input.

        Returns:
            True if the input is valid, False otherwise.
        """
        if not prompt or not prompt.strip():
            return False
        if len(prompt) > 15000:
            self.logger.warning(
                f"Prompt too long: {len(prompt)} characters")
            return False
        return True

    def _rate_limit_check(self) -> None:
        """Checks if the request is within the rate limit and waits if necessary."""
        if self.min_interval == 0:
            return
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        if time_since_last < self.min_interval:
            sleep_time = self.min_interval - time_since_last
            self.logger.info(
                f"Rate limiting: waiting {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def enhance_prompt(self, prompt: str, api_token: str, prompt_type: str) -> Dict[str, Any]:
        """Enhances the user's prompt using the Pollinations.ai API.

        Args:
            prompt: The user's prompt.
            api_token: The user's API token.
            prompt_type: The type of prompt to enhance.

        Returns:
            A dictionary with the enhanced prompt or an error message.
        """
        if not self._validate_input(prompt):
            return {'success': False, 'error': 'Invalid input prompt.', 'enhanced_prompt': None}
        if not api_token or not api_token.strip():
            return {'success': False, 'error': 'API token is not configured.', 'enhanced_prompt': None}

        self._rate_limit_check()

        system_prompt = self._get_system_prompt(prompt_type)
        if not system_prompt:
            return {'success': False, 'error': f"Prompt type '{prompt_type}' not found.", 'enhanced_prompt': None}

        url = f"{self.base_url}{self.endpoint}"
        headers = {'Authorization': f'Bearer {api_token.strip()}', **
                   self.session.headers}
        payload = {"model": "gpt-4", "messages": [{"role": "system", "content": system_prompt}, {
            "role": "user", "content": prompt.strip()}], "max_tokens": 1200, "temperature": 0.7}

        for attempt in range(self.max_retries):
            try:
                self.logger.info(
                    f"Making API request for type '{prompt_type}' (attempt {attempt + 1}/{self.max_retries})")
                response = self.session.post(
                    url, headers=headers, json=payload, timeout=self.timeout, verify=self.validate_ssl)
                response.raise_for_status()
                data = response.json()
                enhanced_prompt = data.get('choices', [{}])[0].get(
                    'message', {}).get('content', '').strip()
                if not enhanced_prompt:
                    return {'success': False, 'error': 'API returned an empty response.', 'enhanced_prompt': None}
                self.logger.info(
                    f"Prompt type '{prompt_type}' enhanced successfully")
                return {'success': True, 'error': None, 'enhanced_prompt': enhanced_prompt}
            except requests.exceptions.HTTPError as e:
                self.logger.error(
                    f"HTTP Error: {e.response.status_code} - {e.response.text}")
                if e.response.status_code == 401:
                    return {'success': False, 'error': 'Authentication failed. Check your API_TOKEN.', 'enhanced_prompt': None}
                if e.response.status_code == 429:
                    if attempt < self.max_retries - 1:
                        time.sleep(2 ** attempt)
                    continue
                return {'success': False, 'error': f'API request failed (Status: {e.response.status_code})', 'enhanced_prompt': None}
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Request Exception: {e}")
                if attempt < self.max_retries - 1:
                    continue
                return {'success': False, 'error': f'Connection failed: {e}', 'enhanced_prompt': None}
            except (json.JSONDecodeError, KeyError, IndexError) as e:
                self.logger.error(f"Error processing response: {e}")
                return {'success': False, 'error': 'Invalid response format from API.', 'enhanced_prompt': None}
        return {'success': False, 'error': f'Failed after {self.max_retries} attempts.', 'enhanced_prompt': None}

    def _get_system_prompt(self, prompt_type: str) -> Optional[str]:
        """Constructs the system prompt from the loaded data."""
        prompt_info = self.prompts_data.get(prompt_type)
        if not prompt_info:
            return None

        description = prompt_info.get("description", "")
        guidelines = prompt_info.get("guidelines", [])

        formatted_guidelines = "\n".join(f"- {line}" for line in guidelines)

        final_prompt = f"{description}\n\nGuidelines:{formatted_guidelines}\n\nTransform the following user prompt:"
        return final_prompt

    def __del__(self) -> None:
        if hasattr(self, 'session'):
            self.session.close()
