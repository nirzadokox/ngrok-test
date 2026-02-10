from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests

class FetchNgrokInput(BaseModel):
    """Input schema for Fetch Ngrok Tool."""
    url: str = Field(
        default="https://85e00b2844ad.ngrok.app",
        description="The ngrok endpoint URL to fetch data from"
    )

class FetchNgrokTool(BaseTool):
    """Tool for fetching data from ngrok endpoints with secure connections."""

    name: str = "fetch_ngrok"
    description: str = (
        "Fetches data from ngrok endpoints using secure HTTPS connections. "
        "Returns the HTTP status code and first 500 characters of the response body. "
        "Handles errors gracefully and returns formatted error messages."
    )
    args_schema: Type[BaseModel] = FetchNgrokInput

    def _run(self, url: str = "https://85e00b2844ad.ngrok.app") -> str:
        """
        Fetch data from the specified ngrok endpoint.
        
        Args:
            url: The ngrok endpoint URL to fetch data from
            
        Returns:
            A formatted string containing the status code and response body,
            or an error message if the request fails.
        """
        try:
            # Make GET request with 30-second timeout
            response = requests.get(
                url,
                timeout=30,
                verify=True  # Ensures SSL certificate verification
            )
            
            # Get status code
            status_code = response.status_code
            
            # Get response body text and limit to first 500 characters
            response_text = response.text
            body_preview = response_text[:500] if response_text else ""
            
            # Format and return the result
            return f"Status: {status_code}\nBody: {body_preview}"
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out after 30 seconds"
            
        except requests.exceptions.SSLError as e:
            return f"Error: SSL certificate error - {str(e)}"
            
        except requests.exceptions.ConnectionError as e:
            return f"Error: Connection error - {str(e)}"
            
        except requests.exceptions.HTTPError as e:
            return f"Error: HTTP error - {str(e)}"
            
        except requests.exceptions.RequestException as e:
            return f"Error: Request failed - {str(e)}"
            
        except Exception as e:
            return f"Error: Unexpected error - {str(e)}"