import os
from datetime import datetime
import csv

CATEGORIES = {
    "food": ["pizza", "burger", "restaurant", "coffee", "groceries", "snack", "sushi", "steak", "salad", "breakfast", "lunch", "dinner", "brunch", "bakery", "cafe", "tea", "sandwich", "noodle", "bbq", "fast food", "ice cream", "deli", "supermarket", "market", "fruit", "vegetable", "meat", "fish", "seafood", "wine", "beer", "liquor", "catering", "takeout", "delivery", "pastry", "chocolate", "candy", "juice", "smoothie", "organic", "vegan", "grocery", "butcher", "cheese", "egg", "milk", "yogurt", "spice", "herb", "soup", "rice", "pasta", "bento", "taco", "burrito", "wrap", "hotdog", "popcorn", "chips", "cookie", "muffin", "pie", "cake", "scone", "jam", "honey", "soda", "cola", "energy drink", "water", "sparkling", "kombucha", "beer", "lager", "ale", "cider"],
    "transport": ["bus", "taxi", "uber", "train", "metro", "fuel", "gasoline", "diesel", "flight", "plane", "tram", "subway", "cab", "ride", "car", "parking", "toll", "highway", "bridge", "ferry", "ticket", "pass", "shuttle", "bike", "bicycle", "scooter", "motorcycle", "moped", "carpool", "van", "minibus", "coach", "limousine", "driver", "rental", "lease", "maintenance", "repair", "oil", "tire", "battery", "insurance", "registration", "license"],
    "travel": ["hotel", "hostel", "airbnb", "motel", "resort", "flight", "plane", "ticket", "visa", "passport", "tour", "excursion", "trip", "holiday", "vacation", "cruise", "luggage", "car rental", "guide", "map", "souvenir", "travel", "insurance", "booking", "reservation", "ferry", "bus", "train", "taxi", "uber", "airport", "transfer", "check-in", "check-out", "boarding", "gate", "terminal", "baggage", "customs", "duty free", "itinerary"],
    "personal care": ["haircut", "salon", "barber", "spa", "massage", "manicure", "pedicure", "beauty", "cosmetic", "skincare", "shaving", "waxing", "facial", "treatment", "makeup", "perfume", "deodorant", "toothpaste", "toothbrush", "soap", "shampoo", "conditioner", "lotion", "cream", "razor", "nail", "dye", "sunscreen", "moisturizer", "cleanser", "serum", "toner", "mask", "scrub", "brush", "comb", "mirror", "tweezer", "cotton", "pad"],
    "household": ["rent", "mortgage", "maintenance", "repair", "cleaning", "maid", "gardener", "plumber", "electrician", "pest control", "security", "alarm", "furniture", "appliance", "decor", "tool", "paint", "hardware", "key", "lock", "moving", "storage", "utility", "bill", "water", "electricity", "gas", "internet", "phone", "tv", "cable", "satellite", "trash", "recycling", "yard", "garden", "pool", "chimney", "roof", "window", "door"],
    "finance": ["bank", "atm", "fee", "interest", "loan", "credit", "debit", "investment", "stock", "bond", "mutual fund", "insurance", "tax", "account", "transfer", "payment", "deposit", "withdrawal", "mortgage", "brokerage", "dividend", "exchange", "currency", "crypto", "bitcoin", "ethereum", "wallet", "saving", "checking", "fund", "portfolio", "advisor", "consultant", "audit", "statement", "balance", "overdraft", "charge", "refund"],
    "kids": ["toy", "game", "school", "tuition", "clothes", "shoes", "book", "stationery", "diaper", "formula", "baby", "childcare", "nursery", "kindergarten", "birthday", "party", "gift", "lesson", "activity", "playground", "uniform", "lunchbox", "backpack", "pencil", "crayon", "drawing", "coloring", "puzzle", "lego", "doll", "car seat", "stroller", "crib", "swing", "slide", "sandbox", "blocks", "train set", "board game"],
    "pets": ["pet", "dog", "cat", "vet", "grooming", "food", "treat", "toy", "accessory", "leash", "collar", "kennel", "boarding", "training", "medicine", "vaccine", "adoption", "litter", "aquarium", "fish", "bird", "hamster", "rabbit", "guinea pig", "parrot", "turtle", "snake", "reptile", "cage", "tank", "bowl", "scratcher", "bed"],
    "charity": ["donation", "charity", "fundraiser", "ngo", "foundation", "relief", "support", "volunteer", "aid", "gift", "contribution", "sponsorship", "pledge", "church", "temple", "mosque", "synagogue", "community", "event", "drive", "campaign", "outreach", "mission", "grant", "endowment", "scholarship", "benefit"],
    "gifts": ["gift", "present", "birthday", "wedding", "anniversary", "christmas", "holiday", "valentine", "surprise", "party", "congratulation", "farewell", "graduation", "baby shower", "housewarming", "thank you", "retirement", "engagement", "promotion", "invitation", "celebration", "event", "prize", "award", "token"],
    "subscriptions": ["netflix","jio hotstar", "spotify", "amazon prime", "hbo", "disney+", "apple music", "youtube premium", "magazine", "newspaper", "membership", "subscription", "cloud", "storage", "dropbox", "onedrive", "google drive", "adobe", "office 365", "zoom", "slack", "discord", "patreon", "twitch", "newsletter", "substack", "audible", "kindle", "prime", "apple tv", "crunchyroll", "paramount+", "hulu", "showtime", "starz", "fitbit", "strava"],
    "education": ["school", "college", "university", "course", "class", "tuition", "fee", "textbook", "book", "stationery", "pen", "pencil", "notebook", "exam", "test", "lab", "project", "assignment", "enrollment", "registration", "library", "study", "research", "degree", "certificate", "seminar", "workshop", "lecture", "online course"],
    "health": ["doctor", "hospital", "clinic", "pharmacy", "medicine", "drug", "prescription", "checkup", "dentist", "optician", "glasses", "contact lens", "surgery", "therapy", "counseling", "insurance", "premium", "copay", "vaccine", "test", "scan", "x-ray", "blood", "lab", "treatment", "appointment", "ambulance", "first aid"],
    "entertainment": ["movie", "cinema", "game", "concert", "netflix", "theater", "show", "event", "festival", "music", "album", "song", "track", "ticket", "museum", "gallery", "exhibition", "fair", "circus", "amusement park", "zoo", "aquarium", "escape room", "bowling", "arcade", "laser tag", "paintball", "sports", "match", "race", "bet"],
    "shopping": ["clothes", "shoes", "amazon", "mall", "store", "boutique", "market", "supermarket", "department", "outlet", "online", "ecommerce", "purchase", "order", "cart", "checkout", "sale", "discount", "coupon", "gift card", "electronics", "gadget", "phone", "laptop", "tablet", "accessory", "jewelry", "watch", "bag", "wallet", "furniture", "appliance", "tool", "hardware", "toy", "book", "magazine", "music", "video", "game"],
    "sports": ["gym", "fitness", "workout", "exercise", "yoga", "pilates", "swimming", "tennis", "football", "soccer", "basketball", "baseball", "golf", "hockey", "cricket", "rugby", "volleyball", "badminton", "table tennis", "ski", "snowboard", "skate", "surf", "run", "marathon", "triathlon", "race", "cycle", "bike", "climb", "hike", "camp", "outdoor", "adventure", "membership", "subscription", "coach", "trainer", "equipment"],
    "technology": ["computer", "laptop", "tablet", "phone", "smartphone", "desktop", "monitor", "keyboard", "mouse", "printer", "scanner", "router", "modem", "cable", "charger", "battery", "usb", "hard drive", "ssd", "memory", "ram", "gpu", "cpu", "motherboard", "case", "speaker", "headphone", "earbud", "microphone", "webcam", "software", "app", "license", "subscription", "update", "repair", "service", "support", "accessory"],
    "other": []
}

