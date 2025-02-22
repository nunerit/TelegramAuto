import os
import time
import shutil
import subprocess
import asyncio
import math
import ctypes
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.errors import SessionPasswordNeededError

# --- CẤU HÌNH BAN ĐẦU (DEFAULT) ---
CONFIG_FILE = "config.txt"
DEFAULT_TELEGRAM_PATH = r"C:\Users\SAM\AppData\Roaming\Telegram Desktop\Telegram.exe"
API_ID = 22379547      # API_ID của bạn
API_HASH = '9fc2845bde4b64a6a51320a8045c8178'  # API_HASH của bạn

# --- THÔNG TIN VERSION & BẢN QUYỀN ---
VERSION_INFO = "Version 1.0 - Copyright SAMADS"

# --- NGÔN NGỮ ---
languages = {
    "vi": {
        "title": "Công cụ Tự động Telegram TData",
        "choose_folder": "Chọn thư mục",
        "save_path": "💾 Lưu đường dẫn",
        "login_all": "🔐 Đăng nhập Tất cả",
        "update_privacy": "🚀 Cập nhật Quyền riêng tư",
        "copy_telegram": "📋 Copy Telegram Portable",
        "open_telegram": "🟢 Mở Telegram Copies",
        "close_telegram": "❌ Đóng All Telegram",
        "arrange_telegram": "🟣 Sắp xếp Telegram",
        "stats_label": "Bảng thống kê thư mục con:",
        "account_summary": "Thống kê tài khoản:",
        "logged_accounts": "Tài khoản đã đăng nhập:",
        "log_label": "Tiến trình:",
        "telegram_path_label": "Đường dẫn Telegram:",
        "lang_select_title": "Chọn ngôn ngữ",
        "lang_vi": "Tiếng Việt",
        "lang_en": "English",
        "lang_zh": "中文",
        "msg_saved_path": "Đã lưu đường dẫn vào máy!",
        "msg_error_path": "Đường dẫn không hợp lệ!",
        "msg_copy_result": "Kết quả Copy",
        "msg_open_result": "Kết quả mở Telegram",
        "msg_login_complete": "Quá trình đăng nhập cho tất cả các tài khoản đã hoàn tất.",
        "msg_privacy_complete": "Đã cập nhật quyền riêng tư cho tất cả các tài khoản.",
        "already_logged": "Đã có session",
        "success": "Thành công",
        "failure": "Thất bại",
        "not_found": "Chưa có",
        "otp_prompt": "Nhập mã OTP gửi tới {phone}:",
        "phone_prompt": "Nhập số điện thoại cho tài khoản ở\n{folder}:",
        "2fa_error": "Không tìm thấy mật khẩu 2FA tự động cho {phone}.",
        "copy_success": "Copy telegram.exe thành công cho {phone}",
        "copy_skip": "{phone} đã có telegram.exe, bỏ qua.",
        "close_result": "Đóng All Telegram:\nĐã đóng: {closed}\nLỗi: {errors}",
        "arrange_result": "Đã sắp xếp {count} cửa sổ Telegram."
    },
    "en": {
        "title": "Telegram TData Auto Tool",
        "choose_folder": "Choose Folder",
        "save_path": "💾 Save Path",
        "login_all": "🔐 Login All",
        "update_privacy": "🚀 Update Privacy",
        "copy_telegram": "📋 Copy Telegram Portable",
        "open_telegram": "🟢 Open Telegram Copies",
        "close_telegram": "❌ Close All Telegram",
        "arrange_telegram": "🟣 Arrange Telegram",
        "stats_label": "Folder Statistics:",
        "account_summary": "Account Summary:",
        "logged_accounts": "Logged In Accounts:",
        "log_label": "Log:",
        "telegram_path_label": "Telegram Path:",
        "lang_select_title": "Select Language",
        "lang_vi": "Tiếng Việt",
        "lang_en": "English",
        "lang_zh": "中文",
        "msg_saved_path": "Path saved successfully!",
        "msg_error_path": "Invalid path!",
        "msg_copy_result": "Copy Result",
        "msg_open_result": "Telegram Open Result",
        "msg_login_complete": "Login process completed for all accounts.",
        "msg_privacy_complete": "Privacy updated for all accounts.",
        "already_logged": "Already Logged In",
        "success": "Success",
        "failure": "Failure",
        "not_found": "Not Found",
        "otp_prompt": "Enter OTP sent to {phone}:",
        "phone_prompt": "Enter phone number for account in\n{folder}:",
        "2fa_error": "No automatic 2FA password found for {phone}.",
        "copy_success": "Copied telegram.exe successfully for {phone}",
        "copy_skip": "{phone} already has telegram.exe, skipped.",
        "close_result": "Close All Telegram:\nClosed: {closed}\nErrors: {errors}",
        "arrange_result": "Arranged {count} Telegram windows."
    },
    "zh": {
        "title": "Telegram TData 自动工具",
        "choose_folder": "选择文件夹",
        "save_path": "💾 保存路径",
        "login_all": "🔐 全部登录",
        "update_privacy": "🚀 更新隐私",
        "copy_telegram": "📋 复制 Telegram Portable",
        "open_telegram": "🟢 打开 Telegram 副本",
        "close_telegram": "❌ 关闭所有 Telegram",
        "arrange_telegram": "🟣 排列 Telegram",
        "stats_label": "文件夹统计：",
        "account_summary": "账户统计：",
        "logged_accounts": "已登录账户：",
        "log_label": "日志：",
        "telegram_path_label": "Telegram 路径：",
        "lang_select_title": "选择语言",
        "lang_vi": "Tiếng Việt",
        "lang_en": "English",
        "lang_zh": "中文",
        "msg_saved_path": "路径保存成功！",
        "msg_error_path": "路径无效！",
        "msg_copy_result": "复制结果",
        "msg_open_result": "打开 Telegram 结果",
        "msg_login_complete": "所有账户登录流程已完成。",
        "msg_privacy_complete": "所有账户隐私更新成功。",
        "already_logged": "已存在会话",
        "success": "成功",
        "failure": "失败",
        "not_found": "未找到",
        "otp_prompt": "请输入发送至 {phone} 的 OTP：",
        "phone_prompt": "请输入账户所在文件夹 {folder} 的电话号码：",
        "2fa_error": "未自动找到 {phone} 的2FA密码。",
        "copy_success": "成功复制 telegram.exe 给 {phone}",
        "copy_skip": "{phone} 已有 telegram.exe，跳过。",
        "close_result": "关闭所有 Telegram:\n已关闭: {closed}\n错误: {errors}",
        "arrange_result": "排列了 {count} 个 Telegram 窗口。"
    }
}

