"""
CDC WONDER API Integration

This module provides integration with the CDC WONDER API for accessing vital statistics,
mortality, natality, and cancer data.

CDC WONDER API Documentation: https://wonder.cdc.gov/wonder/help/wonder-api.html

IMPORTANT LIMITATIONS:
- Only NATIONAL data available via API (no state/county filtering)
- Rate limit: 1 request per 2 minutes recommended
- Sequential queries only (no parallel requests)
- Must accept data use restrictions

Available Databases:
- D76: Detailed Mortality 1999-2013
- D77: Detailed Mortality 2013+
- D149: Natality (births) data
- D66: Cancer incidence
"""

import requests
import xml.etree.ElementTree as ET
import time
from typing import Dict, List, Optional, Union
from dataclasses import dataclass
from datetime import datetime
import os


@dataclass
class CDCWonderResult:
    """Represents a result from CDC WONDER API"""
    database_id: str
    query_date: datetime
    data: List[Dict[str, Union[str, int, float]]]
    footnotes: List[str]
    caveats: List[str]
    raw_xml: str


class CDCWonderAPI:
    """
    Client for CDC WONDER API.

    Rate Limiting:
    - CDC recommends 1 query per 2 minutes for system recovery
    - This class enforces rate limiting automatically
    """

    BASE_URL = "https://wonder.cdc.gov/controller/datarequest"

    # Database IDs
    DETAILED_MORTALITY_1999_2013 = "D76"
    DETAILED_MORTALITY_2013_PLUS = "D77"
    NATALITY = "D149"
    CANCER_INCIDENCE = "D66"

    def __init__(self, rate_limit_seconds: int = 120):
        """
        Initialize CDC WONDER API client.

        Args:
            rate_limit_seconds: Seconds to wait between requests (default 120)
        """
        self.session = requests.Session()
        self.rate_limit_seconds = rate_limit_seconds
        self.last_request_time = 0.0

    def _enforce_rate_limit(self):
        """Enforce rate limiting between requests"""
        elapsed = time.time() - self.last_request_time
        wait_time = self.rate_limit_seconds - elapsed

        if wait_time > 0:
            print(f"[Rate Limit] Waiting {wait_time:.1f} seconds before next request...")
            time.sleep(wait_time)

        self.last_request_time = time.time()

    def query(
        self,
        database_id: str,
        xml_request: str,
        accept_datause_restrictions: bool = True
    ) -> CDCWonderResult:
        """
        Execute a query against CDC WONDER API.

        Args:
            database_id: CDC WONDER database ID (e.g., "D76")
            xml_request: XML request string with query parameters
            accept_datause_restrictions: Must be True to comply with CDC policies

        Returns:
            CDCWonderResult object with parsed data

        Raises:
            ValueError: If data use restrictions not accepted
            requests.RequestException: If API request fails
        """
        if not accept_datause_restrictions:
            raise ValueError(
                "Must accept CDC data use restrictions. "
                "See: https://wonder.cdc.gov/datause.html"
            )

        # Ensure rate limit compliance
        self._enforce_rate_limit()

        # Build URL
        url = f"{self.BASE_URL}/{database_id}"

        # Make request
        print(f"[CDC WONDER] Querying database {database_id}...")

        try:
            response = self.session.post(
                url,
                data={
                    "request_xml": xml_request,
                    "accept_datause_restrictions": "true"
                },
                timeout=60
            )
            response.raise_for_status()

            # Parse response
            result = self._parse_response(database_id, response.content)

            print(f"[CDC WONDER] Query successful. Retrieved {len(result.data)} rows.")

            return result

        except requests.exceptions.RequestException as e:
            print(f"[ERROR] CDC WONDER API request failed: {e}")
            raise

    def _parse_response(self, database_id: str, xml_content: bytes) -> CDCWonderResult:
        """
        Parse XML response from CDC WONDER API.

        Args:
            database_id: Database ID
            xml_content: Raw XML response bytes

        Returns:
            CDCWonderResult object
        """
        root = ET.fromstring(xml_content)

        # Extract data rows
        data_rows = []
        for row in root.findall(".//r"):
            row_data = {}
            for cell in row.findall("c"):
                # Get column name and value
                col_name = cell.get("l", "unknown")
                col_value = cell.get("v", "")

                # Try to convert to appropriate type
                if col_value.replace(".", "", 1).isdigit():
                    col_value = float(col_value) if "." in col_value else int(col_value)

                row_data[col_name] = col_value

            data_rows.append(row_data)

        # Extract footnotes
        footnotes = []
        for footnote in root.findall(".//footnote"):
            footnotes.append(footnote.text or "")

        # Extract caveats
        caveats = []
        for caveat in root.findall(".//caveat"):
            caveats.append(caveat.text or "")

        return CDCWonderResult(
            database_id=database_id,
            query_date=datetime.now(),
            data=data_rows,
            footnotes=footnotes,
            caveats=caveats,
            raw_xml=xml_content.decode("utf-8")
        )

    def build_xml_request(self, parameters: Dict[str, str]) -> str:
        """
        Build XML request from parameter dictionary.

        Args:
            parameters: Dictionary of parameter names and values

        Returns:
            XML request string

        Example:
            parameters = {
                "B_1": "D76.V1-level1",  # Group by year
                "M_1": "D76.M1",         # Deaths measure
                "F_D76.V1": "2015 2016 2017",  # Year filter
                "V_D76.V2": "I00-I99"    # ICD-10 cardiovascular
            }
        """
        root = ET.Element("request-parameters")

        for name, value in parameters.items():
            param = ET.SubElement(root, "parameter")
            name_elem = ET.SubElement(param, "name")
            name_elem.text = name
            value_elem = ET.SubElement(param, "value")
            value_elem.text = str(value)

        return ET.tostring(root, encoding="unicode")


