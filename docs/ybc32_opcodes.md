# YBC32 脚本操作码表 (150 个, 索引=操作码值)

来源: 脱壳镜像 0x624850 名字指针表 (VC6 debug 构建残留), 描述为光谱繁中版 Big5 原文
解释器: E:\CrossHermit\GAME\SRC\YOSHIMARU\YBC\YBC32.CPP

| 值 | 操作码 | 说明 (繁中原文) |
|---:|---|---|
| 0 | `CODE_TOP` | [ 特殊密碼 ] |
| 1 | `CODE_HINCLUDE` | 檔案包括範圍 |
| 2 | `CODE_DEFINE` | define定義 |
| 3 | `CODE_LABEL` | 標籤處理 |
| 4 | `CODE_CREATE` | 變數定義 |
| 5 | `CODE_SET1` | 變數內容更新    類比替換禁止↓１ |
| 6 | `CODE_SET2` | 變數計算更新    類比替換禁止↑２ |
| 7 | `CODE_SETRANDOM` | 在亂數上中加上變數 |
| 8 | `CODE_IFGOTO` | 條件分歧        類比替換禁止↓１ |
| 9 | `CODE_IFTHEN` | 條件分歧２      類比替換禁止↑２ |
| 10 | `CODE_IFEND` | [ ifend ] |
| 11 | `CODE_GOTO` | jump |
| 12 | `CODE_VWAIT` | wait |
| 13 | `CODE_VWAITKB` | wait Key Break |
| 14 | `CODE_VWAITKJ` | wait Key Jump |
| 15 | `CODE_SCRIPTEXEC` | script ＥＸＥ�d |
| 16 | `CODE_SCRIPTEXIT` | script ＥＸＩＴ |
| 17 | `CODE_TEXT` | 文件顯示（以一行為單位） |
| 18 | `CODE_TEXTINDEX` | 文件標題 |
| 19 | `CODE_END` | script結束 |
| 20 | `CODE_ADVMODESET` | 設定現在的角色模式 |
| 21 | `CODE_ALLOFF` | 不顯示所有的物件系統 |
| 22 | `CODE_BORDSET` | 設定面板狀態 |
| 23 | `CODE_BORDSETWAIT` | 設定面板狀態及等待顯示 |
| 24 | `CODE_BORDDISP` | 設定面板顯示模式 |
| 25 | `CODE_BORDWAIT` | 等待面板顯示 |
| 26 | `CODE_BORDCHANGE` | 面板風格調整 |
| 27 | `CODE_BORDONWAIT` | 顯示  面板    及  等待  顯示 |
| 28 | `CODE_BORDOFFWAIT` | 不顯示面板    及  不等待顯示 |
| 29 | `CODE_BORDPACKON` | 面板與角色的顯示設定 |
| 30 | `CODE_BORDPACKONWAIT` | 面板與角色的顯示設定  及  等待顯示 |
| 31 | `CODE_BORDPACKOFF` | 面板與角色的顯示設定 |
| 32 | `CODE_BORDPACKOFFWAIT` | 面板與角色的顯示設定  及  等待顯示 |
| 33 | `CODE_CHARSET` | 角色設定 |
| 34 | `CODE_CHARSETWAIT` | 角色設定  及  等待顯示 |
| 35 | `CODE_CHARDISP` | 角色顯示模式設定 |
| 36 | `CODE_CHARWAIT` | 等待角色顯示 |
| 37 | `CODE_CHARSWAPA` | 將角色排列在ID之間 |
| 38 | `CODE_CHARSWAPAWAIT` | 將角色排列在ID之間  及  等待顯示 |
| 39 | `CODE_CHARFACE` | 角色表情改變 |
| 40 | `CODE_CHARFACEWAIT` | 角色表情改變  及  等待顯示 |
| 41 | `CODE_CHARONWAIT` | 等待角色顯示 |
| 42 | `CODE_CHAROFFWAIT` | 等待角色不顯示 |
| 43 | `CODE_TEXTACTIVE` | 活動面板設定 |
| 44 | `CODE_TEXTCLEAR` | 將活動的文字訊息清除 |
| 45 | `CODE_TEXTFADEWAIT` | 訊息消失速度 |
| 46 | `CODE_TEXTPUTWAIT` | 顯示下一個訊息的間隔時間 |
| 47 | `CODE_TEXTFONT` | 字型大小 |
| 48 | `CODE_TEXTFONTRET` | 回復原先的字型大小 |
| 49 | `CODE_TEXTWAIT` | 等待文字訊息顯示 |
| 50 | `CODE_TEXTWAITKB` | 等待文字訊息顯示  及  鍵盤無效化 |
| 51 | `CODE_KEYWAIT` | 等待鍵盤 |
| 52 | `CODE_MOUSEHITGOTO` | 滑鼠範圍點擊檢查 |
| 53 | `CODE_MOUSEHITGOTOTABLE` | 滑鼠範圍點擊檢查表格 |
| 54 | `CODE_MOUSEHITGOTOEND` | 滑鼠範圍點擊檢查表格 |
| 55 | `CODE_FADESET` | 訊息消失控制 |
| 56 | `CODE_FADESETWAIT` | 訊息消失控制  及  等待處理 |
| 57 | `CODE_FADEWAIT` | 等待訊息消失 |
| 58 | `CODE_BGSET` | 顯示背景 |
| 59 | `CODE_BGSETWAIT` | 顯示背景  及  等待顯示 |
| 60 | `CODE_BGWAIT` | 等待背景顯示 |
| 61 | `CODE_MENU` | 選項 |
| 62 | `CODE_MENUEND` | 結束選擇 |
| 63 | `CODE_SE` | SE 音效開啟 |
| 64 | `CODE_SESTOP` | SE 關閉 |
| 65 | `CODE_BGM` | 背景音樂  開啟 |
| 66 | `CODE_BGMSTOP` | 背景音樂  關閉 |
| 67 | `CODE_VOICE` | 角色配音  開啟 |
| 68 | `CODE_VOICESTOP` | 角色配音  關閉 |
| 69 | `CODE_DRAWBINFREAD` | 讀取任意的組織ＢＩＮ |
| 70 | `CODE_DRAWOBJSETA` | 顯示定義 ID X Y No Pri |
| 71 | `CODE_DRAWOBJSETB` | 顯示定義 ID X Y No Pri CX CY CW CH |
| 72 | `CODE_DRAWOBJSETC` | 顯示定義 ID X Y No Pri CX CY CW CH SX SY |
| 73 | `CODE_DRAWOBJSETD` | 顯示定義 ID X Y No Pri CX CY CW CH A R G B |
| 74 | `CODE_DRAWOBJSETE` | 顯示定義 ID X Y No Pri A R G B |
| 75 | `CODE_DRAWOBJCLEAR` | 清除組織中的ID |
| 76 | `CODE_DRAWALLOBJCLEAR` | 清除組織中所有資料所有特徵 |
| 77 | `CODE_DRAWNOSET` | 組織重新設定  角色編號 |
| 78 | `CODE_DRAWPRIOSET` | 組織重新設定  優先權 |
| 79 | `CODE_DRAWSCALESET` | 組織重新設定  比例 |
| 80 | `CODE_DRAWPOSSET` | 組織重新設定  X Y 座標 |
| 81 | `CODE_DRAWRGBSET` | 組織重新設定  RGB |
| 82 | `CODE_DRAWALPHASET` | 組織重新設定  半透明速率設定 |
| 83 | `CODE_DRAWTEXTURESET` | 組織重新設定  CX CY CW CH |
| 84 | `CODE_GETADVCHARWK` | 以變數方式讀取  冒險角色工作 |
| 85 | `CODE_PUTADVCHARWK` | 寫入  冒險角色工作 |
| 86 | `CODE_GETADVEVENTWK` | 以變數方式讀取  冒險角色事件工作 |
| 87 | `CODE_PUTADVEVENTWK` | 寫入  冒險角色事件工作 |
| 88 | `CODE_GETITEMWK` | 以變數方式讀取  道具工作 |
| 89 | `CODE_PUTITEMWK` | 寫入  道具工作 |
| 90 | `CODE_GETUNITWK` | 以變數方式讀取  單位工作 |
| 91 | `CODE_PUTUNITWK` | 寫入  單位工作 |
| 92 | `CODE_GETSYSREG` | 以變數方式讀取  系統工作 |
| 93 | `CODE_PUTSYSREG` | 寫入  系統工作 |
| 94 | `CODE_SYSTEMREAD32` | 讀取  系統工作  32位元組 |
| 95 | `CODE_SYSTEMREAD16` | 讀取  系統工作  16位元組 |
| 96 | `CODE_SYSTEMREAD8` | 讀取  系統工作   8位元組 |
| 97 | `CODE_SYSTEMREADBIT` | 讀取  系統工作  BIT |
| 98 | `CODE_SYSTEMWRITE32` | 寫入  系統工作  32位元組 |
| 99 | `CODE_SYSTEMWRITE16` | 寫入  系統工作  16位元組 |
| 100 | `CODE_SYSTEMWRITE8` | 寫入  系統工作   8位元組 |
| 101 | `CODE_SYSTEMWRITEBIT` | 寫入  系統工作   BIT |
| 102 | `CODE_SENJYUTUREAD32` | 讀取  戰術工作  32位元組 |
| 103 | `CODE_SENJYUTUREAD16` | 讀取  戰術工作  16位元組 |
| 104 | `CODE_SENJYUTUREAD8` | 讀取  戰術工作   8位元組 |
| 105 | `CODE_SENJYUTUREADBIT` | 讀取  戰術工作  BIT |
| 106 | `CODE_SENJYUTUWRITE32` | 寫入  戰術工作  32位元組 |
| 107 | `CODE_SENJYUTUWRITE16` | 寫入  戰術工作  16位元組 |
| 108 | `CODE_SENJYUTUWRITE8` | 寫入  戰術工作   8位元組 |
| 109 | `CODE_SENJYUTUWRITEBIT` | 寫入  戰術工作  BIT |
| 110 | `CODE_UNIONREAD` | 共有  讀取 |
| 111 | `CODE_UNIONWRITE` | 共有  寫入 |
| 112 | `CODE_TACTGAMEEND` | 結束遊戲 |
| 113 | `CODE_TACTPLAYERAPPEAR` | 讓我方登場 |
| 114 | `CODE_TACTENEMYAPPEAR` | 讓敵方登場 |
| 115 | `CODE_TACTEVENTCELLSETSW` | 事件座標發動活性切換 |
| 116 | `CODE_TACTEVENTCELLWRITE` | 事件座標發動活性切換（置換角色經過的地點） |
| 117 | `CODE_TACTEVENTCELLWRITEPOS` | 事件座標發動活性切換（角色經過的地點） |
| 118 | `CODE_TACTSETDESTROYSCRIPT` | 全滅時的腳本指定 |
| 119 | `CODE_TACTFADEOUT` | 漸層停止顯示 |
| 120 | `CODE_TACTFADEIN` | 漸層開始顯示 |
| 121 | `CODE_TACTFADEWAIT` | 等待漸層顯示 |
| 122 | `CODE_TACTSCROLLSET` | 螢幕捲動設定 |
| 123 | `CODE_TACTSCROLLWAIT` | 等待螢幕捲動 |
| 124 | `CODE_TACTPLAYEREXIT` | 使我方退場 |
| 125 | `CODE_TACTENEMYEXIT` | 使敵方退場 |
| 126 | `CODE_TACTSETTIMERSCRIPT` | 以定時方式啟動腳本 |
| 127 | `CODE_TACTSETINTERVALSCRIPT` | 以一定間隔啟動不同腳本 |
| 128 | `CODE_TACTGETEVENTCELLPOS` | 讀取指定事件發動座標 |
| 129 | `CODE_TACTSETDESTROYSCRIPTSW` | 全滅確認 ON/OFF 切換 |
| 130 | `CODE_TACTPLAYERAPPEARGROUP` | 讓玩家角色群登場 |
| 131 | `CODE_TACTPLAYEREXITGROUP` | 讓玩家角色群退場 |
| 132 | `CODE_TACTENEMYAPPEARGROUP` | 讓敵方角色群登場 |
| 133 | `CODE_TACTENEMYEXITGROUP` | 讓敵方角色群退場 |
| 134 | `CODE_TACTPLAYERTHINKCHANGE` | 思考變更 |
| 135 | `CODE_TACTENEMYTHINKCHANGE` | 思考變更 |
| 136 | `CODE_TACTANIMPLAY` | 播放登錄動畫 |
| 137 | `CODE_TACTGETCNTEVENTCELLUNIT` | 存在於指定事件編號的單位數 |
| 138 | `CODE_TACTUNIONFUNCCALL` |  |
| 139 | `CODE_TACTANIMSET` |  |
| 140 | `CODE_TACTANIMSETCELL` |  |
| 141 | `CODE_TACTANIMSETUNIT` |  |
| 142 | `CODE_TACTANIMSTOP` |  |
| 143 | `CODE_TACTSETGAMECTRL` |  |
| 144 | `CODE_TACTSCROLLSETUNIT` |  |
| 145 | `CODE_TACTGETUNITPOS` |  |
| 146 | `CODE_NETKEYWAIT` | 連線遊戲中 CODE_VWAIT  通常  CODE_KEYWAIT |
| 147 | `CODE_GETTACTRET` | 讀取戰術結果 |
| 148 | `CODE_PUTTACTRET` | 讀取戰術結果 |
| 149 | `CODE_GETLASTMVP` | 讀取最終MVP角色編號 |