# Global language dictionary (will be set after language selection)
lang = {}

# --- GIAO DIỆN CHỌN NGÔN NGỮ ---
def select_language():
    def set_language():
        global lang
        selected = language_var.get()
        lang = languages[selected]
        lang_window.destroy()
        init_main_ui()
    lang_window = tk.Tk()
    lang_window.title(languages["en"]["lang_select_title"])
    tk.Label(lang_window, text="Select Language / 选择语言 / Chọn ngôn ngữ:", font=("Arial", 12)).pack(pady=10)
    language_var = tk.StringVar(value="en")
    for code in ["vi", "en", "zh"]:
        tk.Radiobutton(lang_window, text=languages[code]["lang_" + code], variable=language_var, value=code, font=("Arial", 10)).pack(anchor="w", padx=20)
    # Hiển thị thông tin version & bản quyền trong cửa sổ chọn ngôn ngữ
    tk.Label(lang_window, text=VERSION_INFO, font=("Arial", 8)).pack(pady=5)
    tk.Button(lang_window, text="OK", command=set_language, font=("Arial", 10)).pack(pady=10)
    lang_window.mainloop()

# --- CHỨC NĂNG SẮP XẾP CỬA SỔ (STAGGERED/OVERLAPPING GRID) ---
def arrange_telegram_windows():
    """
    Sắp xếp các cửa sổ Telegram theo kiểu Staggered/Overlapping Grid.
    Các cửa sổ được xếp thành lưới với kích thước ô tính theo độ phân giải màn hình.
    Mỗi cửa sổ sẽ có kích thước 120% của ô lưới và các hàng lẻ được dịch chuyển theo X (offset 30% của ô) tạo hiệu ứng xen kẽ.
    Delay 1 giây giữa các lần di chuyển. Loại trừ cửa sổ của tool (root).
    """
    user32 = ctypes.windll.user32
    handles = []
    my_hwnd = root.winfo_id()  # Loại trừ cửa sổ tool

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    def enum_callback(hwnd, lParam):
        if hwnd == my_hwnd:
            return True
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            user32.GetWindowTextW(hwnd, buff, length + 1)
            title = buff.value
            if ("Telegram" in title or "telegram" in title) and (title != lang["title"]):
                handles.append(hwnd)
        return True

    user32.EnumWindows(enum_callback, 0)
    n = len(handles)
    if n == 0:
        messagebox.showinfo("Arrange", "Không tìm thấy cửa sổ Telegram nào.")
        return

    cols = math.ceil(math.sqrt(n))
    rows = math.ceil(n / cols)
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    cell_width = screen_width / cols
    cell_height = screen_height / rows
    win_width = int(cell_width * 1.2)
    win_height = int(cell_height * 1.2)
    stagger_offset = int(cell_width * 0.3)

    for i, hwnd in enumerate(handles):
        row = i // cols
        col = i % cols
        base_x = int(col * cell_width)
        base_y = int(row * cell_height)
        if row % 2 == 1:
            x = base_x + stagger_offset
        else:
            x = base_x
        y = base_y
        user32.MoveWindow(hwnd, x, y, win_width, win_height, True)
        log_message(f"Di chuyển cửa sổ (HWND: {hwnd}) đến ({x},{y}) với kích thước ({win_width}x{win_height})")
        time.sleep(1)
    messagebox.showinfo("Arrange", lang["arrange_result"].format(count=n))
    log_message(lang["arrange_result"].format(count=n))

