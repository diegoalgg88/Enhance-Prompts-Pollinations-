import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, filedialog
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any
from datetime import datetime
import sys

from config.config_manager import ConfigManager
from core.api_client import SecureAPIClient

class PromptEnhancerGUI:
    """Modern GUI whose interface is dynamically generated from a prompts file."""

    def __init__(self, config: ConfigManager, logger, api_token: str, prompts_data: Dict) -> None:
        """Initializes the GUI.

        Args:
            config: The application's configuration manager.
            logger: The application's logger.
            api_token: The user's API token.
            prompts_data: The data for the prompts.
        """
        self.config = config
        self.logger = logger
        self.api_token = api_token
        self.prompts_data = prompts_data
        self.api_client = SecureAPIClient(config, logger, self.prompts_data)

        self.root = tk.Tk()
        self.root.title("AI Prompt Enhancer v2.5.0")
        width = config.getint('APP', 'window_width', 900)
        height = config.getint('APP', 'window_height', 700)
        self.root.geometry(f"{width}x{height}")
        self.root.state('zoomed')
        self.root.minsize(600, 500)

        self.setup_styles()

        self.status_var = tk.StringVar(value="Ready")
        self.history_limit = config.getint('APP', 'max_history', 100)

        self.prompt_types = list(self.prompts_data.keys())
        self.selected_type = tk.StringVar(value=self.prompt_types[0])

        self.conversations = {pt: [] for pt in self.prompt_types}
        self.prompt_histories = {pt: [] for pt in self.prompt_types}
        self.last_enhanced_prompts = {
            pt: "" for pt in self.prompt_types}

        self.create_menu()
        self.create_widgets()
        self.setup_event_handlers()

        self.executor = ThreadPoolExecutor(
            max_workers=2, thread_name_prefix="PromptEnhancer")
        self.logger.info(
            "Application initialized. Prompts loaded from JSON.")
        self.on_type_change()

    def setup_styles(self) -> None:
        """Sets up the styles for the GUI."""
        style = ttk.Style(self.root)
        try:
            if sys.platform == "win32":
                style.theme_use('winnative')
            elif sys.platform == "darwin":
                style.theme_use('aqua')
            else:
                style.theme_use('clam')
        except tk.TclError:
            style.theme_use('clam')
        style.configure('TButton', padding=(10, 5), font=('Arial', 10))
        style.configure('Primary.TButton', font=('Arial', 10, 'bold'))
        style.configure('TRadiobutton', font=('Arial', 9))

    def create_menu(self) -> None:
        """Creates the main menu of the application."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(
            label="View Category History", command=self.show_history_window)
        file_menu.add_command(
            label="Export Category Conversation", command=self.export_history)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        menubar.add_cascade(label="File", menu=file_menu)
        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_help)
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_widgets(self) -> None:
        """Creates the main widgets of the application."""
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        self.create_input_frame(main_frame)
        self.create_chat_frame(main_frame)
        self.create_status_bar()
        self.setup_text_tags()

    def create_input_frame(self, parent: ttk.Frame) -> None:
        """Creates the input frame with the prompt text and controls."""
        input_container = ttk.Frame(parent)
        input_container.pack(fill=tk.X, pady=(0, 15))
        prompt_frame = ttk.LabelFrame(
            input_container, text="Prompt Input", padding="10")
        prompt_frame.pack(fill=tk.X, expand=True)
        self.prompt_text = tk.Text(prompt_frame, height=5, wrap=tk.WORD, font=(
            'Arial', 11), relief=tk.SOLID, borderwidth=1)
        self.prompt_text.pack(fill=tk.X, expand=True)
        self.prompt_text.focus()
        controls_frame = ttk.Frame(input_container, padding=(0, 10))
        controls_frame.pack(fill=tk.X)
        type_selector_frame = ttk.LabelFrame(
            controls_frame, text="Enhancement Type", padding=(10, 5))
        type_selector_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        for p_type in self.prompt_types:
            rb = ttk.Radiobutton(type_selector_frame, text=p_type, variable=self.selected_type,
                                 value=p_type, command=self.on_type_change, style='TRadiobutton')
            rb.pack(side=tk.LEFT, padx=5, pady=2, anchor='w')
        btn_frame = ttk.Frame(controls_frame)
        btn_frame.pack(side=tk.RIGHT, anchor='e')

        self.enhance_btn = ttk.Button(
            btn_frame, text="Enhance Prompt", command=self.enhance_prompt, style='Primary.TButton')
        self.enhance_btn.grid(row=0, column=0, padx=(10, 5), pady=5)

        self.copy_btn = ttk.Button(
            btn_frame, text="Copy Result", command=self.copy_last_prompt, state=tk.DISABLED)
        self.copy_btn.grid(row=0, column=1, padx=5, pady=5)

        clear_hist_btn = ttk.Button(
            btn_frame, text="Clear History", command=self.clear_history)
        clear_hist_btn.grid(row=0, column=2, padx=(5, 0), pady=5)

        close_btn = ttk.Button(
            btn_frame, text="Close", command=self.on_closing)
        close_btn.grid(row=1, column=0, columnspan=3, pady=(5, 0))

    def create_chat_frame(self, parent: ttk.Frame) -> None:
        """Creates the chat frame with the conversation history."""
        chat_frame = ttk.LabelFrame(
            parent, text="Conversation History", padding="10")
        chat_frame.pack(fill=tk.BOTH, expand=True)
        self.chat_history = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, state=tk.DISABLED, font=('Arial', 10), relief=tk.SOLID, borderwidth=1)
        self.chat_history.pack(fill=tk.BOTH, expand=True)
        self.create_chat_context_menu()

    def create_status_bar(self) -> None:
        """Creates the status bar at the bottom of the application."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)

        self.progress_bar = ttk.Progressbar(status_frame, mode='indeterminate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(0, 5))

        status_label = ttk.Label(status_frame, textvariable=self.status_var)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        self.progress_bar.pack_forget()

    def setup_text_tags(self) -> None:
        """Sets up the text tags for the chat history."""
        self.chat_history.tag_config(
            'user', foreground='blue', font=('Arial', 10, 'bold'))
        self.chat_history.tag_config('enhanced', foreground='green')
        self.chat_history.tag_config(
            'error', foreground='red', font=('Arial', 10, 'bold'))
        self.chat_history.tag_config(
            'timestamp', foreground='gray', font=('Arial', 8))

    def create_chat_context_menu(self) -> None:
        """Creates the context menu for the chat history."""
        self.chat_menu = tk.Menu(self.root, tearoff=0)
        self.chat_menu.add_command(label="Copy", command=self.copy_selection)
        self.chat_menu.add_separator()
        self.chat_menu.add_command(
            label="Export Category History", command=self.export_history)
        self.chat_menu.add_command(
            label="Clear Category History", command=self.clear_history)

    def setup_event_handlers(self) -> None:
        """Sets up the event handlers for the application."""
        self.root.bind('<Control-Return>', lambda e: self.enhance_prompt())
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.chat_history.bind(
            '<Button-3>', lambda e: self.chat_menu.tk_popup(e.x_root, e.y_root))

    def on_type_change(self, event=None) -> None:
        """Handles the change of the prompt type."""
        current_type = self.selected_type.get()
        self.display_history_for_type(current_type)
        self.copy_btn.config(
            state=tk.NORMAL if self.last_enhanced_prompts[current_type] else tk.DISABLED)
        self.status_var.set(f"Category '{current_type}' active. Ready.")

    def display_history_for_type(self, prompt_type: str) -> None:
        """Displays the history for the given prompt type."""
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete('1.0', tk.END)
        conversation_log = self.conversations.get(prompt_type, [])
        for timestamp, message, tag, add_ts in conversation_log:
            self.chat_history.insert(
                tk.END, f"[{timestamp}] " if add_ts else "", "timestamp")
            self.chat_history.insert(tk.END, f"{message}\n\n", tag)
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)

    def update_chat_history(self, message: str, tag: str, add_timestamp: bool = True) -> None:
        """Updates the chat history with a new message."""
        current_type = self.selected_type.get()
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_entry = (timestamp, message, tag, add_timestamp)
        self.conversations[current_type].append(log_entry)

        def _update():
            self.chat_history.config(state=tk.NORMAL)
            if add_timestamp:
                self.chat_history.insert(
                    tk.END, f"[{timestamp}] ", "timestamp")
            self.chat_history.insert(tk.END, f"{message}\n\n", tag)
            self.chat_history.config(state=tk.DISABLED)
            self.chat_history.see(tk.END)
        self.root.after(0, _update)

    def enhance_prompt(self) -> None:
        """Enhances the user's prompt."""
        user_prompt = self.prompt_text.get('1.0', tk.END).strip()
        if not user_prompt:
            messagebox.showwarning(
                "Input Required", "Please enter a prompt to enhance.", parent=self.root)
            return
        current_type = self.selected_type.get()
        self.enhance_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.status_var.set(f"Enhancing '{current_type}' prompt...")
        self.progress_bar.pack(side=tk.RIGHT, padx=(0, 5))
        self.progress_bar.start(10)
        self.update_chat_history(f"Original Prompt: {user_prompt}", "user")
        self.executor.submit(self._enhance_prompt_worker,
                             user_prompt, self.api_token, current_type)

    def _enhance_prompt_worker(self, prompt: str, token: str, prompt_type: str) -> None:
        """Worker thread for enhancing the prompt."""
        result = self.api_client.enhance_prompt(prompt, token, prompt_type)
        self.root.after(0, self._handle_enhancement_result,
                        result, prompt_type)

    def run(self) -> None:
        """Runs the main loop of the application."""
        try:
            self.root.mainloop()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("Application closing.")
        finally:
            if hasattr(self, 'executor') and not self.executor._shutdown:
                self.executor.shutdown(wait=False, cancel_futures=True)

    def _handle_enhancement_result(self, result: Dict[str, Any], prompt_type: str) -> None:
        """Handles the result of the prompt enhancement."""
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.enhance_btn.config(state=tk.NORMAL)
        current_type_on_gui = self.selected_type.get()
        is_still_on_same_type = (current_type_on_gui == prompt_type)
        if result.get('success'):
            enhanced_prompt = result['enhanced_prompt']
            self.last_enhanced_prompts[prompt_type] = enhanced_prompt
            self.prompt_histories[prompt_type].append(enhanced_prompt)
            if len(self.prompt_histories[prompt_type]) > self.history_limit:
                self.prompt_histories[prompt_type].pop(0)
            log_entry = (datetime.now().strftime(
                '%H:%M:%S'), f"Enhanced Result:\n{enhanced_prompt}", "enhanced", False)
            self.conversations[prompt_type].append(log_entry)
            if is_still_on_same_type:
                self.display_history_for_type(prompt_type)
                self.status_var.set(
                    f"Prompt '{prompt_type}' enhanced successfully.")
                self.copy_btn.config(state=tk.NORMAL)
                self.prompt_text.delete('1.0', tk.END)
        else:
            error_message = result.get(
                'error', 'An unknown error occurred.')
            log_entry = (datetime.now().strftime('%H:%M:%S'),
                         f"Error: {error_message}", "error", False)
            self.conversations[prompt_type].append(log_entry)
            if is_still_on_same_type:
                self.display_history_for_type(prompt_type)
                self.status_var.set(
                    f"Error in '{prompt_type}': {error_message}")
                messagebox.showerror("Enhancement Failed",
                                     error_message, parent=self.root)

    def clear_history(self) -> None:
        """Clears the history of the current category."""
        current_type = self.selected_type.get()
        if messagebox.askyesno("Confirm Clear", f"Are you sure you want to permanently delete the history for the category '{current_type}'?", icon='warning', parent=self.root):
            self.conversations[current_type].clear()
            self.prompt_histories[current_type].clear()
            self.last_enhanced_prompts[current_type] = ""
            self.display_history_for_type(current_type)
            self.copy_btn.config(state=tk.DISABLED)
            self.status_var.set(f"History for '{current_type}' cleared.")
            self.logger.info(
                f"History for category '{current_type}' cleared by user.")

    def copy_last_prompt(self) -> None:
        """Copies the last enhanced prompt to the clipboard."""
        current_type = self.selected_type.get()
        last_prompt = self.last_enhanced_prompts[current_type]
        if last_prompt:
            self.root.clipboard_clear()
            self.root.clipboard_append(last_prompt)
            self.status_var.set("Enhanced result copied to clipboard.")
        else:
            self.status_var.set(
                "No result to copy in this category.")

    def copy_selection(self) -> None:
        """Copies the selected text from the chat history to the clipboard."""
        try:
            selected = self.chat_history.selection_get()
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
            self.status_var.set("Selection copied to clipboard.")
        except tk.TclError:
            pass

    def export_history(self) -> None:
        """Exports the history of the current category to a text file."""
        current_type = self.selected_type.get()
        conversation_log = self.conversations.get(current_type, [])
        if not conversation_log:
            messagebox.showwarning(
                "Empty Export", "There is no history to export in this category.", parent=self.root)
            return
        content = "\n\n".join(
            [f"[{ts}] {msg}" if add_ts else msg for ts, msg, _, add_ts in conversation_log])
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[
            ("Text Files", "*.txt"), ("Markdown Files", "*.md")], title=f"Export History for '{current_type}'", parent=self.root)
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.status_var.set(f"History exported to {filename}")
            except Exception as e:
                self.logger.error(f"Error exporting history: {e}")
                messagebox.showerror(
                    "Export Error", f"Could not export history: {e}", parent=self.root)

    def show_history_window(self):
        """Shows a window with the history of enhanced prompts for the current category."""
        current_type = self.selected_type.get()
        current_history = self.prompt_histories[current_type]
        if not current_history:
            messagebox.showinfo(
                "History", f"No enhanced prompts in the category '{current_type}'.", parent=self.root)
            return
        history_win = tk.Toplevel(self.root)
        history_win.title(f"Prompt History - {current_type}")
        history_win.geometry("500x400")
        history_win.transient(self.root)
        history_win.grab_set()
        listbox = tk.Listbox(history_win, font=(
            'Arial', 10), relief=tk.SOLID, borderwidth=1)
        scrollbar = ttk.Scrollbar(
            history_win, orient=tk.VERTICAL, command=listbox.yview)
        listbox.config(yscrollcommand=scrollbar.set)
        for prompt in current_history:
            listbox.insert(tk.END, " " + prompt.replace('\n',
                                                         ' ').strip()[:80] + '...')
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        btn_frame = ttk.Frame(history_win, padding="10")
        btn_frame.pack(fill=tk.X)
        view_btn = ttk.Button(
            btn_frame, text="View Full", state=tk.DISABLED)
        reuse_btn = ttk.Button(btn_frame, text="Reuse", state=tk.DISABLED)
        copy_hist_btn = ttk.Button(
            btn_frame, text="Copy", state=tk.DISABLED)
        view_btn.pack(side=tk.LEFT, expand=True, padx=5)
        reuse_btn.pack(side=tk.LEFT, expand=True, padx=5)
        copy_hist_btn.pack(side=tk.LEFT, expand=True, padx=5)

        def on_select(event):
            selected_indices = listbox.curselection()
            if not selected_indices:
                return
            idx = selected_indices[0]
            full_prompt = current_history[idx]
            view_btn.config(state=tk.NORMAL, command=lambda: messagebox.showinfo(
                "Full Prompt", full_prompt, parent=history_win))
            copy_hist_btn.config(state=tk.NORMAL, command=lambda: (self.root.clipboard_clear(), self.root.clipboard_append(
                full_prompt), self.status_var.set("Prompt from history copied."), history_win.destroy()))
            reuse_btn.config(state=tk.NORMAL, command=lambda: (self.prompt_text.delete(
                '1.0', tk.END), self.prompt_text.insert('1.0', full_prompt), history_win.destroy()))
        listbox.bind("<<ListboxSelect>>", on_select)
        self.root.wait_window(history_win)

    def show_help(self) -> None:
        """Shows the about dialog."""
        messagebox.showinfo(
            "About", "Pollinations.ai Prompt Enhancer v2.5.0\n\nCreado por Diego Gonzalez\nContacto: diegoalgg88@gmail.com\n\nTool to enhance prompts using AI, with customizable categories from prompts.json.", parent=self.root)

    def on_closing(self) -> None:
        """Handles the closing of the application."""
        if messagebox.askokcancel("Exit", "Do you want to exit the application?", parent=self.root, icon='question'):
            self.executor.shutdown(wait=False, cancel_futures=True)
            self.root.destroy()

    def run(self) -> None:
        """Runs the main loop of the application."""
        try:
            self.root.mainloop()
        except (KeyboardInterrupt, SystemExit):
            self.logger.info("Application closing.")
        finally:
            if hasattr(self, 'executor') and not self.executor._shutdown:
                self.executor.shutdown(wait=False, cancel_futures=True)
