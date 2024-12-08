def getFilePath(profile: str, docType: str, idx: int) -> str:
    return f"./data/{profile}/{idx}{docType}.txt"


def preprocessBotConvo(text: str) -> str:
    return "\n".join(
        line.replace("Użytkownik:", "") for line in text.split("\n") if "?" not in line)
