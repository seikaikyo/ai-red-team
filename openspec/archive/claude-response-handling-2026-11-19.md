# 呼叫 Claude API 的回應處理照官方文件修正

- **type**: fix
- **建立日期**: 2026-11-19
- **status**: completed

## 背景

2026-11-19 對照 Claude 平台官方文件，紅隊測試的 Claude 呼叫（backend/services/runner.py）有兩處跟文件寫法不同：

1. 每次都送使用者設的 `temperature`。Claude 4.7 以後的模型（opus-4-7、opus-4-8、opus-5、sonnet-5、haiku-5、fable、mythos）收到非預設值會回 400（官方 build-with-claude/thinking.md:1230）。目前白名單只有 claude-sonnet-4-6 與 claude-haiku-4-5-20251001，這兩個接受 temperature；白名單加入新模型時，使用者調了溫度就會整次失敗。
2. 沒有讀 `stop_reason`。拒答是 HTTP 200 加 `stop_reason: "refusal"`，不是錯誤（build-with-claude/handling-stop-reasons.md:1783）；思考也算進 `max_tokens`，上限太小時會在出文字前就停（models/fable-5-2/migration-guide.md:95）。現在這兩種情況存進紀錄時看起來跟正常的空回應或半截回應一樣。

文字已經依區塊 type 收集，這部分不用改。

## 變更內容

1. 新增 `backend/services/claude_response.py`：依 `type` 收集文字區塊並回傳 `stop_reason`；判斷模型是否接受取樣參數（前綴比對）。
2. `backend/services/runner.py`：
   - Claude 4.7 以後的模型不送 `temperature`，附註寫明本次未送出與要求值。
   - 回應以 `refusal` 或 `max_tokens` 結束時，在回應文字後附一行 `[stop_reason: ...]`，紀錄看得出是拒答或被截斷。
   - `execute_prompt` 改回傳三個值（文字、毫秒、附註）；OpenAI-compatible 路徑附註為空字串，其餘不動。
3. `backend/routers/tests.py`：把附註寫進 TestRun 的 `notes`。

## 影響範圍

- 只動上述檔案與新增的共用檔。資料表不動（`notes` 欄位本來就有），API 回應格式不動。
- 模型 ID、max_tokens、提示詞、白名單不動。
- `backend/scripts/batch_run.py`、`batch_run_remote.py` 用 claude-haiku-4-5-20251001 送 temperature 1.0（4.5 接受），文字已依 type 收集，不在這次範圍。

## UI規格

無畫面變更。紅隊紀錄的回應文字可能多一行 `[stop_reason: ...]`，notes 可能多一句未送出 temperature 的說明。

## 測試計畫

1. 新增 `backend/tests/test_claude_response_handling.py`，用假的 SDK 回應（不打 API）：
   - 第一塊是 thinking、第二塊是 text：讀到的是 text。
   - 選 claude-sonnet-5、temperature 0.3：送出的參數沒有 temperature，附註寫明；選 claude-haiku-4-5-20251001：照送。
   - `stop_reason: refusal` 沒有文字：回應是 `[stop_reason: refusal]`。
   - `stop_reason: max_tokens`：半截文字後附 `[stop_reason: max_tokens]`。
   - `/api/tests/run` 端點：附註寫進 TestRun 的 notes。
2. 這些新測試在改動前的程式上要失敗。
3. 既有測試全過。