# --- CÁC CHỨC NĂNG KHÁC ---

def log_message(msg):
    text_log.insert(tk.END, msg + "\n")
    text_log.see(tk.END)

def save_path():
    folder_path = entry_path.get()
    if os.path.exists(folder_path):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            f.write(folder_path)
        messagebox.showinfo("Lưu thành công", lang["msg_saved_path"])
        update_stats()
        update_logged()
    else:
        messagebox.showerror("Lỗi", lang["msg_error_path"])

def load_path():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return ""

def browse_folder():
    folder_selected = filedialog.askdirectory()
    entry_path.delete(0, tk.END)
    entry_path.insert(0, folder_selected)

def update_stats():
    folder_path = entry_path.get()
    try:
        subfolders = [d for d in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, d))]
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đọc thư mục: {e}")
        return
    info_list = []
    for sub in subfolders:
        sub_path = os.path.join(folder_path, sub)
        tdata_count = sum(1 for item in os.listdir(sub_path)
                          if item.lower() == 'tdata' and os.path.isdir(os.path.join(sub_path, item)))
        info_list.append(f"- {sub}: có {tdata_count} tdata folder(s)")
    info_text = "\n".join(info_list) if info_list else "Không có thư mục con nào."
    text_stats.delete("1.0", tk.END)
    text_stats.insert(tk.END, info_text)

