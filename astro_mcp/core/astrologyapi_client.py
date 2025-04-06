import requests
from typing import Dict, Any, List
from datetime import datetime
from .models import NatalChart, PlanetaryPosition, Aspect, ZodiacSign, House, Planet
import base64
import socket
import urllib3
import time
import json
import sys

class AstrologyAPIClient:
    def __init__(self, user_id: str, api_key: str):
        self.user_id = user_id
        self.api_key = api_key
        self.base_url = "https://json.astrologyapi.com/v1"
        self.domain = "astrologycontext.in"  # Add domain configuration
        self.max_retries = 3
        self.retry_delay = 2  # seconds
        
        # Disable SSL verification warnings
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Add CORS headers
        self.headers = {
            "authorization": f"Basic {base64.b64encode(f'{self.user_id}:{self.api_key}'.encode()).decode()}",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
            "Access-Control-Allow-Origin": f"https://{self.domain}",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization"
        }
        
    def _test_connection(self, host: str, port: int = 443) -> bool:
        """Test if we can connect to a host on a specific port."""
        try:
            socket.create_connection((host, port), timeout=5)
            return True
        except (socket.timeout, socket.error):
            return False
            
    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Make a request to AstrologyAPI."""
        url = f"{self.base_url}/{endpoint}"
        
        # Create Basic Auth header
        auth_string = f"{self.user_id}:{self.api_key}"
        auth_bytes = auth_string.encode('ascii')
        base64_auth = base64.b64encode(auth_bytes).decode('ascii')
        auth_header = f"Basic {base64_auth}"
        
        headers = {
            "authorization": auth_header,
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        # Convert params to form data
        form_data = {k: str(v) for k, v in params.items()}
        
        for attempt in range(self.max_retries):
            try:
                print(f"\nAttempt {attempt + 1}:")
                print(f"URL: {url}")
                print(f"Headers: {headers}")
                print(f"Auth: Basic {self.user_id}:***")
                print(f"Request Data: {form_data}")
                
                # First test connection
                if not self._test_connection("json.astrologyapi.com"):
                    print("Direct connection failed, trying with requests...")
                    # Try a simple GET request to test connectivity
                    test_response = requests.get(
                        "https://json.astrologyapi.com",
                        timeout=5,
                        verify=False
                    )
                    if test_response.status_code != 200:
                        raise ConnectionError("Cannot connect to AstrologyAPI server")
                
                response = requests.post(
                    url,
                    headers=headers,
                    data=form_data,
                    timeout=10,
                    verify=False  # Disable SSL verification
                )
                
                print(f"Response Status: {response.status_code}")
                print(f"Response Headers: {dict(response.headers)}")
                print(f"Response Content: {response.text}")
                
                if response.status_code == 401:
                    raise ValueError(
                        "Authentication failed. Please check:\n"
                        f"1. User ID: {self.user_id}\n"
                        "2. API Key: [hidden]\n"
                        "3. Account status"
                    )
                elif response.status_code == 405:
                    raise ValueError(
                        "Invalid API endpoint or method. Please check:\n"
                        f"1. Endpoint URL: {url}\n"
                        "2. Request method: POST\n"
                        "3. API documentation\n"
                        f"4. Response: {response.text}"
                    )
                
                response.raise_for_status()
                return response.json()
                
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {str(e)}")
                
                if attempt < self.max_retries - 1:
                    print(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                    continue
                
                if isinstance(e, requests.exceptions.ConnectionError):
                    raise ConnectionError(
                        "Could not connect to AstrologyAPI. Please check:\n"
                        "1. Your internet connection\n"
                        "2. If you can access https://json.astrologyapi.com\n"
                        "3. If you're behind a corporate network or VPN\n"
                        "4. Try using a different DNS server (e.g., 8.8.8.8 or 1.1.1.1)\n"
                        "5. Check your firewall settings"
                    )
                elif isinstance(e, requests.exceptions.Timeout):
                    raise ConnectionError(
                        "Request timed out. Please try again in a few minutes."
                    )
                else:
                    raise ConnectionError(f"Error: {str(e)}")
    
    def get_birth_details(self, 
                         birth_time: datetime,
                         latitude: float,
                         longitude: float,
                         timezone: str = "UTC") -> Dict[str, Any]:
        """Get basic birth details."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("birth_details", params)
    
    def get_astro_details(self,
                         birth_time: datetime,
                         latitude: float,
                         longitude: float,
                         timezone: str = "UTC") -> Dict[str, Any]:
        """Get astrological details."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("astro_details", params)
    
    def get_planets(self,
                   birth_time: datetime,
                   latitude: float,
                   longitude: float,
                   timezone: str = "UTC") -> Dict[str, Any]:
        """Get planetary positions."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("planets", params)
    
    def get_ghat_chakra(self,
                       birth_time: datetime,
                       latitude: float,
                       longitude: float,
                       timezone: str = "UTC") -> Dict[str, Any]:
        """Get Ghat Chakra details."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("ghat_chakra", params)
    
    def get_horo_chart(self,
                      birth_time: datetime,
                      latitude: float,
                      longitude: float,
                      chart_type: str = "D1",
                      timezone: str = "UTC") -> Dict[str, Any]:
        """Get horoscope chart data."""
        if chart_type not in ["D1", "D9"]:
            raise ValueError("Chart type must be either D1 or D9")
            
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request(f"horo_chart/{chart_type}", params)
    
    def get_horo_chart_image(self,
                           birth_time: datetime,
                           latitude: float,
                           longitude: float,
                           chart_type: str = "D1",
                           timezone: str = "UTC") -> Dict[str, Any]:
        """Get horoscope chart image."""
        if chart_type not in ["D1", "D9"]:
            raise ValueError("Chart type must be either D1 or D9")
            
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request(f"horo_chart_image/{chart_type}", params)
    
    def get_current_vdasha(self,
                         birth_time: datetime,
                         latitude: float,
                         longitude: float,
                         timezone: str = "UTC") -> Dict[str, Any]:
        """Get current Vimshottari Dasha."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("current_vdasha", params)
    
    def get_kalsarpa_details(self,
                           birth_time: datetime,
                           latitude: float,
                           longitude: float,
                           timezone: str = "UTC") -> Dict[str, Any]:
        """Get Kalsarpa Dosha details."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("kalsarpa_details", params)
    
    def get_numero_table(self,
                        birth_time: datetime,
                        latitude: float,
                        longitude: float,
                        timezone: str = "UTC") -> Dict[str, Any]:
        """Get numerology table."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("numero_table", params)
    
    def get_basic_panchang(self,
                          birth_time: datetime,
                          latitude: float,
                          longitude: float,
                          timezone: str = "UTC") -> Dict[str, Any]:
        """Get basic Panchang details."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("basic_panchang", params)
    
    def get_general_ascendant_report(self,
                                   birth_time: datetime,
                                   latitude: float,
                                   longitude: float,
                                   timezone: str = "UTC") -> Dict[str, Any]:
        """Get general ascendant report."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        return self._make_request("general_ascendant_report", params)
    
    def get_geo_details(self,
                       latitude: float,
                       longitude: float) -> Dict[str, Any]:
        """Get geographical details."""
        params = {
            "lat": latitude,
            "lon": longitude
        }
        return self._make_request("geo_details", params)
    
    def get_timezone_with_dst(self,
                            latitude: float,
                            longitude: float) -> Dict[str, Any]:
        """Get timezone with DST details."""
        params = {
            "lat": latitude,
            "lon": longitude
        }
        return self._make_request("timezone_with_dst", params)
    
    def get_timezone(self,
                    latitude: float,
                    longitude: float) -> Dict[str, Any]:
        """Get timezone details."""
        params = {
            "lat": latitude,
            "lon": longitude
        }
        return self._make_request("timezone", params)
    
    def get_natal_chart(self, 
                       birth_time: datetime,
                       latitude: float,
                       longitude: float,
                       timezone: str = "UTC") -> NatalChart:
        """Get natal chart data from AstrologyAPI."""
        # Convert timezone string to number (e.g., "UTC" -> 0, "UTC+5:30" -> 5.5)
        tz_offset = 0.0
        if timezone != "UTC":
            # Handle timezone strings like "UTC+5:30" or "UTC-5:30"
            tz_str = timezone.replace("UTC", "").strip()
            if tz_str:
                sign = -1 if tz_str[0] == '-' else 1
                tz_str = tz_str[1:] if tz_str[0] in ['+', '-'] else tz_str
                hours, minutes = map(float, tz_str.split(':'))
                tz_offset = sign * (hours + minutes/60)
        
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": tz_offset  # Send as number
        }
        
        # Get birth details
        birth_response = self._make_request("birth_details", params)
        print("Birth Details Response:", birth_response)
        
        # Get basic panchang details if available
        try:
            panchang_response = self._make_request("basic_panchang", params)
            print("Panchang Response:", panchang_response)
        except Exception as e:
            print(f"Could not get panchang details: {str(e)}")
            panchang_response = None
        
        # Convert AstrologyAPI response to our NatalChart model
        planetary_positions = []
        aspects = []
        
        # For Basic Plan, we'll use default values since we don't have access to detailed astrological data
        ascendant_sign = ZodiacSign.ARIES
        midheaven_sign = ZodiacSign.CAPRICORN
        
        # Create additional context dictionary
        additional_context = {}
        
        # Add birth details to additional context
        if isinstance(birth_response, dict):
            additional_context['birth_details'] = birth_response
        
        # Add panchang details to additional context
        if panchang_response and isinstance(panchang_response, dict):
            additional_context['panchang'] = panchang_response
        
        return NatalChart(
            birth_time=birth_time,
            birth_location={"latitude": latitude, "longitude": longitude},
            planetary_positions=planetary_positions,
            aspects=aspects,
            ascendant=ascendant_sign,
            midheaven=midheaven_sign,
            additional_context=additional_context  # Include the additional context
        )
    
    def get_basic_interpretation(self,
                               birth_time: datetime,
                               latitude: float,
                               longitude: float,
                               timezone: str = "UTC") -> Dict[str, Any]:
        """Get basic astrological interpretation using available endpoints."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": timezone
        }
        
        interpretation = {}
        
        # Get birth details
        try:
            birth_response = self._make_request("birth_details", params)
            if isinstance(birth_response, dict):
                interpretation["birth_details"] = birth_response
        except Exception as e:
            print(f"Could not get birth details: {str(e)}")
        
        # Get basic panchang if available
        try:
            panchang_response = self._make_request("basic_panchang", params)
            if isinstance(panchang_response, dict):
                interpretation["panchang"] = panchang_response
        except Exception as e:
            print(f"Could not get panchang details: {str(e)}")
        
        # Get general ascendant report if available
        try:
            ascendant_response = self._make_request("general_ascendant_report", params)
            if isinstance(ascendant_response, dict):
                interpretation["ascendant_report"] = ascendant_response
        except Exception as e:
            print(f"Could not get ascendant report: {str(e)}")
        
        return interpretation
    
    def get_nakshatra_details(self,
                            birth_time: datetime,
                            latitude: float,
                            longitude: float) -> Dict[str, Any]:
        """Get Nakshatra details."""
        params = {
            "day": birth_time.day,
            "month": birth_time.month,
            "year": birth_time.year,
            "hour": birth_time.hour,
            "min": birth_time.minute,
            "lat": latitude,
            "lon": longitude,
            "tzone": "UTC"
        }
        
        return self._make_request("nakshatra_details", params) 