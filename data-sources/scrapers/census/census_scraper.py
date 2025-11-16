"""
U.S. Census Bureau data scraper.

Collects demographic and socioeconomic data from Census API.
"""

import requests
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class CensusScraper:
    """Scraper for U.S. Census Bureau data."""

    BASE_URL = "https://api.census.gov/data"

    def __init__(self, api_key: str, year: int = 2021):
        """
        Initialize Census scraper.

        Args:
            api_key: Census API key
            year: Data year (default: 2021 for ACS 5-year)
        """
        self.api_key = api_key
        self.year = year
        self.session = requests.Session()

    def get_demographics(
        self,
        geography: str,
        state: Optional[str] = None,
        county: Optional[str] = None,
        tract: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get demographic data for a geography.

        Args:
            geography: Geography type (state, county, tract, etc.)
            state: State FIPS code (2 digits)
            county: County FIPS code (3 digits)
            tract: Tract code (6 digits)

        Returns:
            Dict of demographic variables

        Example:
            >>> scraper = CensusScraper(api_key="...")
            >>> data = scraper.get_demographics(
            ...     geography="county",
            ...     state="25",
            ...     county="025"
            ... )
        """
        logger.info(f"Fetching demographics for {geography} {state}-{county}")

        # Define variables to fetch
        variables = [
            "S1701_C03_001E",  # Poverty rate
            "S1901_C01_012E",  # Median household income
            "DP05_0001E",      # Total population
            "DP05_0037PE",     # Percent Black/African American
            "DP05_0071PE",     # Percent Hispanic/Latino
            "DP04_0089E",      # Median home value
            "S1501_C02_014E",  # Percent bachelor's degree or higher
        ]

        # Construct geography parameter
        if geography == "county" and state and county:
            geo_param = f"for=county:{county}&in=state:{state}"
        elif geography == "tract" and state and county and tract:
            geo_param = f"for=tract:{tract}&in=state:{state}&in=county:{county}"
        elif geography == "state" and state:
            geo_param = f"for=state:{state}"
        else:
            raise ValueError(f"Invalid geography parameters")

        # Make API request
        url = f"{self.BASE_URL}/{self.year}/acs/acs5/subject"
        params = {
            "get": ",".join(variables),
            "key": self.api_key,
        }
        url_with_geo = f"{url}?{params}&{geo_param}"

        try:
            response = self.session.get(url, params=params + geo_param)
            response.raise_for_status()
            data = response.json()

            # Parse response (first row is headers, second is data)
            headers = data[0]
            values = data[1] if len(data) > 1 else []

            result = {
                "geography_type": geography,
                "state": state,
                "county": county,
                "tract": tract,
                "data_year": self.year,
                "fetched_at": datetime.utcnow().isoformat(),
                "poverty_rate": float(values[0]) if values else None,
                "median_income": float(values[1]) if values else None,
                "total_population": int(values[2]) if values else None,
                "percent_black": float(values[3]) if values else None,
                "percent_hispanic": float(values[4]) if values else None,
                "median_home_value": float(values[5]) if values else None,
                "percent_college_educated": float(values[6]) if values else None,
            }

            logger.info(f"Successfully fetched demographics")
            return result

        except requests.RequestException as e:
            logger.error(f"Failed to fetch Census data: {e}")
            raise

    def get_housing_data(
        self,
        geography: str,
        state: str,
        county: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get housing characteristics data.

        Args:
            geography: Geography type
            state: State FIPS code
            county: County FIPS code

        Returns:
            Dict of housing variables
        """
        logger.info(f"Fetching housing data for {geography} {state}-{county}")

        variables = [
            "DP04_0002PE",  # Percent owner-occupied
            "DP04_0003PE",  # Percent renter-occupied
            "DP04_0046PE",  # Percent lacking complete plumbing
            "DP04_0047PE",  # Percent lacking complete kitchen
            "DP04_0058E",   # Median year structure built
            "DP04_0134E",   # Median gross rent
        ]

        # TODO: Implement similar to get_demographics
        # Placeholder for now
        return {
            "geography_type": geography,
            "state": state,
            "county": county,
            "housing_data": "TODO"
        }
