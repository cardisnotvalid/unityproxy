### Examples

proxies.txt:
```
127.0.0.1:8080
username:password@127.0.0.1:8080
127.0.0.1:8080@username:password
```

proxies.json:
```json
[
    {
        "host": "127.0.0.1",
        "port": 1234,
        "scheme": "socks5",
        "username": "username",
        "password": "password"
    },
    {
        "host": "0.0.0.0",
        "port": 8080,
        "scheme": "socks5",
        "username": "username",
        "password": "password"
    },
    {
        "host": "43.53.63.1",
        "port": 4431,
        "scheme": "https",
        "username": "username",
        "password": "password"
    }
]
```

proxies.csv:
```csv
host,port,scheme,username,password
127.0.0.1,8080,socks5
127.0.0.1,8080,http,username,password
0.0.0.1,3232,https,username,password
```

---

```python
from unityproxy import UnityProxy

unity = UnityProxy.from_file("proxies.txt")
unity = UnityProxy.from_file("proxies.json")
unity = UnityProxy.from_file("proxies.csv")
print(unity)
```

From txt file:

```console
[
    Proxy(http://127.0.0.1:8080),
    Proxy(http://username:password@127.0.0.1:8080),
    Proxy(http://username:password@127.0.0.1:8080)
]
```

From json file:

```console
[
    Proxy(socks5://username:password@127.0.0.1:1234),
    Proxy(socks5://username:password@0.0.0.0:8080),
    Proxy(https://username:password@43.53.63.1:4431)
]
```

From csv file:

```console
[
	Proxy(socks5://127.0.0.1:8080),
	Proxy(http://username:password@127.0.0.1:8080),
	Proxy(https://username:password@0.0.0.1:3232)
]
```

---

```python
from unityproxy import UnityProxy

unity = UnityProxy()
unity.add_by_line("test://username:password@0.0.0.1:8080")
unity.add_by_line("username:password@0.0.0.1:8080", default_scheme="test_scheme")
unity.add_by_line("test://0.0.0.1:8080@username:password")
unity.add_by_line("0.0.0.1:8080@username:password", default_scheme="test_scheme")
print(unity)
```

```console
[
    Proxy(test://username:password@0.0.0.1:8080),
    Proxy(test_scheme://username:password@0.0.0.1:8080),
    Proxy(test://username:password@0.0.0.1:8080),
    Proxy(test_scheme://username:password@0.0.0.1:8080)
]
```

---

```python
from unityproxy import UnityProxy

unity = UnityProxy.from_file("proxies.txt")

for proxy in unity:
    print(proxy.adapter.requests)
```

```console
{'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}
{'http': 'http://username:password@127.0.0.1:8080', 'https': 'http://username:password@127.0.0.1:8080'}
{'http': 'http://username:password@127.0.0.1:8080', 'https': 'http://username:password@127.0.0.1:8080'}
```
