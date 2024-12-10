from binance.client import Client
import pandas as pd
import time, json
import psycopg2, datetime

api_key = "xoU9rCYYHhw5DOk1h6TGP3fHVusqVZh4xw3ruXu74wSx7iSdQyfwQvtiSgAUjhQS"
api_secrect = "O0H1c4THLvdcxkDh1WV4dVEY63BM1RJ9pvNMvymWrA9sW8Vt7m9ZsJLJloZbMlky"
testnet_api = "JXBSMhkCxnSXx6dKugHf246mYPmSTyHKGrEMesCDWCaeoHUpFEEIpGqsR9WoxzJY"
testnet_api_secrect = "kyYGKMyVfiCkzw3o3brsyDF6RoxieI7iIroR0T8xr9Exiq44M5YqqKxzPoloadUD"
db_params = {
    "host": "localhost",
    "database": "Binance ",
    "user": "postgres",
    "password": "admin123"
}
acc_ssid = "ACf867ac43d3e65c2a2bea6b23725fb323"
auth_token = "2d5e8aa4e52727e35921068c6516b226"

client = Client(api_key, api_secrect)
order_client = Client(testnet_api, testnet_api_secrect, testnet=True)

tickers = client.get_all_tickers()
tickers_df = pd.DataFrame(tickers)
current_pairs = list(tickers_df['symbol'])

def connect_to_db():
    return psycopg2.connect(**db_params)

def connect_to_dbs():
    conn = connect_to_db()
    cur = conn.cursor()
    
    cur.execute("SELECT pairs FROM trading_pairs")
    results = cur.fetchall()
    
    cur.close()
    conn.close()

    return results

def adding_current_pairs():
    
    already_existing = len(access())
    
    client1 = Client(api_key, api_secrect)
    tick = client1.get_all_tickers()
    dg = pd.DataFrame(tick)
    cp = list(dg['symbol'])

    if len(cp) != already_existing:
        
        conn = connect_to_db()
        cur = conn.cursor()
        this = datetime.datetime.now()
        json_p = json.dumps({"data": cp})

        query = "INSERT INTO new (ts, pairs) VALUES (%s, %s)"
        cur.execute(query, (this, json_p))

        conn.commit()

        cur.close()
        conn.close()
    else:
        print("No listing or delisting^_^")


def access():
    conn = connect_to_db()
    cur = conn.cursor()

    cur.execute("SELECT pairs FROM new")
    res = cur.fetchall()
    cur.close()
    conn.close()

    dt = res[-1][0]["data"]
    return dt

def tracker():
    client1 = Client(api_key, api_secrect)
    tick = client1.get_all_tickers()
    dg = pd.DataFrame(tick)
    
    cur = set(list(dg['symbol']))
    prv = set(access())

    result = list(cur - prv)
    print(result)
    result = [i for i in result if i[-4:] == "USDT"]
    executer(result)
    end_time = time.time()
    
def order_place(target_pair):
    pair = tickers_df[tickers_df['symbol'] == target_pair]
    price = list(pair['price'].astype(float))
    quant = 60 / price[0]

    buy_order = order_client.create_test_order(
        symbol = target_pair,
        type = "MARKET", 
        quantity = round(quant, 5),
        side = "BUY"
    )
    end_time = time.time()

def executer(x):
    for i in x:
        order_place(i)

while True:
    
    tracker()
    adding_current_pairs()
    t = datetime.datetime.now()
    time.sleep(0.05)