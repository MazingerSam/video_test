"""一鍵開啟與重連 Google Colab GPU 伺服器工具 (Colab Reconnect Helper)"""

import os
import sys
import webbrowser
from src.colab_client import ColabVideoClient, ENV_FILE

COLAB_NOTEBOOK_URL = "https://colab.research.google.com/github/MazingerSam/video_test/blob/main/notebooks/colab_ai_video_workflow.ipynb"

def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except Exception:
            pass

    client = ColabVideoClient()
    print("=" * 65)
    print("🎬 Google Colab GPU 遠端伺服器重啟與連線工具")
    print("=" * 65)

    # 1. 檢查目前設定之連線狀態
    if client.colab_url:
        print(f"[*] 目前設定的連線網址: {client.colab_url}")
        print("[*] 正在測試連線狀態...")
        try:
            status = client.check_health()
            print("[OK] 連線正常！Colab GPU 正在線上運行中。")
            print(f"     GPU 裝置: {status.get('gpu', '未知')}")
            print(f"     常駐模型: {', '.join(status.get('models_loaded', []))}")
            choice = input("\n是否要更換為新的連線網址？(y/N): ").strip().lower()
            if choice != 'y':
                print("[*] 保留現有連線，結束程式。")
                return
        except Exception as e:
            print(f"[!] 目前連線已失效或 Colab 已離線 (原因: {e})")
    else:
        print("[!] 尚未設定任何 Colab 連線網址。")

    # 2. 引導重啟 Colab
    print("\n" + "-" * 65)
    print("【重啟 Colab 3 步驟】:")
    print(" 1. 正在為您在瀏覽器開啟 Colab 筆記本...")
    print(f"    網址: {COLAB_NOTEBOOK_URL}")
    webbrowser.open(COLAB_NOTEBOOK_URL)
    print(" 2. 在 Colab 頁面點擊選單:「執行階段 (Runtime)」➔「全部執行 (Run all)」(快捷鍵 Ctrl+F9)")
    print(" 3. 待步驟 3 執行完成後，複製終端輸出的 https://xxxx.trycloudflare.com 網址")
    print("-" * 65 + "\n")

    # 3. 提示輸入新網址
    new_url = input("請在此貼上新的 Cloudflare Tunnel 連線網址: ").strip()
    if not new_url:
        print("[!] 未輸入網址，取消連線。")
        return

    try:
        client.set_colab_url(new_url)
        status = client.check_health()
        print("\n" + "=" * 65)
        print("🎉 恭喜！已成功連接至 Google Colab GPU 伺服器！")
        print(f"   連線網址: {new_url}")
        print(f"   GPU 規格: {status.get('gpu', '未知')}")
        print(f"   常駐模型: {', '.join(status.get('models_loaded', []))}")
        print(f"   設定已存入: {ENV_FILE}")
        print("=" * 65)
    except Exception as e:
        print(f"\n[X] 連線失敗: {e}")
        print("    請確認 Colab 步驟 3 儲存格是否仍在執行中。")

if __name__ == "__main__":
    main()
