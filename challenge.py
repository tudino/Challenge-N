import sys
import pyRofex

ticker = ""
user = ""
password = ""
account = ""

def read_arguments():
	global ticker, user, password, account
	n = len(sys.argv)
	if n != 8:
		raise Exception("Debe ingresar ticker [-t] | user [-u] | password [-p] | account [-a]")

	ticker = sys.argv[1]
	for i in range(1, n):
		if sys.argv[i] == "-t" or sys.argv[i] == "--ticker":
			ticker = sys.argv[i+1]
		if sys.argv[i] == "-u" or sys.argv[i] == "--user":
			user = sys.argv[i+1]
		if sys.argv[i] == "-p" or sys.argv[i] == "--password":
			password = sys.argv[i+1]
		if sys.argv[i] == "-a" or sys.argv[i] == "--account":
			account = sys.argv[i+1]

def connect():
	print("Iniciando sesion en Remarkets")
	initialize = pyRofex.initialize(user=user, password=password, account=account, environment=pyRofex.Environment.REMARKET)

def disconnect():
	print("Cerrando sesion en Remarkets")

def symbol_exists():
	print("Consultando simbolo [{}]".format(ticker))
	instruments = pyRofex.get_all_instruments()
	for instrument in instruments["instruments"]:
		if ticker == instrument["instrumentId"]["symbol"]:
			return True
	raise Exception("Simbolo [{}] invalido".format(ticker))

def get_lp():
	print("Consultando LAST ...")
	md = pyRofex.get_market_data(ticker=ticker, entries=[pyRofex.MarketDataEntry.LAST])
	lp = md["marketData"]["LA"]["price"]
	print("Ultimo precio operado: " + str(lp))
	return lp

def get_bid():
	print("Consultando BID ...")
	md = pyRofex.get_market_data(ticker=ticker, entries=[pyRofex.MarketDataEntry.BIDS])
	if len(md["marketData"]["BI"]) == 0:
		return None
	else:
		bid = md["marketData"]["BI"][0]["price"]
		print("Precio de BID: " + str(bid))
		return bid

def send_order(value):
	order = pyRofex.send_order(ticker=ticker,
								side=pyRofex.Side.BUY,
								size=10,
								price=value,
								order_type=pyRofex.OrderType.LIMIT)
	if order["status"] == "ERROR":
		raise Exception("No se pudo enviar la orden: " + order["message"] + " " + order["description"])

	print("Nueva orden ingresada. Precio: " + str(value))
	print("ClientId: " + order["order"]["clientId"])

if __name__ == '__main__':
	try:
		read_arguments()
		connect()
		symbol_exists()
		lp = get_lp()
		bid = get_bid()
		if bid == None:
			send_order(189)
		else:
			send_order(bid - 0.5)
		disconnect()
	except Exception as e:
		print(e)