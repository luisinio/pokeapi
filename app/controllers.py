"""This module contains the controller functions for the API."""

import os
import asyncio
from cachetools import cached, TTLCache
import aiohttp
import requests
from flask import jsonify

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import io
import base64


# create a memory cache with a time to live of 10 minutes
cache = TTLCache(maxsize=100, ttl=600)

data_berries = {}


@cached(cache)
def get_general_berries():
    """get the data from the url and add it to the data_berries dict"""
    try:
        url = os.environ["URL_BERRY"]
        while url is not None:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                for elemnt in data["results"]:
                    data_berries[elemnt["name"]] = {"url": elemnt["url"]}
            else:
                return "Error to get API", response.status_code
            url = data["next"]
        return data_berries
    except requests.exceptions.RequestException as e_message:
        return "Error connecting API " + str(e_message), 500


async def consult_url(name, url):
    """get the data from the url and add it to the data_berries dict"""
    if name in cache:
        return cache[name]

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            # async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return name, data
            return name, None
    except Exception as e_message:  # pylint: disable=broad-except
        print(f"Error to get URL {url}: {str(e_message)}")
        return name, None


async def process_berries():
    """get the data from the url and add it to the data_berries dict"""
    for name, berry in data_berries.items():
        name, data = await consult_url(name, berry["url"])
        await process_results(name, data)


async def process_results(name, data):
    """get the data from the url and add it to the data_berries dict"""
    if data is not None:
        data_berries[name]["growth_time"] = data["growth_time"]


async def main_task():
    """main task to get the data from the url and add it to the data_berries dict"""
    await process_berries()


def get_berries_statics():
    """get the data from the url and add it to the data_berries dict"""
    data_berries = get_general_berries()

    asyncio.run(main_task())

    min_growth_time = min(  # noqa: F841
        data_berries.values(), key=lambda x: x["growth_time"]
    )["growth_time"]

    median_growth_time = sorted(  # noqa: F841
        data_berries.values(), key=lambda x: x["growth_time"]
    )[len(data_berries) // 2]["growth_time"]

    max_growth_time = max(  # noqa: F841
        data_berries.values(), key=lambda x: x["growth_time"]
    )["growth_time"]

    mean_growth_time = sum(
        x["growth_time"] for x in data_berries.values()
    ) / len(data_berries)

    variance_growth_time = sum(
        (x["growth_time"] - mean_growth_time) ** 2
        for x in data_berries.values()
    ) / len(data_berries)

    growth_times = [x["growth_time"] for x in data_berries.values()]
    growth_times.sort()
    growth_count = len(growth_times)
    if growth_count % 2 == 0:
        median_growth_time = (
            growth_times[growth_count // 2 - 1]
            + growth_times[growth_count // 2]
        ) / 2
    else:
        median_growth_time = growth_times[growth_count // 2]

    frequency_growth_time = {  # noqa: F841
        x["growth_time"]: len(
            [
                y
                for y in data_berries.values()
                if y["growth_time"] == x["growth_time"]
            ]
        )
        for x in data_berries.values()
    }

    result = {
        "berries_names": sorted(data_berries.keys()),
        "min_growth_time": min_growth_time,
        "median_growth_time": round(median_growth_time, 2),
        "max_growth_time": max_growth_time,
        "variance_growth_time": round(variance_growth_time, 2),
        "mean_growth_time": round(median_growth_time, 2),
        "frequency_growth_time": frequency_growth_time,
    }
    return jsonify(result)


def generate_histogram():
    """get the data from get_berries_statics and generate a histogram"""

    if not data_berries:
        get_berries_statics()
    data = [x["growth_time"] for x in data_berries.values()]

    # Create the plot sorted by the growth time
    plt.hist(data, bins=10, color="blue", edgecolor="black")

    plt.xlabel("Value")
    plt.ylabel("Frecuency")
    plt.title("Histogram of Frequency Growth Time")

    # Save the image as object BytesIO
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    # Encode the image to base64
    image_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

    # return the image as html
    html = f'<img src="data:image/png;base64,{image_base64}" alt="Histogram">'

    return html
