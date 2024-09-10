import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from llm_core.agent_builder import build_agent  # Import the agent builder function

# Initialize history as a list of dictionaries
history = []


def add_to_history(prompt, response):
    history.append({"prompt": prompt, "response": response})
    if len(history) > 5:
        history.pop(0)


def get_relevant_history():
    return "\n".join(
        [
            f"Prompt: {entry['prompt']}\nResponse: {entry['response']}"
            for entry in history
        ]
    )


def show_loading_bar():
    loading_label.config(text="Loading, please wait...")
    progress_bar.start(10)
    root.update_idletasks()


def hide_loading_bar():
    progress_bar.stop()
    loading_label.pack_forget()
    progress_bar.pack_forget()


def add_pdf():
    file_path = filedialog.askopenfilename(
        filetypes=[("PDF files", "*.pdf")], title="Select a PDF file"
    )
    if file_path:
        messagebox.showinfo("PDF Added", f"Added PDF: {file_path}")


def submit_prompt():
    prompt = prompt_entry.get()
    if prompt.strip():
        chat_text.insert(tk.END, f"User: {prompt}\n", "user")
        relevant_history = get_relevant_history()

        # Disable the submit button and show loading message
        submit_button.config(state=tk.DISABLED)
        loading_label.config(text="Processing, please wait...")

        def process_prompt():
            # Query the agent with the current prompt and relevant history
            result = agent.query(
                f"Here is the relevant history:\n{relevant_history}\n\nNew prompt: {prompt}"
            )
            # Add the current interaction to history
            add_to_history(prompt, result)
            # Update the chat with the result
            chat_text.insert(tk.END, f"Bot: {result}\n", "bot")
            prompt_entry.delete(0, tk.END)

            # Re-enable the submit button and clear loading message
            submit_button.config(state=tk.NORMAL)
            loading_label.config(text="")

        # Start processing in a separate thread
        threading.Thread(target=process_prompt).start()


def clear_chat():
    chat_text.delete(1.0, tk.END)


def on_hover(event, widget, color):
    widget.config(bg=color)


def on_leave(event, widget, color):
    widget.config(bg=color)


def disable_interface():
    prompt_entry.config(state=tk.DISABLED)
    add_pdf_button.config(state=tk.DISABLED)
    clear_button.config(state=tk.DISABLED)
    submit_button.config(state=tk.DISABLED)


def enable_interface():
    prompt_entry.config(state=tk.NORMAL)
    add_pdf_button.config(state=tk.NORMAL)
    clear_button.config(state=tk.NORMAL)
    submit_button.config(state=tk.NORMAL)


def build_agent_thread():
    global agent
    show_loading_bar()
    agent = build_agent()  # Build the agent
    hide_loading_bar()
    show_main_components()


def show_main_components():
    chat_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=5)
    prompt_entry.pack(fill=tk.X, padx=10, pady=5)
    button_frame.pack(fill=tk.X, padx=10, pady=5)


def create_main_window():
  global root, prompt_entry, chat_text, loading_label, progress_bar
  global add_pdf_button, clear_button, submit_button, chat_frame, button_frame

  root = tk.Tk()
  root.title("Modern Chatbot Interface")
  root.geometry("600x500")
  root.configure(bg="#2c2f33")

  loading_label = tk.Label(root, text="", fg="#ffcccb", bg="#2c2f33")
  loading_label.pack(pady=5)

  progress_bar = ttk.Progressbar(root, mode="indeterminate")
  progress_bar.pack(pady=5)

  chat_frame = tk.Frame(root, bg="#2c2f33")

  chat_text = tk.Text(
      chat_frame,
      wrap=tk.WORD,
      state=tk.NORMAL,
      bg="#23272a",
      fg="#ffffff",
      bd=0,
      padx=10,
      pady=10,
  )
  chat_text.pack(expand=True, fill=tk.BOTH)
  chat_text.tag_config("user", foreground="#7289da")
  chat_text.tag_config("bot", foreground="#43b581")

  prompt_entry = tk.Entry(
      root, width=50, bg="#40444b", fg="#ffffff", insertbackground="#ffffff", bd=0
  )
  prompt_entry.pack(fill=tk.X, padx=10, pady=5)

  # Bind the Enter key to the submit_prompt function
  prompt_entry.bind("<Return>", lambda event: submit_prompt())

  button_frame = tk.Frame(root, bg="#2c2f33")

  add_pdf_button = tk.Button(
      button_frame, text="Add PDF", command=add_pdf, bg="#7289da", fg="#ffffff", bd=0
  )
  add_pdf_button.pack(side=tk.LEFT, padx=5)
  add_pdf_button.bind("<Enter>", lambda e: on_hover(e, add_pdf_button, "#5b6eae"))
  add_pdf_button.bind("<Leave>", lambda e: on_leave(e, add_pdf_button, "#7289da"))

  clear_button = tk.Button(
      button_frame, text="Clear", command=clear_chat, bg="#7289da", fg="#ffffff", bd=0
  )
  clear_button.pack(side=tk.LEFT, padx=5)
  clear_button.bind("<Enter>", lambda e: on_hover(e, clear_button, "#5b6eae"))
  clear_button.bind("<Leave>", lambda e: on_leave(e, clear_button, "#7289da"))

  submit_button = tk.Button(
      button_frame,
      text="Submit",
      command=submit_prompt,
      bg="#7289da",
      fg="#ffffff",
      bd=0,
  )
  submit_button.pack(side=tk.RIGHT, padx=5)
  submit_button.bind("<Enter>", lambda e: on_hover(e, submit_button, "#5b6eae"))
  submit_button.bind("<Leave>", lambda e: on_leave(e, submit_button, "#7289da"))

  # Start the agent building process in a separate thread
  threading.Thread(target=build_agent_thread).start()

  root.mainloop()

if __name__ == "__main__":
    create_main_window()
