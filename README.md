### Examples

proxies.txt:
```
127.0.0.1:8080
username:password@127.0.0.1:8080
127.0.0.1:8080@username:password
```

---

```python
from unityproxy import UnityProxy

unity = UnityProxy.from_file("proxies.txt")
print(unity)
```

```console
[
    Proxy(http://127.0.0.1:8080),
    Proxy(http://username:password@127.0.0.1:8080),
    Proxy(http://username:password@127.0.0.1:8080)
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
