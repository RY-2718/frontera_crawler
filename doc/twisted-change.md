# twistedへの変更
/doc/に含まれている `client.py` `common.py` を参考に，以下のようにtwistedを変更して下さい．

- twisted/names/client.pyで以下のメソッドを書き換え，定義
    + getHostByName
    + getHostByNameV4
    + getHostByNameV6Address
    + getHostByName6
- twisted/names/common.pyで以下のメソッドを書き換え，定義
    + getHostByName
    + getHostByNameV4
    + getHostByNameV6Address
    + getHostByName6
