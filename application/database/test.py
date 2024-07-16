import asyncio
from http import HTTPStatus
import logging
import requests
import time
from pydantic import BaseModel


logger = logging.getLogger(__name__)

    # Validate entry data
class TeamRequest(BaseModel):
    team: str

async def get_team_data(team):
    # Validate entry data
    TeamRequest(team=team)

    # Retry mechanism
    max_retries = 3
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(f"https://www.thesportsdb.com/api/v1/json/3/searchteams.php?t={team}")
            if response.status_code == HTTPStatus.OK:
                return response.json()
            elif response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
                time.sleep(20)
            else:
                raise Exception("Failed to fetch data from the API") 
        except Exception as e:
            logger.error("Request failed: {}".format(e))
            retries += 1
            time.sleep(1)
    raise Exception("Max retries exceeded")

# Example usage

async def main():
    try:
        # Directly await the coroutine's result
        result = await get_team_data("Arsenal")
    except Exception as e:
        print(f"An error occurred: {e}")

# This is the correct way to run a coroutine from a synchronous context in Python 3.7+
for i in range(0,2):
    asyncio.run(main())
    print(i)