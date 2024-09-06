from llama_index.core.tools import FunctionTool
import os


note_file = os.path.join("data", "notes.txt")


def save_note(note):
    try:
        if not os.path.exists(note_file):
            open(note_file, "w")

        with open(note_file, "a") as f:
            f.writelines([note + "\n"])

        return "note saved"

    except Exception as e:
        return False


note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="""This powerful note engine allows users to create, save and manage 
    their notes in a structured format. With its ability to export notes to files, 
    users can easily store and retrieve their important information, making it a 
    reliable tool for personal or professional use. Whether you're looking to keep 
    track of ideas, jot down reminders, or maintain a journal, this note engine is 
    designed to simplify the process and provide a seamless experience.""",
)