def update_logged():
    tdata_dir = entry_path.get()
    logged_list = []
    for folder in get_tdata_folders(tdata_dir):
        session_path = os.path.join(folder, "session")
        if os.path.exists(session_path):
            logged_list.append(os.path.basename(folder))
    text_logged.delete("1.0", tk.END)
    if logged_list:
        text_logged.insert(tk.END, ", ".join(logged_list))
    else:
        text_logged.insert(tk.END, lang["not_found"])

def get_tdata_folders(main_dir):
    return [os.path.join(main_dir, f) for f in os.listdir(main_dir)
            if os.path.isdir(os.path.join(main_dir, f))]

def open_telegram_with_tdata(tdata_folder):
    tdata_path = os.path.join(tdata_folder, "tdata")
    if os.path.exists(tdata_path):
        log_message(f"🟢 Đang mở Telegram: {tdata_folder}")
        subprocess.Popen([telegram_path_entry.get(), "-workdir", tdata_path])
        time.sleep(1)

def find_password_candidates(tdata_folder):
    candidates = []
    for root_dir, dirs, files in os.walk(tdata_folder):
        for file in files:
            if file.lower().endswith('.txt'):
                path = os.path.join(root_dir, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read().strip()
                    if content and len(content) <= 100:
                        candidates.append((file, content))
                except Exception as e:
                    log_message(f"Lỗi đọc file {path}: {e}")
    return candidates

async def async_login(session_path, phone, tdata_folder):
    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.connect()
    if not await client.is_user_authorized():
        try:
            await client.send_code_request(phone)
            log_message(f"Đã gửi OTP cho {phone}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Gửi mã OTP thất bại cho {phone}: {e}")
            await client.disconnect()
            return False
        otp = simpledialog.askstring("OTP", lang["otp_prompt"].format(phone=phone), parent=root)
        if not otp:
            messagebox.showerror("Lỗi", "Không nhập OTP.")
            await client.disconnect()
            return False
        try:
            await client.sign_in(phone, otp)
            log_message(f"Đăng nhập thành công cho {phone} (không 2FA)")
        except SessionPasswordNeededError:
            candidates = find_password_candidates(tdata_folder)
            if len(candidates) == 0:
                messagebox.showerror("Lỗi", lang["2fa_error"].format(phone=phone))
                await client.disconnect()
                return False
            else:
                password = candidates[0][1]
                log_message(f"Tự động sử dụng mật khẩu từ file '{candidates[0][0]}' cho {phone}.")
            try:
                await client.sign_in(password=password)
                log_message(f"Đăng nhập thành công cho {phone} (2FA)")
            except Exception as e:
                messagebox.showerror("Lỗi", f"Đăng nhập 2FA thất bại cho {phone}: {e}")
                await client.disconnect()
                return False
        except Exception as e:
            messagebox.showerror("Lỗi", f"Đăng nhập thất bại cho {phone}: {e}")
            await client.disconnect()
            return False
    await client.disconnect()
    return True

def login_account(tdata_folder):
    session_path = os.path.join(tdata_folder, "session")
    phone = os.path.basename(tdata_folder)
    if os.path.exists(session_path):
        log_message(f"🔸 {phone} đã có session, bỏ qua đăng nhập.")
        return True
    if not phone:
        phone = simpledialog.askstring("Phone", lang["phone_prompt"].format(folder=tdata_folder), parent=root)
        if not phone:
            messagebox.showerror("Lỗi", "Không có số điện thoại, bỏ qua tài khoản này.")
            return False
    open_telegram_with_tdata(tdata_folder)
    result = asyncio.run(async_login(session_path, phone, tdata_folder))
    if result:
        messagebox.showinfo("Thành công", f"Đăng nhập thành công cho {phone}")
        log_message(f"✅ {phone} đăng nhập thành công.")
    else:
        log_message(f"❌ {phone} đăng nhập thất bại.")
    return result

def login_all_accounts():
    tdata_dir = entry_path.get()
    if not os.path.exists(tdata_dir):
        messagebox.showerror("Lỗi", lang["msg_error_path"])
        return
    tdata_folders = get_tdata_folders(tdata_dir)
    login_success = []
    login_failure = []
    already_logged = []
    for folder in tdata_folders:
        phone = os.path.basename(folder)
        session_path = os.path.join(folder, "session")
        if os.path.exists(session_path):
            already_logged.append(phone)
            log_message(f"🔸 {phone} đã có session, bỏ qua đăng nhập.")
        else:
            if login_account(folder):
                login_success.append(phone)
            else:
                login_failure.append(phone)
    summary = f"{lang['already_logged']}: {len(already_logged)}\n{lang['success']} new: {len(login_success)}\n{lang['failure']}: {len(login_failure)}\n"
    if already_logged:
        summary += f"{lang['already_logged']}: " + ", ".join(already_logged) + "\n"
    if login_success:
        summary += f"{lang['success']}: " + ", ".join(login_success) + "\n"
    if login_failure:
        summary += f"{lang['failure']}: " + ", ".join(login_failure)
    text_summary.delete("1.0", tk.END)
    text_summary.insert(tk.END, summary)
    update_logged()
    messagebox.showinfo("Hoàn thành", lang["msg_login_complete"])
    log_message("Đã hoàn tất đăng nhập tất cả các tài khoản.")

async def update_privacy(session_path):
    client = TelegramClient(session_path, API_ID, API_HASH)
    await client.connect()
    try:
        await client(functions.account.SetPrivacyRequest(
            key=types.InputPrivacyKeyPhoneNumber(),
            rules=[types.InputPrivacyValueDisallowAll()]
        ))
        if hasattr(types, "InputPrivacyKeyCalls"):
            await client(functions.account.SetPrivacyRequest(
                key=types.InputPrivacyKeyCalls(),
                rules=[types.InputPrivacyValueDisallowAll()]
            ))
        else:
            log_message("InputPrivacyKeyCalls không khả dụng, bỏ qua cập nhật quyền riêng tư cho cuộc gọi.")
        log_message(f"✅ Cập nhật quyền riêng tư thành công cho session {session_path}")
    except Exception as e:
        log_message(f"❌ Lỗi cập nhật quyền riêng tư cho session {session_path}: {e}")
    await client.disconnect()

def run_tool():
    tdata_dir = entry_path.get()
    if not os.path.exists(tdata_dir):
        messagebox.showerror("Lỗi", lang["msg_error_path"])
        return
    tdata_folders = get_tdata_folders(tdata_dir)
    for folder in tdata_folders:
        open_telegram_with_tdata(folder)
    time.sleep(10)
    for folder in tdata_folders:
        session_path = os.path.join(folder, "session")
        try:
            asyncio.run(update_privacy(session_path))
        except Exception as e:
            log_message(f"❌ Lỗi cập nhật quyền riêng tư cho {folder}: {e}")
    messagebox.showinfo("Hoàn thành", lang["msg_privacy_complete"])
    log_message("Đã hoàn tất cập nhật quyền riêng tư cho tất cả các tài khoản.")

def copy_telegram_portable():
    tdata_dir = entry_path.get()
    if not os.path.exists(tdata_dir):
        messagebox.showerror("Lỗi", lang["msg_error_path"])
        return
    tdata_folders = get_tdata_folders(tdata_dir)
    copied = []
    skipped = []
    errors = []
    for folder in tdata_folders:
        target_path = os.path.join(folder, "telegram.exe")
        phone = os.path.basename(folder)
        if not os.path.exists(target_path):
            try:
                shutil.copy(telegram_path_entry.get(), target_path)
                copied.append(phone)
                log_message(lang["copy_success"].format(phone=phone))
            except Exception as e:
                errors.append(f"{phone}: {str(e)}")
                log_message(f"❌ Lỗi copy telegram.exe cho {phone}: {e}")
        else:
            skipped.append(phone)
            log_message(lang["copy_skip"].format(phone=phone))
    summary = f"Đã copy: {len(copied)}\nBỏ qua: {len(skipped)}\nLỗi: {len(errors)}\n"
    if copied:
        summary += "Đã copy: " + ", ".join(copied) + "\n"
    if skipped:
        summary += "Bỏ qua: " + ", ".join(skipped) + "\n"
    if errors:
        summary += "Lỗi: " + "; ".join(errors)
    messagebox.showinfo(lang["msg_copy_result"], summary)

def open_telegram_copies():
    tdata_dir = entry_path.get()
    if not os.path.exists(tdata_dir):
        messagebox.showerror("Lỗi", lang["msg_error_path"])
        return
    tdata_folders = get_tdata_folders(tdata_dir)
    opened = []
    not_found = []
    for folder in tdata_folders:
        target_path = os.path.join(folder, "telegram.exe")
        phone = os.path.basename(folder)
        if os.path.exists(target_path):
            log_message(f"Mở telegram.exe từ {folder}")
            subprocess.Popen([target_path])
            opened.append(phone)
            time.sleep(1)  # Delay 1s cho mỗi cửa sổ
        else:
            not_found.append(phone)
            log_message(f"Không tìm thấy telegram.exe trong {folder}")
    summary = f"Đã mở: {len(opened)}\nKhông tìm thấy: {len(not_found)}\n"
    if opened:
        summary += "Đã mở: " + ", ".join(opened) + "\n"
    if not_found:
        summary += "Không tìm thấy: " + ", ".join(not_found)
    messagebox.showinfo(lang["msg_open_result"], summary)

def close_all_telegram():
    try:
        result = subprocess.run(["tasklist", "/FI", "IMAGENAME eq Telegram.exe", "/FO", "CSV"], capture_output=True, text=True)
        output = result.stdout.strip().splitlines()
        pids = []
        for line in output[1:]:
            parts = line.replace('"','').split(',')
            if len(parts) >= 2:
                pids.append(parts[1])
        closed = []
        errors = []
        for pid in pids:
            try:
                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, text=True)
                closed.append(pid)
                time.sleep(1)  # Delay 1 giây giữa các lần đóng
            except Exception as e:
                errors.append(f"PID {pid}: {e}")
        summary = lang["close_result"].format(closed=", ".join(closed) if closed else "None",
                                               errors="; ".join(errors) if errors else "None")
        log_message(summary)
        messagebox.showinfo("Close Result", summary)
    except Exception as e:
        messagebox.showerror("Lỗi", f"Không thể đóng các tiến trình Telegram: {e}")

