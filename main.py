from models.auth import AuthManager
from models.solve import Solve
from models.storage import SolveStorage
from models.timer import Timer
from datetime import datetime

def auth_menu(auth):
    print("1. Login")
    print("2. Sign up")
    choice = input("Choose an option: ")
    if choice == "1":
        username = input("Username: ")
        password = input("Password: ")
        ok, msg = auth.login(username, password)
        print(msg)
        if ok:
            return username
    elif choice == "2":
        username = input("Username: ")
        password = input("Password: ")
        ok, msg = auth.sign_up(username, password)
        print(msg)
        if ok:
            return username
    else:
        print("Invalid option.")
    return None


def main_menu():
    print("\n📋 Menu:")
    print("1. New solve")
    print("2. Show all solves")
    print("3. Best solve")
    print("4. Average of 5")
    print("5. Average of 12")
    print("6. Delete solve")
    print("0. Exit")


def get_best(solves, user):
    user_solves = [s for s in solves if s.user == user]
    if user_solves:
        return min(user_solves, key=lambda s: s.time_taken)
    return None


def average(solves, user, count):
    user_solves = [s for s in solves if s.user == user][-count:]
    if len(user_solves) < count:
        print(f"Not enough solves to calculate average of {count}.")
        return
    avg = sum([s.time_taken for s in user_solves]) / count
    print(f"Average of {count}: {avg:.2f} seconds")


def show_solves(solves, user):
    user_solves = [s for s in solves if s.user == user]
    if not user_solves:
        print("No solves found.")
    else:
        for i, s in enumerate(user_solves, 1):
            print(f"{i}. {s.time_taken}s - {s.date} - {s.cube_type} - {s.comment}")


def delete_solve(storage, user):
    user_solves = [s for s in storage.solves if s.user == user]
    show_solves(storage.solves, user)
    if not user_solves:
        return
    try:
        index = int(input("Enter solve number to delete: ")) - 1
        if 0 <= index < len(user_solves):
            solve_to_delete = user_solves[index]
            storage.solves.remove(solve_to_delete)
            storage.save()
            print("Solve deleted.")
        else:
            print("Invalid number.")
    except ValueError:
        print("Invalid input.")


def main():
    auth = AuthManager()
    username = None

    while not username:
        username = auth_menu(auth)

    print(f"\n👋 Welcome, {username}!")
    storage = SolveStorage()

    while True:
        main_menu()
        choice = input("Choose an option: ")

        if choice == "1":
            timer = Timer()
            result = timer.start_timer()
            if result:
                comment = input("Comment (optional): ")
                solve = Solve(
                    time_taken=result,
                    date=datetime.now().strftime("%Y-%m-%d %H:%M"),
                    user=username,
                    comment=comment
                )
                storage.add_solve(solve)

        elif choice == "2":
            show_solves(storage.solves, username)

        elif choice == "3":
            best = get_best(storage.solves, username)
            if best:
                print(f"🏆 Best solve: {best.time_taken}s - {best.date}")
            else:
                print("No solves yet.")

        elif choice == "4":
            average(storage.solves, username, 5)

        elif choice == "5":
            average(storage.solves, username, 12)

        elif choice == "6":
            delete_solve(storage, username)

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()