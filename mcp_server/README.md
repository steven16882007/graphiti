# Graphiti MCP 伺服器

Graphiti 是一個專為在動態環境中運行的 AI 代理而設計的時間感知知識圖譜建構和查詢框架。與傳統的檢索增強生成 (RAG) 方法不同，Graphiti 持續整合用戶互動、結構化和非結構化企業數據以及外部資訊，形成一個連貫且可查詢的圖譜。該框架支援增量數據更新、高效檢索和精確的歷史查詢，無需完整重新計算圖譜，使其適合開發互動式、上下文感知的 AI 應用程式。

這是 Graphiti 的實驗性模型上下文協議 (MCP) 伺服器實作。MCP 伺服器透過 MCP 協議公開 Graphiti 的核心功能，讓 AI 助手能夠與 Graphiti 的知識圖譜功能進行互動。

## 功能特色

Graphiti MCP 伺服器公開了 Graphiti 的以下核心高階功能：

- **情節管理**：新增、檢索和刪除情節（文字、訊息或 JSON 數據）
- **實體管理**：搜尋和管理知識圖譜中的實體節點和關係
- **搜尋功能**：使用語義和混合搜尋來搜尋事實（邊）和節點摘要
- **群組管理**：使用 group_id 過濾來組織和管理相關數據群組
- **圖譜維護**：清除圖譜並重建索引

## 快速開始

### 複製 Graphiti GitHub 儲存庫

```bash
git clone https://github.com/getzep/graphiti.git
```

或

```bash
gh repo clone getzep/graphiti
```

### 適用於 Claude Desktop 和其他僅支援 `stdio` 的客戶端

1. 記下此目錄的完整路徑。

```
cd graphiti && pwd
```

