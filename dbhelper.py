import streamlit as st
import mysql.connector


class DB:
    def __init__(self):
        try:
            config = st.secrets["mysql"]

            self.conn = mysql.connector.connect(
                host=config["host"],
                user=config["username"],
                password=config["password"],
                database=config["database"],
                port=config["port"]
            )
            self.cursor = self.conn.cursor()
            print("✅ MySQL DB connected")
            
        except Exception as e:
            print("❌ Connection failed:", e)

    def fetch_station_names(self):
        station = []

        self.cursor.execute("""
            SELECT DISTINCT(source) FROM train_tickets
            UNION
            SELECT DISTINCT(destination) FROM train_tickets
        """)

        data = self.cursor.fetchall()

        for row in data:
            station.append(row[0])

        return station

    def search_tickets(self, source, destination):
        query = """
            SELECT train_id, train_name, class, days_of_operation 
            FROM train_tickets
            WHERE source = '{}' AND destination = '{}'
        """.format(source, destination)

        self.cursor.execute(query)
        data = self.cursor.fetchall()

        column_names = [desc[0] for desc in self.cursor.description]
        result = [dict(zip(column_names, row)) for row in data]

        return result


    def class_frequency(self):
        labels = []
        values = []

        self.cursor.execute("""
            SELECT class, COUNT(*) FROM train_tickets
            GROUP BY class
        """)

        data = self.cursor.fetchall()

        for row in data:
            labels.append(row[0])
            values.append(row[1])

        return labels, values

    def station_wise_booking(self):
        stations = []
        bookings = []

        self.cursor.execute("""
            SELECT source, COUNT(*) AS Bookings
            FROM train_tickets
            GROUP BY source
            ORDER BY Bookings DESC
        """)

        data = self.cursor.fetchall()

        for row in data:
            stations.append(row[0])
            bookings.append(row[1])

        return stations, bookings

    def daily_bookings(self):
        dates = []
        counts = []

        self.cursor.execute("""
            SELECT travel_date, COUNT(*) AS Bookings 
            FROM train_tickets
            GROUP BY travel_date
            ORDER BY travel_date
        """)

        data = self.cursor.fetchall()

        for row in data:
            dates.append(str(row[0]))
            counts.append(row[1])

        return dates, counts

    def revenue_over_time(self):
        rev_dates = []
        rev_values = []

        self.cursor.execute("""
            SELECT travel_date, SUM(price) as total_revenue 
            FROM train_tickets
            GROUP BY travel_date
            ORDER BY travel_date
        """)

        data = self.cursor.fetchall()

        for row in data:
            rev_dates.append(str(row[0]))
            rev_values.append(row[1])

        return rev_dates, rev_values



## try:
#            self.conn = mysql.connector.connect(
#                host="",
#                user="root",
#                password="",
#                database="sql_dashboard",
#                port=3307
#            )
#            self.cursor = self.conn.cursor()
#            print("✅ MySQL DB connected")
#        except Exception as e:
#            print("❌ Connection failed:", e)
#
#    def fetch_station_names(self):
#        station = []