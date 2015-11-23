from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from puppies import Base, Shelter, Puppy
from datetime import date, timedelta

# Get the engine
engine = create_engine('sqlite:///puppyshelter.db')
# Bind the engine to the base
Base.metadata.bind = engine
# Configure the session factory
DBSession = sessionmaker(bind = engine)

# Queries:
# 1. Query all of the puppies and return the results in ascending alphabetical
# order
#
# 2. Query all of the puppies that are less than 6 months old organized by the
# youngest first
#
# 3. Query all puppies by ascending weight
#
# 4. Query all puppies grouped by the shelter in which they are staying


def main():
    # Get a session
    session = DBSession()
    # First query
    query1 = session.query(Puppy).order_by(Puppy.name)
    for puppy in query1:
        print(puppy.name)
    # Second query
    query2 = session.query(Puppy).\
        filter(Puppy.dateOfBirth > (date.today() - timedelta(days=(30.42*6)))).\
        order_by(desc(Puppy.dateOfBirth))
    for puppy in query2:
        print(puppy.name, puppy.dateOfBirth)
    # Third query
    query3 = session.query(Puppy).order_by(Puppy.weight)
    for puppy in query3:
        print(puppy.name, puppy.weight)
    # Fourth Query
    query4 = session.query(Puppy).order_by(Puppy.shelter_id)
    for puppy in query4:
        print(puppy.shelter_id, puppy.name)


if __name__ == "__main__":
    main()