2. 安裝 [Graphiti 先決條件](#先決條件)。

3. 配置 Claude、Cursor 或其他 MCP 客戶端以使用 [Graphiti 與 `stdio` 傳輸](#與-mcp-客戶端整合)。請參閱客戶端文件以了解在哪裡找到其 MCP 配置檔案。

### 適用於 Cursor 和其他支援 `sse` 的客戶端

1. 切換到 `mcp_server` 目錄

`cd graphiti/mcp_server`

2. 使用 Docker Compose 啟動服務

`docker compose up`

3. 將您的 MCP 客戶端指向 `http://localhost:8000/sse`

## 安裝

### 先決條件

1. 確保您已安裝 Python 3.10 或更高版本。
2. 運行中的 Neo4j 資料庫（需要 5.26 或更高版本）
3. 用於 LLM 操作的 OpenAI API 金鑰

### 設置

1. 複製儲存庫並導航到 mcp_server 目錄
2. 使用 `uv` 創建虛擬環境並安裝依賴項：

```bash
# 如果您還沒有安裝 uv，請先安裝
curl -LsSf https://astral.sh/uv/install.sh | sh

# 一步創建虛擬環境並安裝依賴項
uv sync
```

## 配置

伺服器使用以下環境變數：

- `NEO4J_URI`：Neo4j 資料庫的 URI（預設：`bolt://localhost:7687`）
- `NEO4J_USER`：Neo4j 使用者名稱（預設：`neo4j`）
- `NEO4J_PASSWORD`：Neo4j 密碼（預設：`demodemo`）
- `OPENAI_API_KEY`：OpenAI API 金鑰（LLM 操作必需）
- `OPENAI_BASE_URL`：OpenAI API 的可選基礎 URL
- `MODEL_NAME`：用於 LLM 操作的 OpenAI 模型名稱
- `SMALL_MODEL_NAME`：用於較小 LLM 操作的 OpenAI 模型名稱
- `LLM_TEMPERATURE`：LLM 回應的溫度（0.0-2.0）
- `AZURE_OPENAI_ENDPOINT`：可選的 Azure OpenAI LLM 端點 URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`：可選的 Azure OpenAI LLM 部署名稱
- `AZURE_OPENAI_API_VERSION`：可選的 Azure OpenAI LLM API 版本
- `AZURE_OPENAI_EMBEDDING_API_KEY`：可選的 Azure OpenAI 嵌入部署金鑰（如果與 `OPENAI_API_KEY` 不同）
- `AZURE_OPENAI_EMBEDDING_ENDPOINT`：可選的 Azure OpenAI 嵌入端點 URL
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME`：可選的 Azure OpenAI 嵌入部署名稱
- `AZURE_OPENAI_EMBEDDING_API_VERSION`：可選的 Azure OpenAI API 版本
- `AZURE_OPENAI_USE_MANAGED_IDENTITY`：可選使用 Azure 受控身分進行驗證
- `SEMAPHORE_LIMIT`：情節處理並發性。請參閱 [並發性和 LLM 提供者 429 速率限制錯誤](#並發性和-llm-提供者-429-速率限制錯誤)
- `VSCODE_UI_BRIDGE_WS`：VS Code UI Bridge 整合的可選 WebSocket URL（例如：`ws://127.0.0.1:5310?token=YOUR_TOKEN`）

您可以在專案目錄中的 `.env` 檔案中設置這些變數。

## 運行伺服器

使用 `uv` 直接運行 Graphiti MCP 伺服器：

```bash
uv run graphiti_mcp_server.py
```

使用選項：

```bash
uv run graphiti_mcp_server.py --model gpt-4.1-mini --transport sse
```

可用參數：

- `--model`：覆蓋 `MODEL_NAME` 環境變數
- `--small-model`：覆蓋 `SMALL_MODEL_NAME` 環境變數
- `--temperature`：覆蓋 `LLM_TEMPERATURE` 環境變數
- `--transport`：選擇傳輸方法（sse 或 stdio，預設：sse）
- `--group-id`：為圖譜設置命名空間（可選）。如果未提供，預設為 "default"
- `--destroy-graph`：如果設置，在啟動時銷毀所有 Graphiti 圖譜
- `--use-custom-entities`：啟用使用預定義 ENTITY_TYPES 的實體提取

### 並發性和 LLM 提供者 429 速率限制錯誤

Graphiti 的攝取管道設計為高並發性，由 `SEMAPHORE_LIMIT` 環境變數控制。
預設情況下，`SEMAPHORE_LIMIT` 設置為 `10` 個並發操作，以幫助防止來自您的 LLM 提供者的 `429` 速率限制錯誤。如果您遇到此類錯誤，請嘗試降低此值。

如果您的 LLM 提供者允許更高的吞吐量，您可以增加 `SEMAPHORE_LIMIT` 以提升情節攝取性能。

### Docker 部署

Graphiti MCP 伺服器可以使用 Docker 部署。Dockerfile 使用 `uv` 進行套件管理，確保
一致的依賴項安裝。

#### 環境配置

在運行 Docker Compose 設置之前，您需要配置環境變數。您有兩個選項：

1. **使用 .env 檔案**（推薦）：

   - 複製提供的 `.env.example` 檔案來創建 `.env` 檔案：
     ```bash
     cp .env.example .env
     ```
   - 編輯 `.env` 檔案以設置您的 OpenAI API 金鑰和其他配置選項：
     ```
     # LLM 操作必需
     OPENAI_API_KEY=your_openai_api_key_here
     MODEL_NAME=gpt-4.1-mini
     # 可選：OPENAI_BASE_URL 僅在非標準 OpenAI 端點時需要
     # OPENAI_BASE_URL=https://api.openai.com/v1
     ```
   - Docker Compose 設置配置為使用此檔案（如果存在）（這是可選的）

2. **直接使用環境變數**：
   - 您也可以在運行 Docker Compose 命令時設置環境變數：
     ```bash
     OPENAI_API_KEY=your_key MODEL_NAME=gpt-4.1-mini docker compose up
     ```

#### Neo4j 配置

Docker Compose 設置包含一個具有以下預設配置的 Neo4j 容器：

- 使用者名稱：`neo4j`
- 密碼：`demodemo`
- URI：`bolt://neo4j:7687`（從 Docker 網路內部）
- 為開發使用優化的記憶體設置

#### 使用 Docker Compose 運行

Graphiti MCP 容器可在以下位置獲得：`zepai/knowledge-graph-mcp`。下面的 Compose 設置使用此容器的最新構建。

使用 Docker Compose 啟動服務：

```bash
docker compose up
```

Or if you're using an older version of Docker Compose:

```bash
docker-compose up
```

This will start both the Neo4j database and the Graphiti MCP server. The Docker setup:

- Uses `uv` for package management and running the server
- Installs dependencies from the `pyproject.toml` file
- Connects to the Neo4j container using the environment variables
- Exposes the server on port 8000 for HTTP-based SSE transport
- Includes a healthcheck for Neo4j to ensure it's fully operational before starting the MCP server

## Integrating with MCP Clients

### Configuration

To use the Graphiti MCP server with an MCP-compatible client, configure it to connect to the server:

> [!IMPORTANT]
> You will need the Python package manager, `uv` installed. Please refer to the [`uv` install instructions](https://docs.astral.sh/uv/getting-started/installation/).
>
> Ensure that you set the full path to the `uv` binary and your Graphiti project folder.

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "transport": "stdio",
      "command": "/Users/<user>/.local/bin/uv",
      "args": [
        "run",
        "--isolated",
        "--directory",
        "/Users/<user>>/dev/zep/graphiti/mcp_server",
        "--project",
        ".",
        "graphiti_mcp_server.py",
        "--transport",
        "stdio"
      ],
      "env": {
        "NEO4J_URI": "bolt://localhost:7687",
        "NEO4J_USER": "neo4j",
        "NEO4J_PASSWORD": "password",
        "OPENAI_API_KEY": "sk-XXXXXXXX",
        "MODEL_NAME": "gpt-4.1-mini"
      }
    }
  }
}
```

For SSE transport (HTTP-based), you can use this configuration:

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "transport": "sse",
      "url": "http://localhost:8000/sse"
    }
  }
}
```

## 可用工具

Graphiti MCP 伺服器公開了以下工具：

- `add_episode`：向知識圖譜添加情節（支援文字、JSON 和訊息格式）
- `search_nodes`：在知識圖譜中搜尋相關節點摘要
- `search_facts`：在知識圖譜中搜尋相關事實（實體之間的邊）
- `delete_entity_edge`：從知識圖譜中刪除實體邊
- `delete_episode`：從知識圖譜中刪除情節
- `get_entity_edge`：通過其 UUID 獲取實體邊
- `get_episodes`：獲取特定群組的最新情節
- `clear_graph`：清除知識圖譜中的所有數據並重建索引
- `get_status`：獲取 Graphiti MCP 伺服器和 Neo4j 連接的狀態

### VS Code 整合工具（可選）

當安裝並配置了 VS Code UI Bridge 擴展時，以下額外工具可用：

- `vscode_get_context`：獲取當前 VS Code 上下文（工作區、分頁、編輯器、診斷、git 狀態）
- `vscode_open_file`：通過絕對路徑在 VS Code 中開啟檔案
- `vscode_reveal`：導航到檔案中的特定行和字符位置
- `vscode_apply_edit`：對檔案中的特定範圍應用文字編輯

## VS Code 整合設置

Graphiti MCP 伺服器包含可選的 VS Code 整合，透過 VS Code UI Bridge 擴展實現。這允許 AI 助手查看並與您當前的 VS Code 工作區互動。

### 先決條件

1. 在 VS Code 中安裝 VS Code UI Bridge 擴展
2. 擴展將啟動 WebSocket 伺服器（通常在 port 5310）
3. 從擴展的輸出面板記下 WebSocket URL 和 token

### 配置

設置 `VSCODE_UI_BRIDGE_WS` 環境變數：

```bash
# 本地開發
export VSCODE_UI_BRIDGE_WS="ws://127.0.0.1:5310?token=YOUR_TOKEN"

# Docker 部署
export VSCODE_UI_BRIDGE_WS="ws://host.docker.internal:5310?token=YOUR_TOKEN"
```

或將其添加到您的 `.env` 檔案中：

```
VSCODE_UI_BRIDGE_WS=ws://127.0.0.1:5310?token=YOUR_TOKEN
```

### 測試整合

您可以使用提供的測試腳本來測試 VS Code Bridge 連接：

```bash
uv run test_vscode_integration.py
```

這將驗證 WebSocket 連接是否正常工作，並顯示有關您當前 VS Code 工作區的資訊。

## 處理 JSON 數據

Graphiti MCP 伺服器可以透過 `add_episode` 工具使用 `source="json"` 處理結構化 JSON 數據。這
允許您自動從結構化數據中提取實體和關係：

```

add_episode(
name="Customer Profile",
episode_body="{\"company\": {\"name\": \"Acme Technologies\"}, \"products\": [{\"id\": \"P001\", \"name\": \"CloudSync\"}, {\"id\": \"P002\", \"name\": \"DataMiner\"}]}",
source="json",
source_description="CRM data"
)

```

## 範例：與 Augment 整合

要將 Graphiti MCP 伺服器與 Augment 整合，請按照以下步驟操作：

1. 啟動 Graphiti MCP 伺服器：

```bash
# 使用 uv 直接運行
uv run graphiti_mcp_server.py --group-id <your_group_id>

# 或使用 Docker
docker compose up
```

提示：指定 `group_id` 來為圖譜數據設置命名空間。如果您不指定 `group_id`，伺服器將使用 "default" 作為 group_id。

2. 配置 Augment 連接到 Graphiti MCP 伺服器。

對於 stdio 傳輸（預設）：
```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "uv",
      "args": ["run", "graphiti_mcp_server.py"],
      "cwd": "/path/to/graphiti/mcp_server"
    }
  }
}
```

對於 SSE 傳輸：
```json
{
  "mcpServers": {
    "graphiti-memory": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

3. 配置您的 AI 代理使用 Graphiti 使用指南。請參閱 [mcp_usage_guide.md](mcp_usage_guide.md) 了解詳細資訊。

4. 可選：如果您使用 VS Code，請設置 VS Code UI Bridge 整合以獲得上下文感知協助。

此整合使 Augment 中的 AI 助手能夠透過 Graphiti 的知識圖譜功能維護持久記憶，並在配置了 VS Code Bridge 時提供上下文感知的協助。

## 與 MCP 客戶端整合

### 使用 stdio 傳輸（推薦）

大多數 MCP 客戶端（如 Claude Desktop、Augment）支援 stdio 傳輸：

```json
{
  "mcpServers": {
    "graphiti-memory": {
      "command": "uv",
      "args": ["run", "graphiti_mcp_server.py"],
      "cwd": "/path/to/graphiti/mcp_server"
    }
  }
}
```

### 使用 SSE 傳輸（Docker 部署）

對於支援 SSE 的客戶端或需要遠端存取的情況：

1.  **運行 Graphiti MCP 伺服器使用 SSE 傳輸**：

    ```bash
    docker compose up
    ```

2.  **直接連接**（支援 SSE 的客戶端）：

    ```json
    {
      "mcpServers": {
        "graphiti-memory": {
          "url": "http://localhost:8000/sse"
        }
      }
    }
    ```

3.  **使用 mcp-remote 閘道**（不支援 SSE 的客戶端如 Claude Desktop）：

    安裝 mcp-remote（可選，npx 會自動處理）：
    ```bash
    npm install -g mcp-remote
    ```

    配置客戶端：
    ```json
    {
      "mcpServers": {
        "graphiti-memory": {
          "command": "npx",
          "args": [
            "mcp-remote",
            "http://localhost:8000/sse"
          ]
        }
      }
    }
    ```

    如果您已有 `mcpServers` 條目，請將 `graphiti-memory`（或您選擇的名稱）作為新鍵添加其中。

4.  **重新啟動您的 MCP 客戶端** 以使變更生效。

## 系統需求

- Python 3.10 或更高版本
- Neo4j 資料庫（需要 5.26 或更高版本）
- OpenAI API 金鑰（用於 LLM 操作和嵌入）
- MCP 相容客戶端

## 遙測

Graphiti MCP 伺服器使用 Graphiti 核心函式庫，其中包含匿名遙測收集。當您初始化 Graphiti MCP 伺服器時，會收集匿名使用統計資料以幫助改進框架。

### 收集的內容

- 匿名識別符和系統資訊（作業系統、Python 版本）
- Graphiti 版本和配置選擇（LLM 提供者、資料庫後端、嵌入器類型）
- **絕不收集個人數據、API 金鑰或實際圖譜內容**

### 如何停用

要在 MCP 伺服器中停用遙測，請設置環境變數：

```bash
export GRAPHITI_TELEMETRY_ENABLED=false
```

或將其添加到您的 `.env` 檔案中：

```
GRAPHITI_TELEMETRY_ENABLED=false
```

有關收集內容和原因的完整詳細資訊，請參閱 [主要 Graphiti README 中的遙測部分](../README.md#telemetry)。

## 授權

此專案使用與父專案 Graphiti 相同的授權。
