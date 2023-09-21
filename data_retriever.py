import logging
import requests
from typing import Union
import pandas as pd
import streamlit as st

logging.basicConfig(level=logging.INFO)

class DataRetriever:
    """Class to encapsulate data retrieval and processing operations."""
    
    def set_limit(period: str) -> int:
        """
        Sets the limit based on the period.
        
        :param period: The time period for which to set the limit.
        :return: The calculated limit based on the input period.
        """
        if period == "4HRS":
            return ((24 // 4) * 30) + (24 * 7)  # one month + one week more
        elif period == "12HRS":
            return ((24 // 12) * 90) + (24 * 7)   # three months + one week more
        else:
            return (24 * 7) * 2  # one week + one week more

    def retrieve_data(url: str, headers: dict) -> Union[dict, list, None]:
        """
        Retrieves data from the API.
        
        :param url: The API URL from which to retrieve data.
        :param headers: The headers to include in the API request.
        :return: A data frame with the retrieved data, or None if an error occurred.
        """
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            st.write(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error occurred: {conn_err}")
            st.write(f"Connection error occurred: {conn_err}")
            return None
        except requests.exceptions.RequestException as req_err:
            logging.error(f"Error fetching data: {req_err}")
            st.write(f"Error fetching data: {req_err}")
            return None

        data = response.json()
        return data
