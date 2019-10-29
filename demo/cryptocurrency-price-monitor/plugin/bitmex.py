import json
import bitmex

def get_price_generator(c1, c2):
    client = bitmex.bitmex(test=False)
    def get_price():
        try:
            return client.Instrument.Instrument_get(filter=json.dumps({'symbol': 'XBTUSD'})).result()[0][0]['lastPrice'];
        except:
            return -1
    return get_price

