import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt

hawaii_file = "../data/hawaii.sqlite"
year_format = "%Y-%m-%d"

class Climate_Database():
    """
    This class is used to connect to a Climate Database.
    """
    def __init__(self, filepath = hawaii_file):
        """
        Connects to the SQLite database specified in the filepath.
        """
        engine = create_engine(f"sqlite:///{filepath}")
        Base = automap_base()
        Base.prepare(engine, reflect = True)
        self.measurement_table = Base.classes["measurement"]
        self.station_table = Base.classes["station"]
        self.session = Session(engine)
        self.inspect = inspect(engine)

    def __del__(self):
        """
        On deconstruction, close all connnections.
        """
        self.session.close()
    
    def get_latest_date(self):
        """ 
        This method retrieves the latest date in
        the database in the format YYYY-MM-DD
        """
        measurement_table = self.measurement_table
        session = self.session
        return session.query(
            measurement_table.date
            ).order_by(measurement_table.date.desc()).first()[0]

    def get_all_precip_data(self):
        session = self.session
        measurement_table = self.measurement_table
        return session.query(
            measurement_table.date, 
            measurement_table.prcp
            )

    def get_precip_data(self, start_date, end_date):
        """
        This method gets the precipitation data
        between a start and an end date.
        Dates are in the format YYYY-MM-DD.
        """
        session = self.session
        measurement_table = self.measurement_table
        return session.query(
            measurement_table.date, 
            measurement_table.prcp
            ).filter(
                measurement_table.date >= start_date
                ).filter(
                    measurement_table.date <= end_date)

    def get_num_stations(self):
        """
        This method gets the number of
        weather stations in the database.
        """
        session = self.session
        station_table = self.station_table
        return session.query(station_table).distinct(station_table.station).count()

    def get_most_active_station_query(self):
        """
        This method gets the query to get the stations
        with the number of measurements they have made.
        Results are returned in descending order of the number of measurements.
        """
        session = self.session
        measurement_table = self.measurement_table
        session_table = self.station_table
        return session.query(
                    session_table.name,
                    measurement_table.station, 
                    func.count(measurement_table.station)
                    ).filter(
                        measurement_table.station == session_table.station).\
                    group_by(measurement_table.station).\
                    order_by(func.count(measurement_table.station).desc())

    def get_most_active_stations(self):
        """
        This method gets the stations
        with the number of measurements they have made.
        Results are returned in descending order of the number of measurements.
        """
        return self.get_most_active_station_query().all()
    
    def get_most_active_station(self):
        """
        This method retrieves the station ID
        of the station with the most measurements.
        """
        return self.get_most_active_station_query().first()

    def get_temps(self, station, start_date, end_date):
        """
        This function returns all temperatures taken
        at a station between a start date and an end date.
        Dates are in the format YYYY-MM-DD
        """
        session = self.session
        measurement_table = self.measurement_table
        return session.query(
                    measurement_table.date, 
                    measurement_table.tobs
                    ).filter(
                        measurement_table.station == station
                    ).filter(
                        measurement_table.date >= start_date
                    ).filter(
                        measurement_table.date <= end_date).all()

    def get_temp_stats_by_station(self, station):
        """
        Gets temperature statistics for a station.
        Returns a dictionary with the following keys:\n
        "min" - The minimum temp\n
        "max" - The maximum temp\n
        "avg" - The average temp\n
        """
        session = self.session
        measurement_table = self.measurement_table
        stats = session.query(
            func.min(measurement_table.tobs),
                    func.max(measurement_table.tobs),
                    func.avg(measurement_table.tobs)
            ).filter(measurement_table.station == station).first()
        return {
            "min" : stats[0],
            "max" : stats[1],
            "avg" : stats[2]
        }

    def get_temp_stats_by_date(self, start_date, end_date):
        """
        Gets temperature statistics between a start and an end date.
        Returns a dictionary with the following keys:\n
        "min" - The minimum temp\n
        "max" - The maximum temp\n
        "avg" - The average temp\n
        """
        session = self.session
        measurement_table = self.measurement_table
        stats = session.query(
                    func.min(measurement_table.tobs),
                    func.max(measurement_table.tobs),
                    func.avg(measurement_table.tobs)
                    ).filter(
                        measurement_table.date >= start_date
                    ).filter(
                        measurement_table.date <= end_date).first()
        return {
            "min" : stats[0],
            "max" : stats[1],
            "avg" : stats[2]
        }

    def get_all_stations(self):
        session = self.session
        station_table = self.station_table
        return session.query(station_table).all()
    
    def print_info(self):
        inspector = self.inspect
        tables = inspector.get_table_names()
        for table in tables:
            print(table)
            columns = inspector.get_columns(table)
            column_names = [column["name"] for column in columns]
            print(column_names)


def year_ago(date):
    """
    This returns the date from a year ago.
    Dates are in YYYY-MM-DD.
    """
    date_dt = dt.datetime.strptime(date, year_format)
    year_ago_dt = date_dt.replace(year = date_dt.year - 1)
    return year_ago_dt.strftime(year_format)
