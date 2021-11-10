import datetime, time, json, pathlib, csv

cutofftime = time.mktime(datetime.datetime.strptime('2021-11-10 11:01:00 +0800','%Y-%m-%d %H:%M:%S %z').timetuple())

basepath = f"{pathlib.Path(__file__).parent.resolve()}"

fromAddress = '0x4a63f4113eb45d8f25132757005a5be5bf4951c0'

wallets = {}

def file_single():
    with open(f'{basepath}/export-token-0x73f67ae7f934ff15beabf55a28c2da1eeb9b56ec.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['Method']=='Buy' and row['From'] == fromAddress and int(row['UnixTimestamp']) < cutofftime):
                if row['To'] in wallets:
                    wallets[row['To']] += float(row['Quantity'].replace(',',''))
                else:
                    wallets[row['To']] = float(row['Quantity'].replace(',',''))


def file_multi():
    transactions = {}
    files = [
         f'{basepath}/export-token-0x73f67ae7f934ff15beabf55a28c2da1eeb9b56ec.csv',
         ]
    for file in files:
        with open(file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if(row['Method']=='Buy' and row['From'] == fromAddress and int(row['UnixTimestamp']) < cutofftime):
                    if not row['Txhash'] in transactions:
                        transactions[row['Txhash']] = {'To':row['To'], 'Quantity': float(row['Quantity'].replace(',','')) }

    for i, t in transactions.items():
        if t['To'] in wallets:
            wallets[t['To']] += t['Quantity']
        else:
            wallets[t['To']] = t['Quantity']

file_multi()

wallets = {k: v for k, v in sorted(wallets.copy().items(), key=lambda item: item[1])}

whitelist = {k: v for k, v in wallets.copy().items() if v >= 288}

nonlist = {k: v for k, v in wallets.copy().items() if v < 288}

file = f"{basepath}/report_{cutofftime}.json"

with open(file, "w") as fp:
  json.dump(
      {
        "all" : {
            "wallets_count": len(wallets.keys()), 
            "wallets_amount": sum(list(wallets.values())),
            "wallets": wallets,
        },
        "whitelist" : {
            "wallets_count": len(whitelist.keys()),
            "wallets_amount": sum(list(whitelist.values())),
            "wallets": whitelist,
        },
        "nonlist" : {
            "wallets_count": len(nonlist.keys()),
            "wallets_amount": sum(list(nonlist.values())),
            "wallets": nonlist,
        }
      },fp, indent=2)

file = f"{basepath}/whitelist_{cutofftime}.json"
with open(file, "w") as fp:
  json.dump(list(whitelist.keys()),fp, indent=2)


