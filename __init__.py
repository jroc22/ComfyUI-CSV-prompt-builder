from .build_prompt_from_csv import BuildPromptFromCSV

NODE_CLASS_MAPPINGS = {
    "BuildPromptFromCSV": BuildPromptFromCSV,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "BuildPromptFromCSV": "Build Prompt From CSV",
}

__all__ = ['BuildPromptFromCSV']
