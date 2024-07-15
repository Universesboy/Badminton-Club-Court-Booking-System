from typing import Dict, List, Optional 
from datetime import datetime, time, timedelta

# A class to manage badminton court bookings.
class BookCourts:
    def __init__(self, total_courts: int):
        # Define total_courts, create dictionary for booked_courts and court_schedule
        self.total_courts = total_courts
        self.booked_courts: Dict[int, Dict[str, str]] = {}
        self.court_schedule: Dict[int, Dict[time, str]] = {
            court: {} for court in range(1, total_courts + 1)
        }

    def is_available(self, court_number: int, booking_time: time) -> bool:
        # Check if a specific court is available at a given time.
        # If the court is not in the range, raises ValueError.
        if court_number not in range(1, self.total_courts + 1):
            raise ValueError(f"Invalid court number. Must be between 1 and {self.total_courts}")
        return booking_time not in self.court_schedule[court_number]

    def book_court(self, court_number: int, user_name: str, booking_time: time, duration: int = 60) -> bool:
        # Book a court for a user at a specific time.
        """
        Args:
            court_number (int): The number of the court to book.
            user_name (str): The name of the user booking the court.
            booking_time (time): The start time of the booking.
            duration (int, optional): The duration of the booking in minutes. Defaults to 60.
        Returns:
            bool: True if the booking was successful, False otherwise.
        """
        if self.is_available(court_number, booking_time):
            end_time = (datetime.combine(datetime.today(), booking_time) + timedelta(minutes=duration)).time()
            self.court_schedule[court_number][booking_time] = user_name
            self.booked_courts.setdefault(court_number, {})[booking_time.strftime("%H:%M")] = user_name
            return True
        else:
            print(f"Sorry, court {court_number} is not available at {booking_time}")
            return False

    def display_booked_courts(self) -> None:
        """
        Display all booked courts and their booking details.
        """
        for court_number, bookings in self.booked_courts.items():
            for time, user_name in bookings.items():
                print(f"Court Number: {court_number}, Time: {time}, Booked By: {user_name}")

    def display_user_bookings(self, user_name: str) -> None:
        # Display all bookings for a user.
        user_courts = [
            (court, time) 
            for court, bookings in self.booked_courts.items() 
            for time, user in bookings.items() 
            if user == user_name
        ]
        if user_courts:
            print(f"{user_name}, you have booked the following courts:")
            for court, time in user_courts:
                print(f"Court {court} at {time}")
        else:
            print(f"User {user_name} has no bookings.")

    def cancel_booking(self, court_number: int, booking_time: time, user_name: str) -> bool:
        # Cancel a booking for a specific user.
        """
        Args:
            court_number (int): The number of the court to cancel the booking for.
            booking_time (time): The time of the booking to cancel.
            user_name (str): The name of the user who made the booking.
        Returns:
            bool: True if the cancellation was successful, False otherwise.
        """
        if (
            court_number in self.booked_courts 
            and booking_time.strftime("%H:%M") in self.booked_courts[court_number]
            and self.booked_courts[court_number][booking_time.strftime("%H:%M")] == user_name
        ):
            del self.booked_courts[court_number][booking_time.strftime("%H:%M")]
            del self.court_schedule[court_number][booking_time]
            return True
        else:
            print(f"No booking found for user {user_name} on court {court_number} at {booking_time}")
            return False

    def get_available_courts(self, booking_time: time) -> List[int]:
        # Get a list of available courts at a specific time.
        """
        Args:
            booking_time (time): The time to check for available courts.
            
        Returns:
            List[int]: A list of court numbers that are available at the specified time.
        """
        return [
            court for court in range(1, self.total_courts + 1)
            if booking_time not in self.court_schedule[court]
        ]
    def calculate_price (self, start_time, end_time):
        # Define your pricing rules here
        peak_hours = (time(17, 0), time(22, 0))
        total_price = 0
        peak_price = 30
        off_peak_price = 20
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        current_dt = start_dt

        while current_dt < end_dt:
            if current_dt <= start_dt < end_dt:
                total_price += peak_price
            else:
                total_price += off_peak_price
            current_dt += timedelta(minutes = 1) # Increment by one minute
        return total_price
    def calculate_total_price (self, bookings):
        total_price = 0
        for booking in bookings:
            total_price += self.calculate_price(booking['start_time'], booking['end_time'])
        return total_price
    
    def is_booking_allowed (self, booking_date):
        max_advanced_days = 7
        today = datetime.now().date()
        max_date = today + timedelta(days = max_advanced_days)
        if booking_date > max_date:
            return False
        return True

#确定预定场地以后输入邮箱地址以便给顾客发送确认或者取消邮件, 还需要研究how to send confirmation email

# Repeat book courts
def handle_recurring_bookings(user_name, court_number, start_time, duration, recurrence_pattern):
    # Define logic to handle daily, weekly, monthly, and yearly recurrence
    if recurrence_pattern == 'daily':
        recurrence_interval = timedelta(days=1)
    elif recurrence_pattern == 'weekly':
        recurrence_interval = timedelta(weeks=1)
    elif recurrence_pattern == 'monthly':
        recurrence_interval = timedelta(weeks=4)
    elif recurrence_pattern == 'yearly':
        recurrence_interval = timedelta(days=365)

    booking_date = datetime.combine(datetime.today(), start_time)
    end_date = booking_date + duration
    while booking_date <= end_date:
        # Save each booking instance
        book_court(user_name, court_number, booking_date.time(), duration)
        booking_date += recurrence_interval

#SYNCED EVENT (This booking will be synced with Google Workspace)
# Sync bookings with Google Workspace using the Google Calendar API.

    
# Usage example
    if __name__ == "__main__":
        booking_system = BookCourts(9)
    
    # Book some courts
    booking_system.book_court(1, "Alice", time(9, 0))
    booking_system.book_court(2, "Bob", time(10, 0))
    booking_system.book_court(1, "Charlie", time(11, 0))
    
    # Display all booked courts
    booking_system.display_booked_courts()
    
    # Display bookings for a specific user
    booking_system.display_user_bookings("Alice")
    
    # Cancel a booking
    booking_system.cancel_booking(1, time(9, 0), "Alice")
    
    # Check available courts at a specific time
    available_courts = booking_system.get_available_courts(time(9, 0))
    print(f"Available courts at 9:00: {available_courts}")
