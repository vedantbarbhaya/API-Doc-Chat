# backend/app/api_validator/validator.py
import re
import json
import httpx
from typing import Dict, List, Optional
from ..utils.logger import logger


class APIValidator:
    def __init__(self):
        self.api_base_url = "https://api.crustdata.com"
        self.test_token = "test_token"  # For validation only

    def extract_api_calls(self, response: str) -> List[Dict]:
        """Extract API calls from a response string"""
        # Look for curl commands in the response
        curl_pattern = r"```(?:bash|shell)?\s*curl[^`]+```"
        matches = re.finditer(curl_pattern, response, re.MULTILINE | re.DOTALL)

        api_calls = []
        for match in matches:
            curl_command = match.group(0).strip('`').strip()
            try:
                api_call = self.parse_curl_command(curl_command)
                api_calls.append(api_call)
            except Exception as e:
                logger.error(f"Error parsing curl command: {e}")

        return api_calls

    def parse_curl_command(self, curl_command: str) -> Dict:
        """Parse curl command into components"""
        # Extract URL
        url_match = re.search(r"'(https?://[^']+)'", curl_command)
        url = url_match.group(1) if url_match else None

        # Extract headers
        headers = {}
        header_matches = re.finditer(r"--header\s+'([^']+)'", curl_command)
        for match in header_matches:
            try:
                key, value = match.group(1).split(':', 1)
                headers[key.strip()] = value.strip()
            except ValueError:
                continue

        # Extract data
        data_match = re.search(r"--data\s+'({[^']+})'", curl_command)
        data = json.loads(data_match.group(1)) if data_match else None

        return {
            "url": url,
            "headers": headers,
            "data": data
        }

    async def validate_api_call(self, api_call: Dict) -> Dict:
        """Validate an API call and return validation results"""
        validation_results = {
            "is_valid": True,
            "errors": [],
            "fixes": []
        }

        try:
            # Validate region values if present
            if api_call.get("data", {}).get("filters"):
                for filter_item in api_call["data"]["filters"]:
                    if filter_item.get("filter_type") == "REGION":
                        await self.validate_region_values(filter_item, validation_results)

            # Validate headers
            self.validate_headers(api_call["headers"], validation_results)

            # Validate URL
            self.validate_url(api_call["url"], validation_results)

        except Exception as e:
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Validation error: {str(e)}")

        return validation_results

    async def validate_region_values(self, filter_item: Dict, validation_results: Dict):
        """Validate region values against the allowed list"""
        try:
            # In real implementation, fetch from actual region list URL
            # For now, check basic format
            for value in filter_item.get("value", []):
                if not re.match(r"^[\w\s,]+$", value):
                    validation_results["is_valid"] = False
                    validation_results["errors"].append(
                        f"Invalid region format: {value}"
                    )
                    validation_results["fixes"].append(
                        "Use exact region names from the region list"
                    )
        except Exception as e:
            validation_results["errors"].append(f"Region validation error: {str(e)}")

    def validate_headers(self, headers: Dict, validation_results: Dict):
        """Validate required headers"""
        required_headers = {
            "Content-Type": "application/json",
            "Authorization": "Token"
        }

        for header, required_value in required_headers.items():
            if header not in headers:
                validation_results["is_valid"] = False
                validation_results["errors"].append(f"Missing required header: {header}")
                validation_results["fixes"].append(f"Add {header} header")
            elif required_value not in headers[header]:
                validation_results["is_valid"] = False
                validation_results["errors"].append(
                    f"Invalid {header} value: {headers[header]}"
                )
                validation_results["fixes"].append(
                    f"Use {required_value} in {header} header"
                )

    def validate_url(self, url: str, validation_results: Dict):
        """Validate API URL"""
        if not url.startswith(self.api_base_url):
            validation_results["is_valid"] = False
            validation_results["errors"].append(f"Invalid API URL: {url}")
            validation_results["fixes"].append(
                f"Use base URL: {self.api_base_url}"
            )