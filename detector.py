from pathlib import Path
from magika import Magika

magika = Magika()

LABEL_TO_EXT = {
    "javascript": ".js",
    "typescript": ".ts",
    "python": ".py",
    "html": ".html",
    "css": ".css",
    "json": ".json",
    "markdown": ".md",
    "shell": ".sh",
    "batch": ".bat",
    "xml": ".xml",
    "c": ".c",
    "cpp": ".cpp",
    "csharp": ".cs",
    "java": ".java",
    "rust": ".rs",
    "go": ".go",
    "php": ".php",
    "ruby": ".rb",
    "yaml": ".yaml",
    "jpeg": ".jpg",
    "powershell": ".ps1",
}

def detect_file_extention(file_path: Path) -> str | None:
    if not file_path.is_file():
        return None
    
    try:
        result = magika.identify_path(file_path)
        label = result.output.ct_label

        if label in LABEL_TO_EXT:
            return LABEL_TO_EXT[label]

        if label in ("txt", "unknown", "text"):
            return None

        if result.output.score >= 0.5:
            return f".{label}"

    except Exception:
        return None

    return None