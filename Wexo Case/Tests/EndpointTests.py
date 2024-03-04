import unittest
from unittest.mock import patch, MagicMock
from ApiEndpoints import app


class EndpointTests(unittest.TestCase):

    # SetUp is called before each test execution to set up test environment
    # Creates a test client for a flask application
    # It configures the app for testing rather than normal operation
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Tests if the endpoint is able to take in valid data
    @patch('ApiEndpoints.moisture_gauge')
    def test_insert_data_valid_request(self, mock_moisture_gauge):
        # Arrange
        mock_moisture_gauge.labels.return_value.set.return_value = None

        # Act
        response = self.app.post('/api', json={"microcontrollerid": 1, "moisturelevel": 50})

        # Assert
        mock_moisture_gauge.labels.assert_called_with(microcontroller_id=1)
        mock_moisture_gauge.labels.return_value.set.assert_called_with(50)
        self.assertEqual(response.status_code, 200)
        self.assertIn("Data Received and Metric Updated", response.data.decode())

    # Tests that the endpoint handles invalid data correctly. In this case it is missing a microcontroller id.
    @patch('ApiEndpoints.moisture_gauge')
    def test_insert_data_invalid_request_missing_mc_id(self, mock_moisture_gauge):
        # Arrange
        mock_moisture_gauge.labels.return_value.set.return_value = None

        # Act
        response = self.app.post('/api', json={"moisturelevel": 50})

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON Data", response.data.decode())

    # Tests that the endpoint handles invalid data correctly. In this case it is missing moisture data.
    @patch('ApiEndpoints.moisture_gauge')
    def test_insert_data_invalid_request_missing_moisture_level(self, mock_moisture_gauge):
        # Arrange
        mock_moisture_gauge.labels.return_value.set.return_value = None

        # Act
        response = self.app.post('/api', json={"microcontrollerid": "1"})

        # Assert
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid JSON Data", response.data.decode())


if __name__ == '__main__':
    unittest.main()