class MortalityQuery:
    """
    Helper class for constructing mortality database queries.

    Simplifies building queries for CDC WONDER Detailed Mortality databases.
    """

    def __init__(self, database_id: str = "D76"):
        """
        Initialize mortality query builder.

        Args:
            database_id: "D76" (1999-2013) or "D77" (2013+)
        """
        self.database_id = database_id
        self.parameters = {}

    def group_by_year(self) -> "MortalityQuery":
        """Group results by year"""
        self.parameters["B_1"] = f"{self.database_id}.V1-level1"
        return self

    def group_by_race(self) -> "MortalityQuery":
        """Group results by race"""
        next_b = len([k for k in self.parameters if k.startswith("B_")]) + 1
        self.parameters[f"B_{next_b}"] = f"{self.database_id}.V8"
        return self

    def group_by_age(self) -> "MortalityQuery":
        """Group results by age group"""
        next_b = len([k for k in self.parameters if k.startswith("B_")]) + 1
        self.parameters[f"B_{next_b}"] = f"{self.database_id}.V5"
        return self

    def filter_years(self, years: List[int]) -> "MortalityQuery":
        """
        Filter to specific years.

        Args:
            years: List of years (e.g., [2015, 2016, 2017])
        """
        self.parameters[f"F_{self.database_id}.V1"] = " ".join(map(str, years))
        self.parameters[f"I_{self.database_id}.V1"] = " ".join(
            [f"{y} ({y})" for y in years]
        )
        return self

    def filter_icd10_codes(self, codes: Union[str, List[str]]) -> "MortalityQuery":
        """
        Filter by ICD-10 cause of death codes.

        Args:
            codes: ICD-10 code(s) (e.g., "I00-I99" or ["I00-I99", "C00-D48"])

        Common code ranges:
        - I00-I99: Cardiovascular diseases
        - C00-D48: Cancers
        - J00-J99: Respiratory diseases
        - E10-E14: Diabetes
        - V01-Y98: External causes (injuries)
        """
        if isinstance(codes, list):
            codes = " ".join(codes)

        self.parameters[f"V_{self.database_id}.V2"] = codes
        return self

    def measure_deaths(self) -> "MortalityQuery":
        """Include deaths count measure"""
        self.parameters["M_1"] = f"{self.database_id}.M1"
        return self

    def measure_population(self) -> "MortalityQuery":
        """Include population measure"""
        self.parameters["M_2"] = f"{self.database_id}.M2"
        return self

    def measure_crude_rate(self) -> "MortalityQuery":
        """Include crude death rate per 100,000"""
        self.parameters["M_3"] = f"{self.database_id}.M3"
        return self

    def build(self) -> str:
        """
        Build XML request string.

        Returns:
            XML request string ready for API submission
        """
        api = CDCWonderAPI()
        return api.build_xml_request(self.parameters)


