import numpy as np
import pandas as pd

file_name = "travel_bookings-v3.xlsx - Bookings_Data (1).csv"
df = pd.read_csv(file_name)

# 1st: Inspect dataset shape, columns, and data types
print("===  INSPECTING SHAPE, COLUMNS & DATA TYPES ===")
print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.dtypes)

#2nd : Identify missing values and duplicate Booking_ID records
print("\n=== MISSING VALUES & DUPLICATE BOOKING_ID ===")
print("Missing values:\n", df.isnull().sum())
print("Duplicate Booking_ID count:", df["Booking_ID"].duplicated().sum())

# 2nd :Clean Booking_Amount commas and convert to float using slide methods
df["Booking_Amount"] = df["Booking_Amount"].str.replace(",", "")
df["Booking_Amount"] = df["Booking_Amount"].astype(float)

# 3rd: Fill missing Trip_Duration_Days and Booking_Amount with median
print("\n=== HANDLE MISSING VALUES ===")
df["Trip_Duration_Days"] = df["Trip_Duration_Days"].fillna(df["Trip_Duration_Days"].median())
df["Booking_Amount"] = df["Booking_Amount"].fillna(df["Booking_Amount"].median())
print("Remaining missing values:\n", df.isnull().sum())

# 4th: Convert Booking_Date to datetime and extract month and weekday
print("\n=== MONTH AND WEEKDAY ===")
df["Booking_Date"] = pd.to_datetime(df["Booking_Date"])
df["Booking_Month"] = df["Booking_Date"].dt.month
df["Booking_Weekday"] = df["Booking_Date"].dt.day_name()
print(df[["Booking_Date", "Booking_Month", "Booking_Weekday"]].head())

# 5th: Total bookings, total travelers, and total booking revenue
print("\n=== TOTALS ===")
print("Total Bookings:", len(df))
print("Total Travelers:", df["Travelers"].sum())
print("Total Booking Revenue:", round(df["Booking_Amount"].sum(), 2))

# 6th: Average booking amount and average trip duration
print("\n=== AVERAGES ===")
print("Average Booking Amount:", round(df["Booking_Amount"].mean(), 2))
print("Average Trip Duration (Days):", round(df["Trip_Duration_Days"].mean(), 2))

#7th : Rank destinations by booking count and total revenue
print("\n=== RANKING DESTINATIONS ===")
dest_rank = df.groupby("Destination").agg(
    Booking_Count=("Booking_ID", "count"),
    Total_Revenue=("Booking_Amount", "sum"),
).sort_values(by="Total_Revenue", ascending=False)
print(dest_rank)

# 8: Compare average trip duration across package types
print("\n=== AVERAGE DURATION BY PACKAGE TYPE ===")
pkg_duration = df.groupby("Package_Type")["Trip_Duration_Days"].mean()
print(pkg_duration)

# 9: Analyze booking preferences across customer age groups
print("\n=== CUSTOMER AGE GROUPS ===")
df["Age_Group"] = np.where(
    df["Customer_Age"] < 80,
    "Under 80",
    np.where(df["Customer_Age"] <= 87, "80-87", "88+"),
)
print(df.groupby("Age_Group")["Booking_ID"].count())
print(df.groupby(["Age_Group", "Package_Type"])["Booking_ID"].count())

# 10: Identify top 5 months by booking volume
print("\n=== TOP 5 MONTHS BY BOOKING VOLUME ===")
top_5_months = (
    df.groupby("Booking_Month")["Booking_ID"]
    .count()
    .sort_values(ascending=False)
    .head(5)
)
print(top_5_months)

# 11: Use a list, a tuple, and a set
print("\n=== LIST, TUPLE, AND SET ===")
popular_destinations = ["Rome", "Barcelona", "New York"]
fixed_packages = ("Economy", "Boutique", "Executive", "VIP", "Expedition")
unique_destinations = set(df["Destination"])
print("Popular destinations (list):", popular_destinations)
print("Fixed packages (tuple):", fixed_packages)
print("Unique destinations (set):", unique_destinations)

# 12: Dictionary for destination counts and function for average booking value
print("\n=== DICTIONARY & AVERAGE FUNCTION ===")
dest_counts = {}
for dest in df["Destination"]:
    dest_counts[dest] = dest_counts.get(dest, 0) + 1
print("Destination booking counts (dict):", dest_counts)
def avg_booking_value_for_destination(selected_dest):
    filtered = df[df["Destination"] == selected_dest]
    return filtered["Booking_Amount"].mean()
print("Average booking value for Rome:", round(avg_booking_value_for_destination("Rome"), 2))

#13: Use NumPy for mean, median, and standard deviation of booking amounts
print("\n=== NUMPY BOOKING AMOUNT STATS ===")
print("NumPy Mean:", round(np.mean(df["Booking_Amount"]), 2))
print("NumPy Median:", round(np.median(df["Booking_Amount"]), 2))
print("NumPy Std Dev:", round(np.std(df["Booking_Amount"]), 2))

# 4: IQR method for unusually expensive bookings and trip-duration bands
print("\n=== IQR OUTLIERS & DURATION BANDS ===")
q1 = np.percentile(df["Booking_Amount"], 25)
q3 = np.percentile(df["Booking_Amount"], 75)
iqr = q3 - q1
upper_limit = q3 + 1.5 * iqr
expensive_bookings = df[df["Booking_Amount"] > upper_limit]
print("Upper IQR limit:", round(upper_limit, 2))
print("Unusually expensive bookings count:", len(expensive_bookings))

df["Duration_Band"] = np.where(
    df["Trip_Duration_Days"] < 25,
    "Short",
    np.where(df["Trip_Duration_Days"] <= 32, "Medium", "Long"),
)
print(df["Duration_Band"].value_counts())

#15: Simple TravelBooking class and five package-planning recommendations
print("\n=== TRAVELBOOKING CLASS & RECOMMENDATIONS ===")

class TravelBooking:
    def __init__(self, booking_id, destination, amount):
        self.booking_id = booking_id
        self.destination = destination
        self.amount = amount

first_booking = TravelBooking(
    df.loc[0, "Booking_ID"],
    df.loc[0, "Destination"],
    df.loc[0, "Booking_Amount"],
)
print(
    "Sample TravelBooking object:",
    first_booking.booking_id,
    first_booking.destination,
    round(first_booking.amount, 2),
)

recommendations =[
    "1. Focus more on popular destinations that bring the most bookings and money.",
    "2. Run offers and keep extra staff ready during the busiest months.",
    "3. Plan trips and trip lengths to match what different age groups like.",
    "4. Offer extra perks on high-value bookings while keeping prices clear.",
    "5. Keep trip days consistent for each package so planning stays easy.",
]
for rec in recommendations:
    print(rec)
    