# Longbridge OpenAPI Reference

This document is auto-generated from the official documentation source.

## Quote API

### 获取标的实时行情

该接口用于获取标的的实时行情 (支持所有类型标的）。


**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string[] | 标的代码列表，使用 `ticker.region` 格式，例如：`[700.HK]` <br /><br />**校验规则：**<br />每次请求支持传入的标的数量上限是 `500` 个 |
| secu_quote | object[] | 标的实时行情数据列表 |
| ∟ symbol | string | 标的代码 |
| ∟ last_done | string | 最新价 |
| ∟ prev_close | string | 昨收价 |
| ∟ open | string | 开盘价 |
| ∟ high | string | 最高价 |
| ∟ low | string | 最低价 |
| ∟ timestamp | int64 | 最新成交的时间戳 |
| ∟ volume | int64 | 成交量 |
| ∟ turnover | string | 成交额 |
| ∟ pre_market_quote | object | 美股盘前交易行情 |
| ∟∟ last_done | string | 最新价 |
| ∟∟ timestamp | int64 | 最新成交的时间戳 |
| ∟∟ volume | int64 | 成交量 |
| ∟∟ turnover | string | 成交额 |
| ∟∟ high | string | 最高价 |
| ∟∟ low | string | 最低价 |
| ∟∟ prev_close | string | 上一个交易阶段的收盘价 |
| ∟ post_market_quote | object | 美股盘后交易行情 |
| ∟∟ last_done | string | 最新价 |
| ∟∟ timestamp | int64 | 最新成交的时间戳 |
| ∟∟ volume | int64 | 成交量 |
| ∟∟ turnover | string | 成交额 |
| ∟∟ high | string | 最高价 |
| ∟∟ low | string | 最低价 |
| ∟∟ prev_close | string | 上一个交易阶段的收盘价 |
| ∟ overnight_quote | object | 美股夜盘交易行情<br/><br/>注意：需开启 `enable_overnight` 参数，否则会返回 null |
| ∟∟ last_done | string | 最新价 |
| ∟∟ timestamp | int64 | 最新成交的时间戳 |
| ∟∟ volume | int64 | 成交量 |
| ∟∟ turnover | string | 成交额 |
| ∟∟ high | string | 最高价 |
| ∟∟ low | string | 最低价 |
| ∟∟ prev_close | string | 上一个交易阶段的收盘价 |
| 3 | 301600 | 请求参数有误或解包失败 |
| 3 | 301606 | 降低请求频次 |
| 7 | 301602 | 请重试或联系技术人员处理 |
| 7 | 301607 | 请求的标的数量超限，请减少单次请求标的数量 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/quote/pull/quote)

### 获取标的盘口

该接口用于获取标的的盘口数据。


**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string | 标的代码，使用 `ticker.region` 格式，例如：`700.HK` |
| symbol | string | 标的代码 |
| ask | object[] | 卖盘 |
| ∟ position | int32 | 档位 |
| ∟ price | string | 价格 |
| ∟ volume | int64 | 挂单量 |
| ∟ order_num | int64 | 订单数量 |
| bid | object[] | 买盘 |
| ∟ position | int32 | 档位 |
| ∟ price | string | 价格 |
| ∟ volume | int64 | 挂单量 |
| ∟ order_num | int64 | 订单数量 |
| 3 | 301600 | 请求参数有误或解包失败 |
| 3 | 301606 | 降低请求频次 |
| 7 | 301602 | 请重试或联系技术人员处理 |
| 7 | 301600 | 检查请求的 `symbol` 是否正确 |
| 7 | 301603 | 标的没有请求的行情数据 |
| 7 | 301604 | 没有获取标的行情的权限 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/quote/pull/depth)

### Get Security Brokers

该接口用于获取标的的实时经纪队列数据。


