import bitmex
client = bitmex.bitmex(api_key='mzIN8PagBd5wBb7S3RsrjtDu', api_secret='GUafVfBrlWMmG0sUNe0CfU7qkoDL5wSa0ct_I1Klf7dR7_o6')
client.Quote.Quote_get(symbol='XBTUSD').result()