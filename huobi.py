import asyncio
from tardis_client import TardisClient, Channel
tardis_client = TardisClient(api_key="YOUR_API_KEY")

async def replay():
  # replay method returns Async Generator
  messages = tardis_client.replay(
    exchange="huobi-dm",
    from_date="2020-02-01",
    to_date="2020-02-02",
    filters=[Channel(name="detail", symbols=["BTC_CW"])]
  )

  # messages as provided by Huobi Futures real-time stream
  async for local_timestamp, message in messages:
    print(message)


asyncio.run(replay())