**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string | 标的代码，使用 `ticker.region` 格式，例如： `700.HK` |
| symbol | string | 标的代码 |
| ask_brokers | object[] | 卖盘经纪队列 |
| ∟ position | int32 | 档位 |
| ∟ broker_ids | int32[] | 券商席位 ID，通过[获取券商席位 ID ](./broker-ids) 接口获取 |
| bid_brokers | object[] | 买盘经纪队列 |
| ∟ position | int32 | 档位 |
| ∟ broker_ids | int32[] | 券商席位 ID，通过[获取券商席位 ID ](./broker-ids) 接口获取 |
| 3 | 301600 | 请求参数有误或解包失败 |
| 3 | 301606 | 降低请求频次 |
| 7 | 301602 | 请重试或联系技术人员处理 |
| 7 | 301600 | 检查请求的 `symbol` 是否正确 |
| 7 | 301603 | 标的没有请求的行情数据 |
| 7 | 301604 | 没有获取标的行情的权限 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/quote/pull/brokers)

### 获取标的 k 线

该接口用于获取标的的 K 线数据。


**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string | 标的代码，使用 `ticker.region` 格式，例如：`700.HK` |
| count | int32 | 数据数量，例如：`100`<br /><br />**校验规则：** <br />请求数量最大为 `1000` |
| trade_session | int32 | 交易时段，0: 盘中，100: 所有（盘前，盘中，盘后，夜盘） |
| symbol | string | 标的代码，例如：`AAPL.US` |
| candlesticks | object[] | K 线数据 |
| ∟ close | string | 当前周期收盘价 |
| ∟ open | string | 当前周期开盘价 |
| ∟ low | string | 当前周期最低价 |
| ∟ high | string | 当前周期最高价 |
| ∟ volume | int64 | 当前周期成交量 |
| ∟ turnover | string | 当前周期成交额 |
| ∟ timestamp | int64 | 当前周期的时间戳 |
| 3 | 301600 | 请求参数有误或解包失败 |
| 3 | 301606 | 降低请求频次 |
| 7 | 301602 | 请重试或联系技术人员处理 |
| 7 | 301600 | 检查请求的 `symbol`，`count`，`adjust_type`, `period` 数据是否在正确范围 |
| 7 | 301603 | 标的没有请求的行情数据 |
| 7 | 301604 | 没有获取标的行情的权限 |
| 7 | 301607 | 请求的数据数量超限，减少数据数量 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/quote/pull/candlestick)

## Trade API

### Load configuration from environment variables

该接口用于港美股，窝轮，期权的委托下单。

- **Endpoint**: `/v1/trade/order` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string | 股票代码，使用 `ticker.region` 格式，例如：`AAPL.US` |
| order_type | string | [订单类型](../trade-definition#ordertype) |
| submitted_price | string | 下单价格，例如：`388.5`<br/><br/> `LO` / `ELO` / `ALO` / `ODD` / `LIT` 订单必填 |
| submitted_quantity | string | 下单数量，例如：`100` |
| trigger_price | string | 触发价格，例如：`388.5`<br/><br/> `LIT` / `MIT` 订单必填 |
| limit_offset | string | 指定价差，例如 "1.2" 表示价差 1.2 USD (如果是美股)<br/><br/> `TSLPAMT` / `TSLPPCT` 订单在 `limit_depth_level` 为 0 时必填 |
| trailing_amount | string | 跟踪金额<br/><br/> `TSLPAMT` 订单必填 |
| trailing_percent | string | 跟踪涨跌幅，单位为百分比，例如 "2.5" 表示 "2.5%"<br/><br/> `TSLPPCT` 订单必填 |
| expire_date | string | 长期单过期时间，格式为 `YYYY-MM-DD`, 例如：`2022-12-05`<br/><br/> time_in_force 为 `GTD` 时必填 |
| side | string | 买卖方向<br/><br/> **可选值：**<br/> `Buy` - 买入<br/> `Sell` - 卖出 |
| outside_rth | string | 是否允许盘前盘后，美股必填<br/><br/> **可选值：**<br/> `RTH_ONLY` - 不允许盘前盘后<br/> `ANY_TIME` - 允许盘前盘后<br/> `OVERNIGHT` - 夜盘 |
| time_in_force | string | 订单有效期类型<br/><br/> **可选值：**<br/> `Day` - 当日有效<br/> `GTC` - 撤单前有效<br/> `GTD` - 到期前有效 |
| remark | string | 备注 (最大 64 字符) |
| limit_depth_level | int32 | 指定买卖档位，取值范围为 -5 ～ 0 ～ 5，负数代表买盘档位（如 -1 表示买一），<br/>正数代表卖盘档位（如 1 表示卖一），为 0 时 limit_offset 参数生效<br/>`TSLPAMT` / `TSLPPCT` 订单有效 |
| monitor_price | string | 监控价格，需要达到该价格才会开始监控，更新参考价<br/>`TSLPAMT` / `TSLPPCT` 订单有效 |
| trigger_count | int32 | 触发次数，取值范围 0 ~ 3, 表示在 1 分钟内触发多次才会触发订单<br/>`LIT` / `MIT` / `TSLPAMT` / `TSLPPCT` 订单有效 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/order/submit)

