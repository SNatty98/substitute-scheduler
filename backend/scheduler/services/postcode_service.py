import requests
from decimal import Decimal
from math import radians, sin, cos, sqrt, atan2


class PostcodeService:

    BASE_URL = 'https://api.postcodes.io/postcodes'
    TIMEOUT_SECONDS = 5

    @staticmethod
    def lookup(postcode):

        clean_postcode = postcode.replace(' ', '').upper()

        try:
            response = requests.get(
                f'{PostcodeService.BASE_URL}/{clean_postcode}',
                timeout=PostcodeService.TIMEOUT_SECONDS)

            if response.status_code == 200:
                data = response.json()
                result = data['result']
                return {
                    'postcode': result['postcode'],
                    'latitude': Decimal(str(result['latitude'])),
                    'longitude': Decimal(str(result['longitude']))
                }
            else:
                raise ValueError(f"Invalid postcode: {postcode}")

        except requests.RequestException as e:
            raise ValueError(f"Error fetching postcode data: {str(e)}")

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        """
        Calculate distance between two coordinates using Haversine formula.

        Args:
            lat1: Latitude of first point (Decimal or float)
            lon1: Longitude of first point (Decimal or float)
            lat2: Latitude of second point (Decimal or float)
            lon2: Longitude of second point (Decimal or float)

        Returns:
            Distance in miles (float), rounded to 2 decimal places

        Example:
            distance = PostcodeService.calculate_distance(
                51.5014, -0.1419,  # London coordinates
                53.4808, -2.2426   # Manchester coordinates
            )
            # Returns: 163.51 (miles)
        """
        # Convert to float and then to radians
        lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
        lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        # Earth's radius in miles
        radius_miles = 3959
        distance = radius_miles * c

        return round(distance, 2)
