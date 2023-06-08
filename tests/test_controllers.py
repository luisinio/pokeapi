"""Test controllers module."""

import os
import asyncio
from unittest import TestCase, mock
from flask import Flask
from app.controllers import (
    get_general_berries,
    consult_url,
    process_berries,
    process_results,
    main_task,
)


class TestControllers(TestCase):
    """Test controllers module."""

    def setUp(self):
        self.app = Flask(__name__)

    @mock.patch.dict(os.environ, {"URL_BERRY": "http://localhost:8000"})
    def test_get_general_berries(self):
        """Test get_general_berries"""
        with mock.patch("app.controllers.requests") as mock_requests:
            mock_response = mock.Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "results": [
                    {"name": "berry1", "url": "url1"},
                    {"name": "berry2", "url": "url2"},
                ],
                "next": None,
            }
            mock_requests.get.return_value = mock_response

            result = get_general_berries()

            self.assertEqual(
                result,
                {
                    "berry1": {"url": "url1"},
                    "berry2": {"url": "url2"},
                },
            )

    async def test_consult_url(self):
        """Test consult_url"""
        name = "berry"
        url = "http://localhost:8000/berry"
        mock_response = mock.Mock()
        mock_response.status = 200
        mock_response.json.return_value = {"growth_time": 10}

        with mock.patch(
            "app.controllers.aiohttp.ClientSession"
        ) as mock_session:
            mock_session.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            result = await consult_url(name, url)

            self.assertEqual(result, (name, {"growth_time": 10}))

    async def test_process_berries(self):
        """Test process_berries"""
        data_berries = {
            "berry1": {"url": "url1"},
            "berry2": {"url": "url2"},
        }

        with mock.patch("app.controllers.consult_url") as mock_consult_url:
            mock_consult_url.return_value = ("berry1", {"growth_time": 10})

            asyncio.run(process_berries())

            self.assertTrue(mock_consult_url.called)
            self.assertEqual(
                data_berries,
                {
                    "berry1": {"url": "url1", "growth_time": 10},
                    "berry2": {"url": "url2"},
                },
            )

    async def test_process_results(self):
        """Test process_results"""
        name = "berry1"
        data = {"growth_time": 10}
        data_berries = {
            "berry1": {"url": "url1"},
            "berry2": {"url": "url2"},
        }

        await process_results(name, data)

        self.assertEqual(
            data_berries,
            {
                "berry1": {"url": "url1", "growth_time": 10},
                "berry2": {"url": "url2"},
            },
        )

    async def test_main_task(self):
        """Test main_task"""
        with mock.patch(
            "app.controllers.process_berries"
        ) as mock_process_berries:
            await main_task()

            self.assertTrue(mock_process_berries.called)

    async def test_get_berries_statics(self):
        """Test get_berries_statics"""
        with mock.patch.dict(
            os.environ, {"URL_BERRY": "http://localhost:8000"}
        ):
            with mock.patch(
                "app.controllers.get_general_berries"
            ) as mock_get_general_berries:
                data_berries = {
                    "berry1": {"url": "url1", "growth_time": 10},
                    "berry2": {"url": "url2", "growth_time": 20},
                    "berry3": {"url": "url3", "growth_time": 15},
                }
                mock_get_general_berries.return_value = data_berries

                with self.app.test_client() as client:
                    with mock.patch("app.routes.get_data") as mock_get_data:
                        mock_get_data.return_value = "mock response"

                        response = client.get("/allBerryStats")
                        self.assertEqual(response.status_code, 200)

                        expected_result = {
                            "berries_names": ["berry1", "berry2", "berry3"],
                            "min_growth_time": 10,
                            "median_growth_time": 15,
                            "max_growth_time": 20,
                            "variance_growth_time": 12.22,
                            "mean_growth_time": 15,
                            "frequency_growth_time": {10: 1, 20: 1, 15: 1},
                        }

                        self.assertEqual(response.json, expected_result)
