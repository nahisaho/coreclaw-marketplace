#!/usr/bin/env bash
# setup-databases.sh — SHIDEN データベースのインストール
# 教育理論DB (theories.db) と学習指導要領DB (curriculum.db) を
# SHIDEN npm パッケージからセットアップします。
#
# Usage:
#   bash scripts/setup-databases.sh
#   bash scripts/setup-databases.sh --link   # シンボリックリンクで設置（省スペース）
#
# 前提条件: Node.js >= 20.0.0

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DATA_DIR="$SKILL_ROOT/data"
LINK_MODE=false

for arg in "$@"; do
  case "$arg" in
    --link) LINK_MODE=true ;;
    --help|-h)
      echo "Usage: bash scripts/setup-databases.sh [--link]"
      echo ""
      echo "Options:"
      echo "  --link  Use symlinks instead of copying (saves disk space)"
      echo ""
      echo "Installs SHIDEN education databases:"
      echo "  - theories.db      175 education theories (SQLite FTS5)"
      echo "  - theories.json    Theory data (JSON)"
      echo "  - relations.json   Theory relations graph"
      echo "  - curriculum.db    学習指導要領 (SQLite FTS5, ~140MB)"
      exit 0
      ;;
  esac
done

# ===== 1. Node.js チェック =====
if ! command -v node &>/dev/null; then
  echo "ERROR: Node.js が見つかりません。Node.js >= 20.0.0 をインストールしてください。"
  exit 1
fi

NODE_MAJOR=$(node -e "console.log(process.versions.node.split('.')[0])")
if [ "$NODE_MAJOR" -lt 20 ]; then
  echo "ERROR: Node.js >= 20.0.0 が必要です (現在: $(node -v))"
  exit 1
fi

# ===== 2. npm install (shiden パッケージ) =====
echo "📦 SHIDEN パッケージをインストール中..."
cd "$SKILL_ROOT"

if [ ! -f package.json ]; then
  echo "ERROR: package.json が見つかりません。先に package.json を確認してください。"
  exit 1
fi

npm install --no-audit --no-fund 2>&1 | tail -3

# ===== 3. SHIDEN データファイルの検出 =====
SHIDEN_DATA="$SKILL_ROOT/node_modules/shiden/src/data"

if [ ! -d "$SHIDEN_DATA" ]; then
  echo "ERROR: SHIDEN データディレクトリが見つかりません: $SHIDEN_DATA"
  echo "npm install が正常に完了しているか確認してください。"
  exit 1
fi

# 必須ファイルの確認
REQUIRED_FILES=("theories.db" "theories.json" "relations.json" "curriculum.db")
for f in "${REQUIRED_FILES[@]}"; do
  if [ ! -f "$SHIDEN_DATA/$f" ]; then
    echo "WARNING: $f が見つかりません（Git LFS 未ダウンロードの可能性あり）"
  fi
done

# ===== 4. data/ ディレクトリにデータベースを配置 =====
mkdir -p "$DATA_DIR"

echo "📂 データベースを data/ に配置中..."

for f in "${REQUIRED_FILES[@]}"; do
  src="$SHIDEN_DATA/$f"
  dst="$DATA_DIR/$f"

  if [ ! -f "$src" ]; then
    echo "  ⏭️  $f をスキップ（ソースが存在しません）"
    continue
  fi

  # 既存ファイルがある場合は確認
  if [ -e "$dst" ] || [ -L "$dst" ]; then
    echo "  🔄 $f を更新中..."
    rm -f "$dst"
  fi

  if [ "$LINK_MODE" = true ]; then
    ln -s "$src" "$dst"
    echo "  🔗 $f → シンボリックリンク作成"
  else
    cp "$src" "$dst"
    echo "  ✅ $f → コピー完了 ($(du -h "$dst" | cut -f1))"
  fi
done

# ===== 5. .gitignore に data/ を追加 =====
GITIGNORE="$SKILL_ROOT/.gitignore"
if [ ! -f "$GITIGNORE" ] || ! grep -q "^data/" "$GITIGNORE" 2>/dev/null; then
  echo "data/" >> "$GITIGNORE"
  echo "node_modules/" >> "$GITIGNORE"
  echo "📝 .gitignore に data/ と node_modules/ を追加"
fi

# ===== 6. 検証 =====
echo ""
echo "===== セットアップ結果 ====="

PASS=true
for f in "${REQUIRED_FILES[@]}"; do
  if [ -f "$DATA_DIR/$f" ] || [ -L "$DATA_DIR/$f" ]; then
    SIZE=$(du -h "$DATA_DIR/$f" | cut -f1)
    echo "  ✅ $f ($SIZE)"
  else
    echo "  ❌ $f が見つかりません"
    PASS=false
  fi
done

echo ""
if [ "$PASS" = true ]; then
  echo "🎉 セットアップ完了！"
  echo ""
  echo "利用可能なCLIコマンド:"
  echo "  npx shiden theories search \"構成主義\"     # 教育理論を検索"
  echo "  npx shiden theories categories            # カテゴリ一覧"
  echo "  npx shiden curriculum search \"プログラミング\" # 学習指導要領を検索"
  echo "  npx shiden curriculum subject 算数         # 教科別検索"
else
  echo "⚠️  一部のファイルが不足しています。"
  echo "curriculum.db が不足する場合は Git LFS が必要です。"
  echo "  npm pack shiden  # で確認するか、SHIDEN リポジトリを直接参照してください。"
fi