# --- MAIN UI ---
def init_main_ui():
    global root, entry_path, text_stats, text_logged, text_summary, text_log, telegram_path_entry

    root = tk.Tk()
    root.title(lang["title"])
    root.geometry("650x800")

    label_title = tk.Label(root, text=lang["title"], font=("Arial", 14, "bold"))
    label_title.pack(pady=10)

    # Frame chọn thư mục chứa TData
    frame_path = tk.Frame(root)
    frame_path.pack(pady=5)
    entry_path = tk.Entry(frame_path, width=50)
    entry_path.pack(side=tk.LEFT, padx=5)
    btn_browse = tk.Button(frame_path, text=lang["choose_folder"], command=browse_folder)
    btn_browse.pack(side=tk.LEFT)

    # Frame nhập đường dẫn Telegram Portable
    frame_telegram_path = tk.Frame(root)
    frame_telegram_path.pack(pady=5)
    tk.Label(frame_telegram_path, text=lang["telegram_path_label"]).pack(side=tk.LEFT, padx=5)
    telegram_path_entry = tk.Entry(frame_telegram_path, width=50)
    telegram_path_entry.insert(0, DEFAULT_TELEGRAM_PATH)
    telegram_path_entry.pack(side=tk.LEFT, padx=5)

    btn_save = tk.Button(root, text=lang["save_path"], command=save_path, width=20)
    btn_save.pack(pady=5)

    # Frame chứa các nút chức năng, chia thành 2 hàng
    frame_buttons = tk.Frame(root)
    frame_buttons.pack(pady=5)
    # Hàng 0
    btn_login_all = tk.Button(frame_buttons, text=lang["login_all"], command=login_all_accounts, width=18)
    btn_login_all.grid(row=0, column=0, padx=5, pady=5)
    btn_run = tk.Button(frame_buttons, text=lang["update_privacy"], command=run_tool, width=18, bg="green", fg="white")
    btn_run.grid(row=0, column=1, padx=5, pady=5)
    btn_copy = tk.Button(frame_buttons, text=lang["copy_telegram"], command=copy_telegram_portable, width=18)
    btn_copy.grid(row=0, column=2, padx=5, pady=5)
    btn_open = tk.Button(frame_buttons, text=lang["open_telegram"], command=open_telegram_copies, width=18)
    btn_open.grid(row=0, column=3, padx=5, pady=5)
    # Hàng 1
    btn_close = tk.Button(frame_buttons, text=lang["close_telegram"], command=close_all_telegram, width=18)
    btn_close.grid(row=1, column=0, padx=5, pady=5)
    btn_arrange = tk.Button(frame_buttons, text=lang["arrange_telegram"], command=arrange_telegram_windows, width=18)
    btn_arrange.grid(row=1, column=1, padx=5, pady=5)
    # Nếu cần thêm nút thì có thể thêm ở hàng 1

    frame_stats = tk.Frame(root)
    frame_stats.pack(pady=10)
    label_stats = tk.Label(frame_stats, text=lang["stats_label"])
    label_stats.pack()
    text_stats = tk.Text(frame_stats, width=70, height=10)
    text_stats.pack()

    frame_summary = tk.Frame(root)
    frame_summary.pack(pady=10)
    label_summary = tk.Label(frame_summary, text=lang["account_summary"])
    label_summary.pack()
    text_summary = tk.Text(frame_summary, width=70, height=5)
    text_summary.pack()

    frame_logged = tk.Frame(root)
    frame_logged.pack(pady=10)
    label_logged = tk.Label(frame_logged, text=lang["logged_accounts"])
    label_logged.pack()
    text_logged = tk.Text(frame_logged, width=70, height=5)
    text_logged.pack()

    frame_log = tk.Frame(root)
    frame_log.pack(pady=10)
    label_log = tk.Label(frame_log, text=lang["log_label"])
    label_log.pack()
    text_log = tk.Text(frame_log, width=70, height=10)
    text_log.pack()

    saved_path = load_path()
    if saved_path:
        entry_path.insert(0, saved_path)
        update_stats()
        update_logged()

    root.mainloop()

# --- KHỞI ĐỘNG CHỌN NGÔN NGỮ ---
def select_language():
    def set_language():
        global lang
        selected = language_var.get()
        lang = languages[selected]
        lang_window.destroy()
        init_main_ui()
    lang_window = tk.Tk()
    lang_window.title(languages["en"]["lang_select_title"])
    tk.Label(lang_window, text="Select Language / 选择语言 / Chọn ngôn ngữ:", font=("Arial", 12)).pack(pady=10)
    language_var = tk.StringVar(value="en")
    for code in ["vi", "en", "zh"]:
        tk.Radiobutton(lang_window, text=languages[code]["lang_" + code], variable=language_var, value=code, font=("Arial", 10)).pack(anchor="w", padx=20)
    # Thông tin version & bản quyền hiện trong cửa sổ chọn ngôn ngữ
    tk.Label(lang_window, text=VERSION_INFO, font=("Arial", 8)).pack(pady=5)
    tk.Button(lang_window, text="OK", command=set_language, font=("Arial", 10)).pack(pady=10)
    lang_window.mainloop()

# --- MAIN ---
select_language()