### 

该接口用于订单撤销。

- **Endpoint**: `/v1/trade/order` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| order_id | string | 订单 ID |
| 200 | 提交成功，订单已委托。 | None |
| 400 | 撤单被拒绝，请求参数错误。 | None |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/order/withdraw)

### 

该接口用于获取当日订单和订单查询。

- **Endpoint**: `/v1/trade/order/today` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string | 股票代码，使用 `ticker.region` 格式，例如：`AAPL.US` |
| status | string[] | [订单状态](../trade-definition#orderstatus)<br/><br/>例如：`status=FilledStatus&status=NewStatus` |
| side | string | 买卖方向<br/><br/> **可选值：**<br/> `Buy` - 买入<br/> `Sell` - 卖出 |
| market | string | 市场<br/><br/> **可选值：**<br/> `US` - 美股<br/> `HK` - 港股 |
| order_id | string | 订单 ID，用于指定订单 ID 查询，例如：`701276261045858304` |
| 200 | 当日订单查询成功 | [today_orders_rsp](#schematoday_orders_rsp) |
| 400 | 查询失败，请求参数错误。 | None |
| orders | object[] | 订单信息 |
| ∟ order_id | string | 订单 ID |
| ∟ status | string | [订单状态](../trade-definition#orderstatus) |
| ∟ stock_name | string | 股票名称 |
| ∟ quantity | string | 下单数量 |
| ∟ executed_quantity | string | 成交数量。<br/><br/>当订单未成交时为 0 |
| ∟ price | string | 下单价格。<br/><br/>当市价条件单未触发时为空字符串 |
| ∟ executed_price | string | 成交价。<br/><br/>当订单未成交时为 0 |
| ∟ submitted_at | string | 下单时间 |
| ∟ side | string | 买卖方向<br/><br/> **可选值：**<br/> `Buy` - 买入<br/> `Sell` - 卖出 |
| ∟ symbol | string | 股票代码，使用 `ticker.region` 格式，例如：`AAPL.US` |
| ∟ order_type | string | [订单类型](../trade-definition#ordertype) |
| ∟ last_done | string | 最近成交价格。<br/><br/>当订单未成交时为空字符串 |
| ∟ trigger_price | string | `LIT` / `MIT` 订单触发价格。<br/><br/>当订单不是 `LIT` / `MIT` 订单为空字符串 |
| ∟ msg | string | 拒绝信息或备注，默认为空字符串。 |
| ∟ tag | string | 订单标记<br/><br/> **可选值：**<br/> `Normal` - 普通订单<br/> `GTC` - 长期单<br/> `Grey` - 暗盘单 |
| ∟ time_in_force | string | 订单有效期类型<br/><br/> **可选值：**<br/> `Day` - 当日有效<br/> `GTC` - 撤单前有效<br/> `GTD` - 到期前有效 |
| ∟ expire_date | string | 长期单过期时间，格式为 `YYYY-MM-DD`, 例如：`2022-12-05。<br/><br/>不是长期单时，默认为空字符串。` |
| ∟ updated_at | string | 最近更新时间，格式为时间戳 (秒)，默认为 0。 |
| ∟ trigger_at | string | 条件单触发时间，格式为时间戳 (秒)，默认为 0。 |
| ∟ trailing_amount | string | `TSLPAMT` 订单跟踪金额。<br/><br/>当订单不是 `TSLPAMT` 订单时为空字符串。 |
| ∟ trailing_percent | string | `TSLPPCT` 订单跟踪涨跌幅。<br/><br/>当订单不是 `TSLPPCT` 订单时为空字符串。 |
| ∟ limit_offset | string | `TSLPAMT` / `TSLPPCT` 订单指定价差。<br/><br/>当订单不是 `TSLPAMT` / `TSLPPCT` 订单时为空字符串。 |
| ∟ trigger_status | string | 条件单触发状态<br/> 当订单不是条件单或条件单未触发时，触发状态为 NOT_USED<br/><br/> **可选值：**<br/> `NOT_USED` - 未激活 `DEACTIVE` - 已失效 `ACTIVE` - 已激活 `RELEASED` - 已触发 |
| ∟ currency | string | 结算货币 |
| ∟ outside_rth | string | 是否允许盘前盘后<br/> 当订单不是美股时，默认为 UnknownOutsideRth<br/><br/> **可选值：**<br/> `RTH_ONLY` - 不允许盘前盘后<br/> `ANY_TIME` - 允许盘前盘后<br/> `OVERNIGHT` - 夜盘" |
| ∟ remark | string | 备注 |
| ∟ limit_depth_level | int32 | 指定买卖档位 |
| ∟ trigger_count | int32 | 触发次数 |
| ∟ monitor_price | string | 监控价格 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/order/today_orders)

### 

该接口用于获取历史订单。

- **Endpoint**: `/v1/trade/order/history` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string | 股票代码，使用 `ticker.region` 格式，例如：`AAPL.US` |
| status | string[] | [订单状态](../trade-definition#orderstatus)<br/><br/>例如：`status=FilledStatus&status=NewStatus` |
| side | string | 买卖方向<br/><br/> **可选值：**<br/> `Buy` - 买入<br/> `Sell` - 卖出 |
| market | string | 市场<br/><br/> **可选值：**<br/> `US` - 美股<br/> `HK` - 港股 |
| start_at | string | 开始时间，格式为时间戳 (秒)，例如：`1650410999`。<br/><br/>开始时间为空时，默认为结束时间或当前时间前九十天。 |
| end_at | string | 结束时间，格式为时间戳 (秒)，例如：`1650410999`。<br/><br/>结束时间为空时，默认为开始时间后九十天或当前时间。 |
| 200 | 历史订单查询成功 | [history_orders_rsp](#schemahistory_orders_rsp) |
| 400 | 查询失败，请求参数错误。 | None |
| has_more | boolean | 是否还有更多数据。<br/><br/>每次查询最大订单数量为 1000，如果查询结果数量超过 1000，那么 has_more 就会为 true |
| orders | object[] | 订单信息 |
| ∟ order_id | string | 订单 ID |
| ∟ status | string | [订单状态](../trade-definition#orderstatus) |
| ∟ stock_name | string | 股票名称 |
| ∟ quantity | string | 下单数量 |
| ∟ executed_quantity | string | 成交数量。<br/><br/>当订单未成交时为 0 |
| ∟ price | string | 下单价格。<br/><br/>当市价条件单未触发时为空字符串 |
| ∟ executed_price | string | 成交价。<br/><br/>当订单未成交时为 0 |
| ∟ submitted_at | string | 下单时间 |
| ∟ side | string | 买卖方向<br/><br/> **可选值：**<br/> `Buy` - 买入<br/> `Sell` - 卖出 |
| ∟ symbol | string | 股票代码，使用 `ticker.region` 格式，例如：`AAPL.US` |
| ∟ order_type | string | [订单类型](../trade-definition#ordertype) |
| ∟ last_done | string | 最近成交价格。<br/><br/>当订单未成交时为空字符串 |
| ∟ trigger_price | string | `LIT` / `MIT` 订单触发价格。<br/><br/>当订单不是 `LIT` / `MIT` 订单为空字符串 |
| ∟ msg | string | 拒绝信息或备注，默认为空字符串。 |
| ∟ tag | string | 订单标记<br/><br/> **可选值：**<br/> `Normal` - 普通订单<br/> `GTC` - 长期单<br/> `Grey` - 暗盘单 |
| ∟ time_in_force | string | 订单有效期类型<br/><br/> **可选值：**<br/> `Day` - 当日有效<br/> `GTC` - 撤单前有效<br/> `GTD` - 到期前有效 |
| ∟ expire_date | string | 长期单过期时间，格式为 `YYYY-MM-DD`, 例如：`2022-12-05。<br/><br/>不是长期单时，默认为空字符串。` |
| ∟ updated_at | string | 最近更新时间，格式为时间戳 (秒)，默认为 0。 |
| ∟ trigger_at | string | 条件单触发时间，格式为时间戳 (秒)，默认为 0。 |
| ∟ trailing_amount | string | `TSLPAMT` 订单跟踪金额。<br/><br/>当订单不是 `TSLPAMT` 订单时为空字符串。 |
| ∟ trailing_percent | string | `TSLPPCT` 订单跟踪涨跌幅。<br/><br/>当订单不是 `TSLPPCT` 订单时为空字符串。 |
| ∟ limit_offset | string | `TSLPAMT` / `TSLPPCT` 订单指定价差。<br/><br/>当订单不是 `TSLPAMT` / `TSLPPCT` 订单时为空字符串。 |
| ∟ trigger_status | string | 条件单触发状态<br/> 当订单不是条件单或条件单未触发时，触发状态为 NOT_USED<br/><br/> **可选值：**<br/> `NOT_USED` - 未激活 `DEACTIVE` - 已失效 `ACTIVE` - 已激活 `RELEASED` - 已触发 |
| ∟ currency | string | 结算货币 |
| ∟ outside_rth | string | 是否允许盘前盘后<br/> 当订单不是美股时，默认为 UnknownOutsideRth<br/><br/> **可选值：**<br/> `RTH_ONLY` - 不允许盘前盘后<br/> `ANY_TIME` - 允许盘前盘后<br/> `OVERNIGHT` - 夜盘" |
| ∟ remark | string | 备注 |
| ∟ limit_depth_level | int32 | 指定买卖档位 |
| ∟ monitor_price | string | 监控价格 |
| ∟ trigger_count | int32 | 触发次数 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/order/history_orders)

## Asset API

### 获取账户资金

该接口用于获取用户每个币种可用、可取、冻结、待结算金额、在途资金 (基金申购赎回) 信息。

- **Endpoint**: `/v1/asset/account` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| currency | string | 币种（HKD、USD、CNH） |
| 200 | 返回成功 | [accountcash_rsp](#schemaaccountcash_rsp) |
| 400 | 内部错误 | None |
| list | object[] | 账户资金信息 |
| ∟ total_cash | string | 现金总额 |
| ∟ max_finance_amount | string | 最大融资金额 |
| ∟ remaining_finance_amount | string | 剩余融资金额 |
| ∟ risk_level | string | 风控等级 <br/> <br/> <b>可选值:</b><br/> `0` - 安全 <br/> `1` - 中风险<br/> `2` - 预警<br/> `3` - 危险 |
| ∟ margin_call | string | 追缴保证金 |
| ∟ net_assets | string | 净资产 |
| ∟ init_margin | string | 初始保证金 |
| ∟ maintenance_margin | string | 维持保证金 |
| ∟ currency | string | 币种 |
| ∟ market | string | 市场 |
| ∟ buy_power | string | 购买力 |
| ∟ cash_infos | object[] | 现金详情 |
| ∟∟ withdraw_cash | string | 可提现金 |
| ∟∟ available_cash | string | 可用现金 |
| ∟∟ frozen_cash | string | 冻结现金 |
| ∟∟ settling_cash | string | 待结算现金 |
| ∟∟ currency | string | 币种 |
| ∟ frozen_transaction_fees | object[] | 冻结费用 |
| ∟∟ currency | string | 币种 |
| ∟∟ frozen_transaction_fee | string | 费用金额 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/asset/account)

### 获取股票持仓

该接口用于获取包括账户、股票代码、持仓股数、可用股数、持仓均价（按账户设置计算均价方式）、币种在内的股票持仓信息。

- **Endpoint**: `/v1/asset/stock` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| symbol | string[] | 股票代码，使用 `ticker.region` 格式，例如：`AAPL.US` |
| 200 | 返回成功 | [stock_rsp](#schemastock_rsp) |
| 400 | 内部错误 | None |
| list | object[] | 股票持仓信息 |
| ∟ account_channel | string | 账户类型 |
| ∟ stock_info | object[] | 股票列表 |
| ∟∟ symbol | string | 股票代码 |
| ∟∟ symbol_name | string | 股票名称 |
| ∟∟ quantity | string | 持仓股数 |
| ∟∟ available_quantity | string | 可用股数 |
| ∟∟ currency | string | 币种 |
| ∟∟ market | string | 市场 |
| ∟∟ cost_price | string | 成本价格 (具体根据客户端选择平均买入还是摊薄成本) |
| ∟∟ init_quantity | string | 开盘前初始持仓 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/asset/stock)

### 获取资金流水

该接口用于获取资金流入/流出方向、资金类别、资金金额、发生时间、关联股票代码和资金流水说明信息。

- **Endpoint**: `/v1/asset/cashflow` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| start_time | string | 开始时间，时间戳，以 `秒` 为单位，例如：`1650037563` |
| end_time | string | 结束时间，时间戳，以 `秒` 为单位，例如：`1650747581` |
| business_type | string | 资金类型 <br/><br/> <b>可选值:</b> <br/>`1` - 现金 <br/>`2` - 股票<br/> `3` - 基金 |
| symbol | string | 标的代码，例如：`AAPL.US` |
| page | string | 起始页 <br/><br/><b>默认值:</b> `1` <br/><b>数据校验规则:</b><br/> <b>取值范围:</b> `>=1` |
| size | string | 每页大小 <br/><br/><b>默认值:</b> `50` <br/><b>数据校验规则:</b> `1~10000` |
| 200 | 返回成功 | [cashflow_rsp](#schemacashflow_rsp) |
| 400 | 内部错误 | None |
| list | object[] | 流水信息 |
| ∟ transaction_flow_name | string | 流水名称 |
| ∟ direction | string | 流出方向 <br/><br/><b>可选值:</b> <br/>`1` - 流出 <br/> `2` - 流入 |
| ∟ business_type | string | 资金类别 <br/><br/><b>可选值:</b> <br/>`1` - 现金 <br/> `2` - 股票 <br/> `3` - 基金 |
| ∟ balance | string | 资金金额 |
| ∟ currency | string | 资金币种 |
| ∟ business_time | string | 业务时间 |
| ∟ symbol | string | 关联股票代码信息 |
| ∟ description | string | 资金流水说明 |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/trade/asset/cashflow)

## Auth API

### 刷新 Access Token

在老的 `access_token` 过期之前，通过调用此接口获取新的 `access_token`。调用成功后老的 `access_token` 就会作废。

- **Endpoint**: `/v1/token/refresh` (GET)

**Parameters:**

| Name | Type | Description |
|------|------|-------------|
| Authorization | string | 是 |
| expired_at | string | 2023-04-14T12:13:57.859Z |
| code | int | 错误码，非 0 表示失败 |
| msg | string | 错误描述 |
| ∟token | string | 新的 access_token |
| ∟expired_at | string | 过期的时间戳 |
| ∟issued_at | string | 颁发时间 |
| ∟account_info | object | 用户信息 |
| ∟∟member_id | string | 用户 id |
| ∟∟aaid | string | aaid |
| ∟∟account_channel | string | account_channel |

- **Reference**: [Official Docs](https://open.longbridge.com/zh-CN/docs/refresh-token-api)

