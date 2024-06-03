# call_TC
簡單的幫助交控 3.0 下指令，除了可以一個一個指令下達還可以建立 timer 定期下指令與建立新的指令。

## 需求
使用 python3 執行與安裝 `pyserial`。
```
pip3 install pyserial
```

## 使用說明
在 `main.py`5中設定 com port 與 包率。
```
com = serial.Serial('/dev/ttyS1',9600)
```

在 `main.py` 的最後新增下達指令， `tx.request()` 為只會執行一次。中間會使用字串當命令，前面為指令名稱，後面接上參數，如下為 `5F46` 後面是參數。
```
tx.request('5F46 1 5')
```

如果要定期下指令使用 `tx.add_polling_request()` ，如下使用 5F4C 定期查看時制狀態。
```
tx.add_polling_request('5F4C')
```