def save_list(filename="save.csv"):
    expenses = []
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) == 4:
                    expense = {
                        "date": row[0],
                        "amount": float(row[1]),
                        "category": row[2],
                        "description": row[3]
                    }
                    expenses.append(expense)
    except FileNotFoundError:
        print("❌ File not found. Starting with an empty expense list.")
    return expenses

expenses = save_list("save.csv")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def write_expenses_to_file(expenses, filename="save.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for exp in expenses:
            writer.writerow([exp["date"], exp["amount"], exp["category"], exp["description"]])

def is_valid_date(date_str):
    if len(date_str) != 10:
        return False
    if date_str[2] != "-" or date_str[5] != "-":
        return False
    day, month, year = date_str.split("-")
    if not (day.isdigit() and month.isdigit() and year.isdigit()):
        return False
    if int(month) < 1 or int(month) > 12:
        return False
    if len(year) != 4:
        return False
    return True

def auto_category(description):
    desc = description.lower()
    for category, keywords in CATEGORIES.items():
        if any(kw in desc for kw in keywords):  #loop
            return category
    return "other"  

def add_expense(expenses):
    clear_screen()
    print("📝Add Expenses")
    ask_for_date_D = input("📅Enter Date? [Y/N] .. :")
    if ask_for_date_D.strip().lower() in ["y" , "yes"]:
            date_input = input("📆Date [DD-MM-YYYY]: ")
            if not is_valid_date(date_input):
                print("❌Invalid date format. Please use DD-MM-YYYY.")
                return
    elif ask_for_date_D.strip().lower() in ["n" , "no"]:
        date_input = datetime.now().strftime("%d-%m-%Y")
    else:
        clear_screen()
        print("❗Enter a valid Input") 
        return
    try:
        amount = float(input("💵Amount :₹"))
    except ValueError:
        print("❌ Invalid amount. Please enter a number.")
        return
    description = input("📝Description: ")
    category = auto_category(description)
    print(f"📂Auto categorized as: {category.capitalize()}")
    ask_question = input("🔄Change Category? [Y/N]: ")
    if ask_question.strip().lower() in ["y", "yes"]:
        print("📋Available Categories:")
        for cat in CATEGORIES:
            print("-", cat)
        then = input("➡️ Enter the desired Category: ").lower()
        if then in CATEGORIES:
            category = then
    expenses.append({
        "date": date_input,
        "amount": amount,
        "description": description,
        "category": category
    })
    with open("save.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date_input, amount, category, description])
    write_expenses_to_file(expenses)    
    print("\n✅ Expense added successfully!")

def summary_by_category(expenses = None):
    if expenses is None:
        expenses = save_list("save.csv")
    clear_screen()
    summary={}
    print("\n📊 Expense Summary by Category:")
    summary_date = {}
    print("1️⃣  Summary (List)")
    print("2️⃣ Summary by Month")
    print("3️⃣ Summary by Bar Chart")
    ask_for_summary_options = int(input("Enter An option .. :"))
    if ask_for_summary_options == 1:
        clear_screen()
        print("📅 List")
        for exp in expenses:            
            print(f"📅 {exp['date']} : 💰 ₹{exp['amount']:.2f} - 🗂️ {exp['category'].capitalize()} - 📝 {exp['description']}")
        for date, total in summary_date.items():
            print(f"")
        for exp in expenses:
            summary[exp["category"]] = summary.get(exp["category"] , 0) + float(exp["amount"])
            for then, total in summary.items():
                print()
    elif ask_for_summary_options == 2:
        clear_screen()
        print("📅 Summary by month")
        get_month = int(input("Enter month [1 - 12]:..:"))
        found = False
        for ex in expenses:
            day, month, year = ex["date"].split("-")
            if int(month) == get_month:
                print(f"🗓️ {ex['date']} - 📂 {ex['category'].capitalize()} : 💵 ₹{ex['amount']:.2f}")
                found = True
        if not found:
            print("❌ No expenses found for this month.")
    elif ask_for_summary_options == 3:
        clear_screen()
        print("\n📊 Expense Bar Chart:\n")
        for exp in expenses:
            summary[exp["category"]] = summary.get(exp["category"], 0) + float(exp["amount"])
        for category, total in summary.items():
            bars = "#" * int(total // 100)
            print(f"{category.capitalize():<15}: {bars} ₹{total:.2f}")
    else:
        clear_screen()
        print("❌ Enter a valid input")
        summary_by_category(expenses)

def currency_converter():
    exchange_rates = {
    "USD": 1.0,         # United States
    "EUR": 0.87,        # Eurozone
    "INR": 86.76,        # India
    "GBP": 0.75,        # United Kingdom
    "JPY": 147.76,       # Japan
    "AUD": 1.57,        # Australia
    "CAD": 1.38,        # Canada
    "CHF": 0.82,        # Switzerland
    "CNY": 7.19,        # China
    "SGD": 1.29,        # Singapore
    "NZD": 1.70,        # New Zealand
    "ZAR": 18.06,        # South Africa
    "BRL": 5.55,         # Brazil
    "RUB": 78.5,        # Russia
    "KRW": 1389.17,      # South Korea
    "HKD": 7.85,        # Hong Kong
    "SEK": 9.73,        # Sweden
    "NOK": 10.19,        # Norway
    "DKK": 6.50,        # Denmark
    "MXN": 19.22,        # Mexico
    "THB": 32.98,        # Thailand
    "MYR": 4.30,         # Malaysia
    "IDR": 16514.65,     # Indonesia
    "TRY": 39.73,        # Turkey
    "SAR": 3.75,        # Saudi Arabia
    "AED": 3.67,        # United Arab Emirates
    "PLN": 3.73,         # Poland
    "EGP": 50.64,        # Egypt
    "PKR": 284.59,       # Pakistan
    "BDT": 122.64,       # Bangladesh
    "VND": 26211.98,     # Vietnam
    "ILS": 3.47,         # Israel
    "CZK": 21.66,        # Czech Republic
    "HUF": 351.82,       # Hungary
    "TWD": 29.78,        # Taiwan
    "PHP": 57.57,        # Philippines
    "COP": 4101.30,      # Colombia
    "ARS": 1164.62,      # Argentina
    "CLP": 940,          # Chile
    "KWD": 0.31,        # Kuwait
    "QAR": 3.64,        # Qatar
    "OMR": 0.38,        # Oman
    "BHD": 0.38,        # Bahrain
    "LKR": 301.35,       # Sri Lanka
    "MAD": 9.14,        # Morocco
    "NGN": 1553.67,      # Nigeria
    "GHS": 10.33,        # Ghana
    "KES": 129.25,       # Kenya
    "UAH": 42.04,        # Ukraine
    "RON": 4.4,         # Romania
    "BGN": 1.7,         # Bulgaria
    "HRK": 6.54,         # Croatia
    "ISK": 124.64,       # Iceland
    "DZD": 130.31,       # Algeria
    "JOD": 0.71,        # Jordan
    "LBP": 89866.14,     # Lebanon
    "SDG": 600.50,       # Sudan
    "TND": 2.94,         # Tunisia
    "UZS": 12596.66,     # Uzbekistan
    "AZN": 1.7,         # Azerbaijan
    "BYN": 3.28,         # Belarus
    "KZT": 524.09,       # Kazakhstan
    "MNT": 3580,      # Mongolia
    "BAM": 1.7,         # Bosnia and Herzegovina
    "MKD": 53.65,        # North Macedonia
    "RSD": 102.20,       # Serbia
    "ALL": 85.22,        # Albania
    "AMD": 385.34,       # Armenia
    "GEL": 2.72,         # Georgia
    "MDL": 17.18,        # Moldova
    "MOP": 8.11,         # Macau
    "MUR": 45.74,        # Mauritius
    "NPR": 138.92,       # Nepal
    "PEN": 3.6,         # Peru
    "SRD": 38.85,        # Suriname
    "SYP": 13002.6,     # Syria
    "TTD": 6.81,         # Trinidad and Tobago
    "UYU": 41.01,        # Uruguay
    "VEF": 10355092.58,        # Venezuela
    "XAF": 570.89,       # Central African CFA
    "XOF": 570.89,       # West African CFA
    "YER": 242.70,       # Yemen
    "ZMW": 23.19         # Zambia
}
    country_dict = {
    "USD": "United States",
    "EUR": "Eurozone",
    "INR": "India",
    "GBP": "United Kingdom",
    "JPY": "Japan",
    "AUD": "Australia",
    "CAD": "Canada",
    "CHF": "Switzerland",
    "CNY": "China",
    "SGD": "Singapore",
    "NZD": "New Zealand",
    "ZAR": "South Africa",
    "BRL": "Brazil",
    "RUB": "Russia",
    "KRW": "South Korea",
    "HKD": "Hong Kong",
    "SEK": "Sweden",
    "NOK": "Norway",
    "DKK": "Denmark",
    "MXN": "Mexico",
    "THB": "Thailand",
    "MYR": "Malaysia",
    "IDR": "Indonesia",
    "TRY": "Turkey",
    "SAR": "Saudi Arabia",
    "AED": "United Arab Emirates",
    "PLN": "Poland",
    "EGP": "Egypt",
    "PKR": "Pakistan",
    "BDT": "Bangladesh",
    "VND": "Vietnam",
    "ILS": "Israel",
    "CZK": "Czech Republic",
    "HUF": "Hungary",
    "TWD": "Taiwan",
    "PHP": "Philippines",
    "COP": "Colombia",
    "ARS": "Argentina",
    "CLP": "Chile",
    "KWD": "Kuwait",
    "QAR": "Qatar",
    "OMR": "Oman",
    "BHD": "Bahrain",
    "LKR": "Sri Lanka",
    "MAD": "Morocco",
    "NGN": "Nigeria",
    "GHS": "Ghana",
    "KES": "Kenya",
    "UAH": "Ukraine",
    "RON": "Romania",
    "BGN": "Bulgaria",
    "HRK": "Croatia",
    "ISK": "Iceland",
    "DZD": "Algeria",
    "JOD": "Jordan",
    "LBP": "Lebanon",
    "SDG": "Sudan",
    "TND": "Tunisia",
    "UZS": "Uzbekistan",
    "AZN": "Azerbaijan",
    "BYN": "Belarus",
    "KZT": "Kazakhstan",
    "MNT": "Mongolia",
    "BAM": "Bosnia and Herzegovina",
    "MKD": "North Macedonia",
    "RSD": "Serbia",
    "ALL": "Albania",
    "AMD": "Armenia",
    "GEL": "Georgia",
    "MDL": "Moldova",
    "MOP": "Macau",
    "MUR": "Mauritius",
    "NPR": "Nepal",
    "PEN": "Peru",
    "SRD": "Suriname",
    "SYP": "Syria",
    "TTD": "Trinidad and Tobago",
    "UYU": "Uruguay",
    "VEF": "Venezuela",
    "XAF": "Central African CFA",
    "XOF": "West African CFA",
    "YER": "Yemen",
    "ZMW": "Zambia"
}
    print("\n💱 Currency Converter")
    print("Country Code  | Country")
    print("-" * 35)
    for code , country in country_dict.items():
        print(f"{code:<13} | {country}")
    from_currency = str(input("🌍 Enter conversion FROM currency(Country Code)...: ")).upper()
    to_currency = str(input("🌐 Enter conversion TO currency(Country Code)...: ")).upper()
    amount = float(input("💰 Enter the amount: "))

    if from_currency in exchange_rates and to_currency in exchange_rates:
        usd_amount = amount / exchange_rates[from_currency]
        converted = usd_amount * exchange_rates[to_currency]
        print(f"✅ {amount} {from_currency} = {converted:.2f} {to_currency}")
    else:
        print("❌ Conversion is not available. Please check currency codes.")
    ask_for_quit = input("Type ❌ quit to close or 🔁 press Enter to convert again... : ")
    if ask_for_quit.strip().lower() in ["quit"]:
        main_menu()
    else:
        currency_converter()

def search_expenses():
    clear_screen()
    print("🔍 Search using Category or Description keyword")
    keyword = input("📂 Enter the keyword to search: ").strip().lower()

    try:
        with open('save.csv', mode='r', newline='') as file:
            reader = csv.DictReader(
                file,
                fieldnames=["date", "amount", "category", "description"]
            )
            found = False
            print("\n🔎 Matching Expenses... ")
            print("-" * 40)

            for row in reader:
                if (keyword in row["description"].lower()
                    or keyword in row["category"].lower()):
                    found = True
                    print(f"📅 {row['date']} | 💰 ₹{row['amount']} | 🗂️ {row['category'].capitalize()} | 📝 {row['description']}")

            if not found:
                print("❌ No matching expenses found.")
    except FileNotFoundError:
        print("❌ save.csv not found.")
    
    choice = input("Type ❌ quit to close or 🔁 press Enter to search again... : ")
    if choice.strip().lower() not in ["quit", "exit"]:
        search_expenses()
    else:
        main_menu()

spending_limits = {}
    
def option():
    try:
        clear_screen()
        print("☰ Options")
        print("1️⃣ 🔒 Add or update a spending limit by category")
        print("2️⃣ 📊 View current spending and limits by category")
        print("3️⃣ 🏠 Main Menu")
        option_input = int(input("Enter an option...: "))
        if option_input == 1:
            cate = input("Enter category name...: ").strip().lower()
            if not cate:
                print("❌ Category can't be empty")
                return
            try:
                limit = float(input(f"Enter a limit for {cate.capitalize()}: ₹"))
                if limit < 0:
                    print("❌ Limit can't be negative")
                    return
                spending_limits[cate] = limit
                print(f"✅ Spending limit for '{cate.capitalize()}' set to ₹{limit}")
            except ValueError:
                print("❌ Please enter a valid numeric limit.")
        elif option_input == 2:
            expenses = save_list("save.csv")
            category_totals = {}
            for exp in expenses:
                cat = exp["category"].lower()
                category_totals[cat] = category_totals.get(cat, 0) + float(exp["amount"])
            print("\n📊 Current Spending and Limits:")
            print(f"{'Category':<15} {'Spent':>10} {'Limit':>10} {'Status':>10}")
            print("-" * 50)
            for cat, spent in category_totals.items():
                limit = spending_limits.get(cat, None)
                status = ""
                if limit is not None:
                    if spent > limit:
                        status = "❌ Over"
                    else:
                        status = "✅ OK"
                else:
                    status = "—"
                print(f"{cat.capitalize():<15} ₹{spent:>9.2f} ₹{limit if limit is not None else '—':>9} {status:>10}")
        elif option_input == 3:
            main_menu()
            return
        else:
            print("❌ Enter a valid option")
        ask_user_input = str(input("Type ❌ quit to close or 🔁 press Enter to continue... : "))
        if ask_user_input.strip().lower() not in ["quit", "exit"]:
            option()
        else:
            main_menu()
    except ValueError:
        print("❌ Enter a valid input")
        
def main_menu():
    clear_screen()
    while True:
        print("\n💰 Expense Tracker")
        print("1️⃣ Add new Expense")
        print("2️⃣ View Summary")
        print("3️⃣ Currency converter")
        print("4️⃣ Search Expenses")
        print("5️⃣ Options")
        print("6️⃣ Exit")      
        try:
            choice = int(input("Select an option .. : "))
            if choice == 1:
                add_expense(expenses)
            elif choice == 2:
                summary_by_category(expenses)
                input("\n🔁Press enter to go to main menu")
                clear_screen()
            elif choice == 6:
                print("👋 Exiting. Have a great day!")
                break
            elif choice == 3:
                currency_converter()
                break
            elif choice == 4:
                search_expenses()
                break
            elif choice == 5:
                option()
                break
            else:
                clear_screen()
                print("❌ Not a valid input")
        except ValueError:   
            print("❌ Invalid input. Please enter a number" )
            break    

main_menu()
        
