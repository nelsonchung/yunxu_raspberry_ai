# shared

放置 Raspberry Pi 主程式內部共用的資料結構、命令模型與設定定義。

## Recommended Contents

- Action enum
- Mission status enum
- Internal command schema
- Config schema
- Error codes

## Why This Matters

若共用型別不集中管理，模組之間很容易出現：

- 欄位名稱不一致
- action 拼字不同
- mission status 定義不同

把這些資料模型集中後，後續不管模型跑在 Pi 本機、MacBook 或其他主機，都比較容易維護。
