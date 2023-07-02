from collections import namedtuple

Selection = namedtuple("Selection", "WriteFile, SelectedProviders")

availableProviders = {
    "Google": ["https://8.8.8.8/dns-query", "https://8.8.4.4/dns-query"],
    "CloudFlared": ["https://1.1.1.1/dns-query", "https://1.0.0.1/dns-query"],
    "Quad9": ["https://9.9.9.9/dns-query"]
}

FILE_NAME = "cloudflared"
MENU_DELIMITER = " - "
EXIT_SAVE = "Save And Exit"
EXIT_NO_SAVE = "Exit Without Saving"

def ShowMenuAndGetSelection():
    menuDict = BuildMenuDictionary()
    selectedProviders =  set()
    saveExitNum = next(key for key in menuDict if menuDict[key] == EXIT_SAVE)
    choiceNum = 0

    while choiceNum < saveExitNum:
        PrintMenuPrompt(selectedProviders, menuDict)

        choice = input("Choose DNS Provider To Add / Remove Or Exit: ")

        try:
            choiceNum = int(choice)
        except:
            print("Invalid Selection.")
            continue

        if choiceNum >= 0 and choiceNum < saveExitNum:
            selectedProvider = menuDict[choiceNum]
            if selectedProvider in selectedProviders:
                selectedProviders.remove(selectedProvider)
            else:
                selectedProviders.add(selectedProvider)

    return Selection(choiceNum == saveExitNum, selectedProviders)


def WriteConfig(configFileName, selectedProviders):
    fileBuffer = "# Commandline args for cloudflared \n"
    fileBuffer = fileBuffer + "CLOUDFLARED_OPTS=--port 5053"

    for provider in selectedProviders:
        for url in availableProviders[provider]:
            fileBuffer = fileBuffer + " --upstream " + url

    configFile = open(configFileName, "w")
    configFile.write(fileBuffer)
    configFile.close()


def BuildMenuDictionary():
    menuDict = {}
    menuNum = 0

    for provider in availableProviders.keys():
        menuDict[menuNum] = provider
        menuNum = menuNum + 1

    menuDict[menuNum] = EXIT_SAVE
    menuNum = menuNum + 1
    menuDict[menuNum] = EXIT_NO_SAVE

    return menuDict


def PrintMenuPrompt(selectedProviders, menuDict):
    print("==================================================")
    print("Current selected DNS providers:")

    for provider in selectedProviders:
        print(provider)

    print()

    for menuNum, menuOption in menuDict.items():
        print(str(menuNum) + MENU_DELIMITER + menuOption)


if __name__ == '__main__':
    selection = ShowMenuAndGetSelection()

    if selection.WriteFile:
        WriteConfig(FILE_NAME, selection.SelectedProviders)