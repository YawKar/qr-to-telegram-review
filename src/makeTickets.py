import databaseWorker.databaseWorker as Dbw
import qrGenerator.qrGenerator as QRGen
import random
import time


def makeTicket() -> str:
    ticketNumber = '%015x' % random.randrange(16**15)
    while (Dbw.isReviewIdExists(ticketNumber)):
        ticketNumber = '%015x' % random.randrange(16**15)
    Dbw.addReviewId(ticketNumber)
    QRGen.makeQRCodeAndSave(ticketNumber)
    return ticketNumber


def main():
    Dbw.check()
    print("-" * 40)
    print("    Создание билетов    ".center(40, '|'))
    print("-" * 40)
    numberOfTickets = 0
    while (True):
        inputNumberOfTickets = input("Введите количество билетов: ")
        if inputNumberOfTickets.isnumeric() == False:
            print("Нужно ввести число от 1 до 200, например: 10, 15, 70")
        inputNumberOfTickets = int(inputNumberOfTickets)
        if inputNumberOfTickets > 200:
            print("Нужно ввести число от 1 до 200, например: 10, 15, 70")
        numberOfTickets = inputNumberOfTickets
        break
    print(f"Приступаю к созданию {numberOfTickets} билетов.")
    ticketsIds = list()
    random.seed(time.time())
    for indexOfTicket in range(numberOfTickets):
        ticketsIds.append(makeTicket())
    print("QR-коды сохранены в папке outputQRCodes")
    print("Вывожу билеты в формате 'порядок. <номер билета>'")
    for ticket in enumerate(ticketsIds, 1):
        print(str(ticket[0]) + ".", ticket[1])


if __name__ == "__main__":
    main()
