from base import Session, engine, Base
from tools import trigger_database ,extract_updated_data
from location import Location
from current_data_fetch import save_current_pd_csv
"""
def test_triggers_database():
    session =Session()
    locations=session.query(Location).all()
    loc_liste=trigger_database(locations)
    return loc_liste


info=test_triggers_database()
extract_updated_data(info)
"""

#save_current_pd_csv()