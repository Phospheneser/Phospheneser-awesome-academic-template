# 占卜功能

支持九宫六壬、六爻起卦、塔罗牌。基础结果由 Python 本地计算，AI 解读是可选的外部服务。本功能用于娱乐。

## 本地运行

在仓库根目录运行：

```sh
python3 static/python/diviner/divine_server.py 8766
```

基础模式只依赖 Python 标准库。网页的静态服务与此 API 是两个进程；如果网页运行在 8765 端口，请打开：

`http://127.0.0.1:8765/index.html?lang=zh&serverUrl=http%3A%2F%2F127.0.0.1%3A8766`

用 `Ctrl+C` 停止 API。`GET /health` 返回健康状态，不调用占卜或 AI。

## 配置

`data/meta.json` 中的 `add_diviner` 控制显示，`divine.serverUrl` 可设置 API 地址。临时 URL 参数 `serverUrl` 优先，其次是浏览器旧有的 `localStorage.divineServerUrl`，再其次是配置；均未设置时使用现有 Render 地址。排查连错服务时也应检查旧的浏览器设置。

默认只请求基础结果。窗口中勾选「附加 AI 解读」才会等待模型；也可用 `divine.useLLM: true` 设置默认勾选。启用模型需在后端安装 `requirements.txt`，并设置 `LLM_API_KEY`；可通过 `LLM_API_BASE`、`LLM_MODEL` 指定提供方和模型。没有有效配置时保留基础结果并提示解读不可用，不发送占位密钥请求。

## 请求与错误处理

- `GET /divine?type=Tarot&query=...&use_llm=false`，问题为 1–1000 字。
- `200` 表示计算成功，`400` 表示输入错误，`500` 表示内部计算失败；全部返回 JSON 和 CORS 头。
- 前端使用简单 GET，超时覆盖响应体读取（75 秒），8 秒后显示慢响应提示。提交期间禁用重复操作，关闭窗口会取消等待；过期请求不能覆盖新窗口。
- 服务端先计算，再发送一次完整 HTTP 响应。请求可并发，只有使用共享随机数状态的短计算串行执行；AI 请求不占用计算锁，最多同时处理两次解读，繁忙或失败时返回基础结果。
- 请求失败不再自动替换为模拟结果。拖动采用 Pointer Events，区分点击与拖动，支持鼠标和触摸。
- 六爻的用九/用六在当前资料中缺失，会明确提示并展示已有卦辞，不再抛出 KeyError。

## 诊断记录与验证

本次线上探测：关闭 AI 的第一次请求 45 秒无响应，随后的塔罗请求 HTTP 200、约 0.47 秒返回有效 JSON。这与休眠后的冷启动表现一致，但没有访问部署日志，不能据此确认云端套餐或故障原因。Render 官方说明免费服务闲置 15 分钟会休眠，恢复约需一分钟：[Render FAQ](https://render.com/docs/faq)。

```sh
python3 -m unittest discover -s tests -p 'test_*.py'
```

本仓库后端测试覆盖三种算法、HTTP 错误、并发请求、AI 阻塞/失败，以及六爻 4096 种组合的数据覆盖。前端请求、取消、点击与超时测试位于配套的 Phospheneser.github.io 仓库；上述前端交互改进需要发布配套前端后生效。测试不调用真实付费模型接口。

GitHub Pages 仅发布静态前端。后端修复需要另行部署到运行 API 的服务；本地修改不会自动改变 Render 上的版本。
