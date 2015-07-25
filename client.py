import ConfigParser, psutil, os, requests, json

dirname, filename = os.path.split(os.path.abspath(__file__))

Config = ConfigParser.ConfigParser()
Config.read(dirname + '/config.ini')

remote_host = Config.get("main", "remote_host")
api_key = Config.get("main", "api_key")

def cpu_usage_to_json(cpu_usages):
    rows = []
    cpu_num = 0
    for cpu_usage in cpu_usages:
        row = {}
        sum_percent = 0
        row['cpu_num'] = cpu_num
        cpu_num = cpu_num + 1
        for tupel in cpu_usage.__dict__.items():
            row[tupel[0]] = tupel[1]
            if tupel[0] != 'idle':
                sum_percent = sum_percent + tupel[1]
        row['sum'] = sum_percent
        rows.append(row)

    return rows

def loop():
    while True:
        cpu_usage = cpu_usage_to_json(psutil.cpu_times_percent(interval=1, percpu=True))
        requests.post(remote_host + "/" + api_key + "/cpu", data=json.dumps(cpu_usage))

if __name__ == "__main__":
    loop()
