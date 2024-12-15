def getFilePath(profile: str, docType: str, idx: int) -> str:
    return f"./data/{profile}/{idx}{docType}.txt"

def getResultMapPath(profile: str, docType: str, idx: int, city: str) -> str:
    return f"./data/{profile}/{idx}{docType}_{city}_map.html"

def preprocessBotConvo(text: str) -> str:
    return "\n".join(
        line.replace("Użytkownik:", "") for line in text.split("\n") if "?" not in line)
