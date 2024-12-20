import requests
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import queue
import random
import time

INSTAGRAM_HEADERS = {
    "Host": "www.instagram.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/119.0.3945.117 Safari/537.36",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "X-IG-App-ID": "936619743392459",
    "X-ASBD-ID": "198387",
    "X-IG-WWW-Claim": "0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://www.instagram.com",
    "Connection": "keep-alive",
    "Referer": "https://www.instagram.com/",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
}

stop_event = threading.Event()

class InstagramCheckerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Instagram Username Checker")

        self.session = requests.Session()
        self.session.headers.update(INSTAGRAM_HEADERS)

        self.usernames_list = []
        self.proxies_list = []
        self.available_usernames = []

        self.num_threads = tk.IntVar(value=5)
        self.delay_var = tk.DoubleVar(value=1.0)
        self.max_retries = tk.IntVar(value=3)

        self.available_count = 0
        self.unavailable_count = 0
        self.error_count = 0

        top_frame = tk.Frame(master)
        top_frame.pack(side="top", fill="x", padx=10, pady=5)

        self.btn_usernames = tk.Button(top_frame, text="Load Usernames", command=self.load_usernames, width=14)
        self.btn_usernames.grid(row=0, column=0, padx=5, pady=5)

        self.btn_proxies = tk.Button(top_frame, text="Load Proxies", command=self.load_proxies, width=14)
        self.btn_proxies.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(top_frame, text="Threads:").grid(row=0, column=2, sticky="e")
        self.entry_threads = tk.Entry(top_frame, textvariable=self.num_threads, width=5)
        self.entry_threads.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        tk.Label(top_frame, text="Delay(s):").grid(row=0, column=4, sticky="e")
        self.entry_delay = tk.Entry(top_frame, textvariable=self.delay_var, width=5)
        self.entry_delay.grid(row=0, column=5, padx=5, pady=5, sticky="w")

        tk.Label(top_frame, text="Max Retries:").grid(row=0, column=6, sticky="e")
        self.entry_retries = tk.Entry(top_frame, textvariable=self.max_retries, width=5)
        self.entry_retries.grid(row=0, column=7, padx=5, pady=5, sticky="w")

        self.btn_start = tk.Button(top_frame, text="Start", command=self.start_check, width=8)
        self.btn_start.grid(row=0, column=8, padx=5, pady=5)

        self.btn_stop = tk.Button(top_frame, text="Stop", command=self.stop_check, state="disabled", width=8)
        self.btn_stop.grid(row=0, column=9, padx=5, pady=5)

        self.btn_save_lists = tk.Button(top_frame, text="Save Lists", command=self.save_available_list, width=10)
        self.btn_save_lists.grid(row=0, column=10, padx=5, pady=5)

        text_frame = tk.Frame(master)
        text_frame.pack(side="top", fill="both", expand=True, padx=10, pady=(0,10))

        self.result_text = tk.Text(text_frame, height=20, width=120)
        self.result_text.pack(side="left", fill="both", expand=True)
        self.result_text.config(state="disabled")

        scroll = tk.Scrollbar(text_frame, command=self.result_text.yview)
        scroll.pack(side="right", fill="y")
        self.result_text.config(yscrollcommand=scroll.set)

    def load_usernames(self):
        file_path = filedialog.askopenfilename(
            title="Select Usernames File",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.usernames_list = [line.strip() for line in f if line.strip()]
                messagebox.showinfo("Success", f"Loaded {len(self.usernames_list)} usernames.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load usernames.\nError: {str(e)}")

    def load_proxies(self):
        file_path = filedialog.askopenfilename(
            title="Select Proxies File",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.proxies_list = [line.strip() for line in f if line.strip()]
                messagebox.showinfo("Success", f"Loaded {len(self.proxies_list)} proxies.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load proxies.\nError: {str(e)}")

    def start_check(self):
        if not self.usernames_list:
            messagebox.showwarning("Warning", "Please load usernames first.")
            return
        if not self.proxies_list:
            messagebox.showwarning("Warning", "Please load proxies first.")
            return

        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        stop_event.clear()

        self.available_count = 0
        self.unavailable_count = 0
        self.error_count = 0
        self.available_usernames.clear()

        try:
            threads_count = int(self.entry_threads.get())
        except ValueError:
            threads_count = 5

        self.usernames_queue = queue.Queue()
        for username in self.usernames_list:
            self.usernames_queue.put(username)

        self.threads = []
        for _ in range(threads_count):
            t = threading.Thread(target=self.worker)
            t.daemon = True
            t.start()
            self.threads.append(t)

        threading.Thread(target=self.wait_for_completion, daemon=True).start()

    def wait_for_completion(self):
        for t in self.threads:
            t.join()

        if not stop_event.is_set():
            self.update_text("\nAll done!", "blue")

        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")

        summary = (
            f"\nAvailable: {self.available_count}, "
            f"Not Available: {self.unavailable_count}, "
            f"Errors: {self.error_count}"
        )
        self.update_text(summary + "\n", "purple")

    def stop_check(self):
        stop_event.set()
        self.btn_stop.config(state="disabled")

    def worker(self):
        while not stop_event.is_set():
            try:
                username = self.usernames_queue.get_nowait()
            except queue.Empty:
                break

            proxy_str = random.choice(self.proxies_list)
            max_retries = self.max_retries.get()
            result = self.check_username_with_retry(username, proxy_str, max_retries)

            if result is True:
                self.available_count += 1
                self.update_text(f"[+] {username} => Available\n", "green")
                self.available_usernames.append(username)
                self.save_result(username, "available.txt")

            elif result is False:
                self.unavailable_count += 1
                self.update_text(f"[-] {username} => Not Available\n", "red")
                self.save_result(username, "not_available.txt")

            else:
                self.error_count += 1
                self.update_text(f"[!] {username} => Error Checking\n", "orange")
                # Removed saving to "error.txt" here

            self.usernames_queue.task_done()
            time.sleep(float(self.delay_var.get()))

    def check_username_with_retry(self, username, proxy_str, max_retries):
        for _ in range(max_retries):
            if stop_event.is_set():
                return None
            result = self.check_username(username, proxy_str)
            if result is not None:
                return result
            else:
                try:
                    self.proxies_list.remove(proxy_str)
                except ValueError:
                    pass
                if self.proxies_list:
                    proxy_str = random.choice(self.proxies_list)
                else:
                    return None
                time.sleep(1)
        return None

    def check_username(self, username, proxy_str):
        proxy_type, proxy_addr = self.parse_proxy(proxy_str)
        proxies = {
            "http": f"{proxy_type}://{proxy_addr}",
            "https": f"{proxy_type}://{proxy_addr}",
        }
        url = f"https://www.instagram.com/{username}/"
        try:
            resp = self.session.get(url, proxies=proxies, timeout=10, allow_redirects=True)
            if resp.status_code == 404:
                return True
            elif resp.status_code == 200:
                if "sorry, this page isn't available" in resp.text.lower():
                    return True
                else:
                    return False
            elif resp.status_code == 429:
                return None
            else:
                return None
        except:
            return None

    def parse_proxy(self, proxy_str):
        proxy_type = "http"
        proxy_addr = proxy_str
        if "://" in proxy_str:
            ptype, paddr = proxy_str.split("://", 1)
            proxy_type = ptype.strip()
            proxy_addr = paddr.strip()
        return proxy_type, proxy_addr

    def update_text(self, text, color="black"):
        def _update():
            self.result_text.config(state="normal")
            self.result_text.insert("end", text)
            self.result_text.tag_add(color, "end-1c linestart", "end-1c lineend")
            self.result_text.tag_config(color, foreground=color)
            self.result_text.see("end")
            self.result_text.config(state="disabled")
        self.master.after(0, _update)

    def save_result(self, username, filename):
        try:
            with open(filename, "a", encoding="utf-8") as f:
                f.write(username + "\n")
        except:
            pass

    def save_available_list(self):
        if not self.available_usernames:
            messagebox.showinfo("Info", "No available usernames yet.")
            return
        file_path = filedialog.asksaveasfilename(
            title="Save Available Usernames",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    for user in self.available_usernames:
                        f.write(user + "\n")
                messagebox.showinfo("Success", "Available usernames saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file.\nError: {str(e)}")

def main():
    root = tk.Tk()
    app = InstagramCheckerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
