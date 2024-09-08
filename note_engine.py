from llama_index.core.tools import FunctionTool
import os


note_file = os.path.join("data", "notes.txt")


def save_note(note):
    print("Saving note:", note)
    try:
        # Check if the input is a dictionary and extract the content
        if isinstance(note, dict):
            note_title = note.get('title', '')
            note_content = note.get('content', '')  
        else:
            note_content = note

        # Ensure the directory exists
        os.makedirs(os.path.dirname(note_file), exist_ok=True)

        # Open the file in append mode and write the note 
        with open(note_file, "a") as f:
            f.write(note_content + "\n")

        print("Successfully saved the note to", note_file)

        return "note saved"

    except Exception as e:
        print("An error occurred while saving the note:", str(e))
        return f"An error occurred: {str(e)}"

note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="""This tool saves a note when the user asks for saving a note. The user can save any content they want. The tool is designed to be used in the LLM context.""",
)
