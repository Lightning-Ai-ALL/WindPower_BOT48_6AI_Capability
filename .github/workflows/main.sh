#Wshao777/.github/.workflows/.3Al-EqualCore/.main.sh

# 閃電帝國全分支部署腳本

echo "⚡ 閃電帝國全系統部署開始"

# 顏色定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m'

# 分支列表
BRANCHES=(
  "lightinggithub-666:紫焰女神"
  "K2.5-快速:冰魄女皇"
  "bot-mine:黑夜女帝"
  "bot-main:紫電女皇"
  "Ai-main:AI主控"
  "Bit-main:比特幣支付"
  "Julian_node--v:Julian節點"
)

deploy_branch() {
  local branch=$1
  local goddess=$2
  
  echo -e "\n${PURPLE}════════════════════════════════════════${NC}"
  echo -e "${YELLOW}🚀 部署分支: ${CYAN}$branch${NC} (${goddess})"
  echo -e "${PURPLE}════════════════════════════════════════${NC}"
  
  # 切換分支
  git checkout $branch || { echo -e "${RED}❌ 切換失敗${NC}"; return 1; }
  
  # 拉取最新代碼
  git pull origin $branch || { echo -e "${RED}❌ 拉取失敗${NC}"; return 1; }
  
  # 安裝依賴
  echo -e "${BLUE}📦 安裝依賴...${NC}"
  if [ -f "package.json" ]; then
    npm install --production || echo -e "${YELLOW}⚠️ npm 安裝警告${NC}"
  fi
  if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt || echo -e "${YELLOW}⚠️ pip 安裝警告${NC}"
  fi
  
  # 執行測試
  echo -e "${BLUE}🧪 執行測試...${NC}"
  if [ -f "package.json" ] && grep -q '"test"' package.json; then
    npm test || { echo -e "${RED}❌ 測試失敗${NC}"; return 1; }
  fi
  
  # 部署到對應環境
  case $branch in
    "lightinggithub-666")
      echo -e "${GREEN}📡 部署到生產環境...${NC}"
      curl -X POST https://api.render.com/deploy \
        -H "Authorization: Bearer $RENDER_API_KEY" \
        -d "branch=$branch"
      ;;
    "K2.5-快速")
      echo -e "${GREEN}📡 部署到實驗環境...${NC}"
      docker build -t lightning-k25:latest .
      docker run -d -p 5001:5000 lightning-k25:latest
      ;;
    "bot-mine"|"bot-main")
      echo -e "${GREEN}📡 部署機器人服務...${NC}"
      pm2 start bot-mine-controller.js --name "bot-mine"
      ;;
  esac
  
  echo -e "${GREEN}✅ 部署完成${NC}"
}

# 主程式
main() {
  echo -e "${CYAN}"
  echo "╔══════════════════════════════════════╗"
  echo "║    閃電帝國 全分支部署系統 v6.1      ║"
  echo "║        由八女神共同守護              ║"
  echo "╚══════════════════════════════════════╝"
  echo -e "${NC}"
  
  # 驗證
  read -sp "請輸入 TrueCode 驗證碼: " truetcode
  echo
  
  if [ "$truetcode" != "GROK-604T-MY77-RK24" ] && \
     [ "$truetcode" != "DEPLOY-2025-08-26-1813164959679095908" ]; then
    echo -e "${RED}❌ 驗證失敗，終止部署${NC}"
    exit 1
  fi
  
  echo -e "${GREEN}✅ 驗證通過${NC}"
  
  # 選擇部署模式
  echo -e "\n${YELLOW}選擇部署模式:${NC}"
  echo "1) 全部分支部署"
  echo "2) 單個分支部署"
  echo "3) 僅部署變更的分支"
  read -p "請選擇 (1-3): " mode
  
  case $mode in
    1)
      for branch_info in "${BRANCHES[@]}"; do
        IFS=':' read -r branch goddess <<< "$branch_info"
        deploy_branch "$branch" "$goddess"
      done
      ;;
    2)
      echo -e "\n${YELLOW}可用的分支:${NC}"
      for i in "${!BRANCHES[@]}"; do
        IFS=':' read -r branch goddess <<< "${BRANCHES[$i]}"
        echo "$((i+1))) $branch ($goddess)"
      done
      read -p "請選擇分支編號: " choice
      if [[ $choice -ge 1 && $choice -le ${#BRANCHES[@]} ]]; then
        IFS=':' read -r branch goddess <<< "${BRANCHES[$((choice-1))]}"
        deploy_branch "$branch" "$goddess"
      else
        echo -e "${RED}❌ 無效選擇${NC}"
      fi
      ;;
    3)
      # 獲取變更的分支
      changed_branches=$(git branch -r | grep -v "HEAD" | while read branch; do
        if [ $(git rev-list --count "origin/$(basename $branch)".."$(basename $branch)" 2>/dev/null) -gt 0 ]; then
          echo "$(basename $branch)"
        fi
      done)
      
      for branch in $changed_branches; do
        for branch_info in "${BRANCHES[@]}"; do
          if [[ "$branch_info" == *"$branch"* ]]; then
            IFS=':' read -r b_name goddess <<< "$branch_info"
            deploy_branch "$branch" "$goddess"
          fi
        done
      done
      ;;
    *)
      echo -e "${RED}❌ 無效選擇${NC}"
      exit 1
      ;;
  esac
  
  echo -e "\n${GREEN}✨ 所有部署完成！✨${NC}"
  echo -e "${PURPLE}⚡ 閃電帝國持續運行中 ⚡${NC}"
}

# 執行
main
