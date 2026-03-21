while True:
    print("\nReal Estate Lead System")
    print("1. Add Lead")
    print("2. View Leads")
    print("3. Exit")

    choice = input("Choose an option: ").strip()

    if choice == "1":
        name = input("Customer name: ").strip()
        location = input("Preferred location: ").strip()
        budget = input("Budget: ").strip()

        if not name or not location or not budget:
            print("All fields are required. Lead not saved.")
            continue

        lead = f"{name} | {location} | {budget}"

        with open("leads.txt", "a") as file:
            file.write(lead + "\n")

        print("Lead saved successfully.")

    elif choice == "2":
        try:
            with open("leads.txt", "r") as file:
                leads = file.readlines()

            if not leads:
                print("\nNo leads saved yet.")
            else:
                print("\nSaved Leads:\n")
                for i, lead in enumerate(leads, start=1):
                    print(f"{i}. {lead.strip()}")
        except FileNotFoundError:
            print("\nNo leads saved yet.")

    elif choice == "3":
        print("Goodbye.")
        break

    else:
        print("Invalid option. Please choose 1, 2, or 3.")