def example_cardiovascular_mortality():
    """
    Example: Query cardiovascular disease mortality by year.

    This demonstrates how to use the CDC WONDER API to retrieve
    national mortality data.
    """
    print("\n=== CDC WONDER API Example: Cardiovascular Mortality ===\n")

    # Build query
    query = MortalityQuery(database_id="D76")
    query.group_by_year()
    query.filter_years([2010, 2011, 2012])
    query.filter_icd10_codes("I00-I99")  # Cardiovascular diseases
    query.measure_deaths()
    query.measure_crude_rate()

    xml_request = query.build()
    print("XML Request:")
    print(xml_request)
    print()

    # Execute query
    api = CDCWonderAPI(rate_limit_seconds=120)

    try:
        result = api.query(
            database_id="D76",
            xml_request=xml_request
        )

        # Display results
        print("\n=== Results ===\n")
        for row in result.data:
            print(row)

        # Display footnotes
        if result.footnotes:
            print("\n=== Footnotes ===\n")
            for footnote in result.footnotes:
                print(f"- {footnote}")

        # Display caveats
        if result.caveats:
            print("\n=== Caveats ===\n")
            for caveat in result.caveats:
                print(f"- {caveat}")

    except Exception as e:
        print(f"[ERROR] Query failed: {e}")


def example_cancer_mortality_by_race():
    """
    Example: Query cancer mortality by race.

    Demonstrates grouping by multiple dimensions.
    """
    print("\n=== CDC WONDER API Example: Cancer Mortality by Race ===\n")

    # Build query
    query = MortalityQuery(database_id="D76")
    query.group_by_year()
    query.group_by_race()
    query.filter_years([2010, 2011, 2012, 2013])
    query.filter_icd10_codes("C00-D48")  # All cancers
    query.measure_deaths()
    query.measure_crude_rate()

    xml_request = query.build()

    # Execute query
    api = CDCWonderAPI(rate_limit_seconds=120)

    try:
        result = api.query(
            database_id="D76",
            xml_request=xml_request
        )

        # Display results
        print("\n=== Results ===\n")
        print(f"Retrieved {len(result.data)} rows")

        # Show first 10 rows
        for i, row in enumerate(result.data[:10]):
            print(f"Row {i+1}: {row}")

        if len(result.data) > 10:
            print(f"\n... and {len(result.data) - 10} more rows")

    except Exception as e:
        print(f"[ERROR] Query failed: {e}")


def get_parameter_codes_from_web_interface():
    """
    Helper function documentation: How to get parameter codes.

    CDC WONDER API parameter codes are complex. To find the correct codes:

    1. Go to CDC WONDER web interface: https://wonder.cdc.gov/
    2. Select your database (e.g., Detailed Mortality)
    3. Build your query using the web form
    4. Click "Send" to view results
    5. On the Results tab, click "API Options" button
    6. Download the XML request file
    7. Use those parameter codes in your Python code

    This is the RECOMMENDED way to determine correct parameter values.
    """
    pass


if __name__ == "__main__":
    # Check if rate limiting is enabled from environment
    rate_limit = int(os.getenv("CDC_WONDER_RATE_LIMIT_SECONDS", "120"))
    print(f"Using rate limit: {rate_limit} seconds between requests")

    # Run examples
    print("\nNote: These examples will make real API calls to CDC WONDER.")
    print("Each query waits 2 minutes between requests (CDC recommendation).")
    print("\nTo skip examples, comment out the function calls below.\n")

    # Uncomment to run examples:
    # example_cardiovascular_mortality()
    # example_cancer_mortality_by_race()

    print("\n" + "="*70)
    print("CDC WONDER API Integration Ready")
    print("="*70)
    print("\nTo use this module:")
    print("1. Import: from backend.pipelines.cdc_wonder_api import CDCWonderAPI")
    print("2. Initialize: api = CDCWonderAPI()")
    print("3. Build query: Use MortalityQuery() helper or build XML manually")
    print("4. Execute: result = api.query(database_id, xml_request)")
    print("\nSee documentation: docs/API_INTEGRATION_GUIDE.md")
    print("="*70)
