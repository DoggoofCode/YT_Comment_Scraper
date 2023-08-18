import os
from colorama import init, Fore, Style
from termcolor import colored
import googleapiclient.discovery
init()


os.system('cls')

settingsOrder = ['casesense', 'autocreategraph']
settingsState = ['true', 'false']
correctLetters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                  'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '_', '/']


# Error for incorrect state - 1

def clean(word):
    cleanedWord = ''
    for letter in word:
        for x in correctLetters:
            if x == letter:
                cleanedWord = cleanedWord + letter
                break
    return cleanedWord


# def printc(text, Colour='white', ender='\n'):
#     print(colored(text, Colour), end=ender)

def printc(text, Colour='WHITE', ender=' '):
    if Colour == 'white':
        print((Fore.WHITE + str(text)), end=" ")
        print(Style.RESET_ALL)
    if Colour == 'blue':
        print((Fore.BLUE + str(text)), end=" ")
        print(Style.RESET_ALL)
    if Colour == 'red':
        print((Fore.RED + str(text)), end=" ")
        print(Style.RESET_ALL)
    if Colour == 'green':
        print((Fore.GREEN + str(text)), end=" ")
        print(Style.RESET_ALL)
def search(spltcmnt, spltcmntTrue):
    if settingsState[0] == 'false':
        searchedWord = (input(' \n Any Search Words: ')).lower()
    elif settingsState[0] == 'true':
        searchedWord = (input(' \n Any Search Words: '))
    else:
        printc('Error - Unclear state for CaseSense', 'red')
        return 1

    ResultsForSearch = []
    # Percentage Creator
    occuranceManager = 0
    for cmt in range(len(spltcmnt)):
        # print(spltcmnt)
        for w in spltcmnt[cmt]:
            if w == searchedWord:
                occuranceManager = occuranceManager + 1

    # Highlighter
    for cmt in range(len(spltcmnt)):
        for w in spltcmnt[cmt]:
            if w == searchedWord:
                ResultsForSearch.append(cmt + 1)
                break

    OccuranceNumber = []

    for commentId in range(len(ResultsForSearch)):
        printc(ResultsForSearch[commentId], 'blue', ender='\n')
        OccuranceNumber.append(ResultsForSearch[commentId])
        for word in range(len(spltcmnt[ResultsForSearch[commentId] - 1])):
            if spltcmnt[ResultsForSearch[commentId] - 1][word] == searchedWord:
                printc(spltcmntTrue[ResultsForSearch[commentId] - 1][word], 'green', ender=' ')
            else:
                printc(spltcmntTrue[ResultsForSearch[commentId] - 1][word], 'white', ender=' ')
        print(' ')

    printc("The word {} occurred {} and this means that it was included in {} percentage of the comments".format(
        searchedWord, occuranceManager, 98 / 100 * occuranceManager), 'red')

    if settingsState[1] == 'false':
        printc('Would you like to create a graph with this data (1) or exit the to pick screen (2):', 'blue', ' ')
        graph = input(' ')
    elif settingsState[1] == 'true':
        graph = '1'
    else:
        printc('Error - Unclear state for AutoCreateGraph', 'red')
        return 1

    if graph == '1':
        printc(OccuranceNumber, 'blue')

    return None


def ReadCommand(command):
    switch = 1

    order = ''
    state = ''

    for letters in command:
        if letters == '/':
            switch = 2
        if not letters == '/':
            if switch == 1:
                order = order + str(letters)
            else:
                state = state + str(letters)

    return order, state


def CommandLine():
    print('')
    command = input('ytCommentSETTINGS >> ').lower()
    spltCommand = command.split()

    for items in spltCommand:
        order, state = ReadCommand(items)

        if order == '--quit':
            return '--QUIT', 'Quiting CommandLime...'

        if not order == 'read':
            # Find the Order
            orderIdx = None

            for orderNames in range(len(settingsOrder)):
                if settingsOrder[orderNames] == order:
                    orderIdx = orderNames

            if orderIdx == None:
                return 'Error', "Error - '{}' item not found.".format(items)

            settingsState[orderIdx] = state

        if order == 'read':
            if not state == '*':
                orderIdx = None

                for orderNames in range(len(settingsOrder)):
                    if settingsOrder[orderNames] == state:
                        orderIdx = orderNames

                if orderIdx == None:
                    return 'Error', "Error - '{}' item not found and therefore cannot be read.".format(items)

                printc(settingsState[orderIdx], 'blue')

            elif state == '*':
                orderIdx = '*'
                for states in range(len(settingsState)):
                    printc(settingsOrder[states], 'yellow', '')
                    printc(' - ', 'white', '')
                    printc(settingsState[states], 'blue')

    return 'Complete', "All items have been complete"


def main():
    global dismiss
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = "ENTER DEVELPOR KEY"

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=DEVELOPER_KEY)

    vid_id = input('What is the Video ID: ')
    if vid_id == '--EXE':
        vid_id = 'dAjk7Xs4IEQ'
    os.system('cls')

    request = youtube.commentThreads().list(
        part="id,snippet",
        maxResults=100,
        order="relevance",
        videoId=vid_id
    )
    response = request.execute()

    data = response
    # for items in data['items']:
    #     print(items['snippet'])
    spltcmnt = []
    spltcmntTrue = []

    for i in range(1, 99):
        cmnt = str(data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
        cmntTrue = cmnt
        if settingsState[0] == 'false':
            cmnt = cmnt.lower()

        word = str(i) + '\n' + str(data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
        print(word)
        spltcmnt.append(cmnt.split())
        spltcmntTrue.append(cmntTrue.split())

    dismiss = '2'

    while not dismiss == '1':
        printc('\n Would you like to finish the program(1) or do another search (2) or open Command Line (3):', 'green',
               ender=' ')
        dismiss = input('')
        if dismiss == '2':
            spltcmnt = []
            spltcmntTrue = []

            for i in range(1, 99):
                cmnt = str(data['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal'])
                cmntTrue = cmnt
                if settingsState[0] == 'false':
                    cmnt = cmnt.lower()
                spltcmnt.append(cmnt.split())
                spltcmntTrue.append(cmntTrue.split())

            error = search(spltcmnt, spltcmntTrue)
            # if not error == None:
            #     printc('Exit With Error Code {}').format(error)

        if dismiss == '3':
            type = ''
            while not type == '--QUIT':
                type, msg = CommandLine()
                if type == 'Error':
                    printc(msg, 'red')
                elif type == 'Complete':
                    printc(msg, 'green')
                elif type == '--QUIT':
                    printc(msg, 'red')
                    print('')


if __name__ == "__main__":
    main()
    # Second Commit