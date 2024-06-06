#Create SQLAlchemy objects
from sqlalchemy import Column, Integer, String, ForeignKey, Table, LargeBinary, UniqueConstraint
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.orm import declarative_base
import os
import json
import chardet
import csv
import sys
from loguru import logger
from werkzeug.security import generate_password_hash, check_password_hash

source_database_txt = "reptile_database_2023_09.txt"
source_bibliography_txt = "reptile_database_bibliography_2023_09.txt"

def load_file(filename):
    """ Load file into structure """
    # Increase the maximum field size limit
    max_field_size = sys.maxsize
    decrement=True
    while decrement:
        # Try to set the field size limit
        try:
            csv.field_size_limit(max_field_size)
            decrement = False  # If successful, exit the loop
        except OverflowError:
            max_field_size = int(max_field_size / 10)
            decrement = True  # Continue the loop with a smaller value
    # Open the file in binary mode and read a chunk of data
    with open(filename, 'rb') as file:
        rawdata = file.read()

    # Detect the encoding
    result = chardet.detect(rawdata)
    encoding = result['encoding']

    logger.debug(f"{filename} detected encoding: {encoding}")

    # Initialize an empty list to store the data
    data = []

    # Open the CSV file for reading with UTF-16 encoding
    with open(filename, newline='', encoding=encoding) as csvfile:
        # Create a CSV reader object
        csvreader = csv.reader(csvfile, delimiter='\t')

        # Iterate over each row in the CSV file
        for row in csvreader:
            # Append the row as a list to the 'data' list
            data.append(row)

    return data


Base = declarative_base()

##raw_db = load_file( source_database_txt )
##raw_bib = load_file( source_bibliography_txt )

reptile_biblio = Table(
    "reptile_biblio",
    Base.metadata,
    Column("reptile_id", Integer, ForeignKey("reptiles.id"),index=True),
    Column("biblio_id", Integer, ForeignKey("bibliography.bib_id"),index=True),
)

old_reptile_taxa = Table(
    "reptile_taxa",
    Base.metadata,
    Column("reptile_id", Integer, ForeignKey("reptiles.id")),
    Column("taxa_id", Integer, ForeignKey("taxa.id")),
)

class Synonym( Base ):
    __tablename__ = "synonyms"

    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Synonym(id={self.id}), {self.value}>"

class Comment( Base ):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Comment(id={self.id}), {self.value}>"

class Common_Name( Base ):
    __tablename__ = "common_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Common_Name(id={self.id}), {self.value}>"

class Distribution( Base ):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Distribution(id={self.id}), {self.value}>"

class Diagnosis( Base ):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Diagnosis(id={self.id}), {self.value}>"

class External_Link( Base ):
    __tablename__ = "external_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<External_Link(id={self.id}), {self.value}>"

class Specimen( Base ):
    __tablename__ = "specimens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Specimen(id={self.id}), {self.value}>"

class Etymology( Base ):
    __tablename__ = "etymologies"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value = Column(String)
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value
    def __repr__(self):
        return f"<Etymology(id={self.id}), {self.value}>"


class Taxa(Base):
    __tablename__ = "taxa"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value = Column(String, index=True, unique=True)

    def __init__(self, value):  # Now correctly accepts a `value` argument
        self.value = value

    def __repr__(self):
        return f"<Taxa(id={self.id}), {self.value}>"

    __table_args__ = (
        UniqueConstraint('value', name='uq_taxa_value'),
    )
    
class Reptile(Base):
    __tablename__ = 'reptiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
#remove    higher_taxa_species = Column(String)
    subspecies_1 = Column(String)
    subspecies_2 = Column(String)
    subspecies_finder = Column(String)
    subspecies_year = Column(Integer)
    col05 = Column(LargeBinary)
#remove    synonym_string = Column(String)
    col07 = Column(LargeBinary)
#remove    common_names_string = Column(String)
#remove distribution_string = Column(String)
#remove    comment_string = Column(String)
#remove    diagnosis_string = Column(String)
#remove    types_string = Column(String)
#remove    external_links_string = Column(String)
#remove    bibliography_ids = Column(String)
#remove    etymology_string = Column(String)
    col16 = Column(String)
    col17 = Column(String)
    reproduction = Column(String)
    bibliography = relationship(
        "Biblio",secondary=reptile_biblio,back_populates="reptiles"
    )
    taxa_id = Column( Integer, ForeignKey("taxa.id") )
    taxa = relationship('Taxa', foreign_keys=[taxa_id], uselist=False)

    synonyms = relationship("Synonym",backref=backref("reptiles"))
    comments = relationship("Comment",backref=backref("reptiles"))
    common_names = relationship("Common_Name",backref=backref("reptiles"))
    distributions = relationship("Distribution",backref=backref("reptiles"))
    diagnoses = relationship("Diagnosis",backref=backref("reptiles"))
    external_links = relationship("External_Link",backref=backref("reptiles"))
    etymologies = relationship("Etymology",backref=backref("reptiles"))
    specimens = relationship("Specimen",backref=backref("reptiles"))

    def __init__(self, cols ):
#remove        self.higher_taxa_species = cols[0]
        self.subspecies_1 = cols[1]
        self.subspecies_2 = cols[2]
        self.subspecies_finder = str(cols[3])
        self.subspecies_year = int(cols[4])
        self.col05 = cols[5].encode('utf-16')
#remove        self.synonym_string = cols[6]
        self.col07 = cols[7].encode('utf-16')
#remove        self.common_names_string = cols[8]
#remove        self.distribution_string = cols[9]
#remove        self.comment_string = cols[10]
#remove        self.diagnosis_string = cols[11]
#remove        self.types_string = cols[12]
#remove        self.external_links_string = cols[13]
#remove        self.bibliography_ids = cols[14]
#remove        self.etymology_string = cols[15]
        self.col16 = cols[16]
        self.col17 = cols[17]
        self.reproduction = cols[18]

    __table_args__ = (
        UniqueConstraint('subspecies_1', 'subspecies_2', name='uq_subspecies_1_subspecies_2'),
    )
    
    def __repr__(self):
        return f"<Reptile(id={self.id}), {self.subspecies_1} {self.subspecies_2}>"


class Biblio( Base ):
    __tablename__ = 'bibliography'

    bib_id = Column(String, primary_key=True,index=True )
    bib_authors = Column(String)
    bib_year = Column(String)
    bib_title = Column(String)
    bib_journal = Column(String)
    bib_url = Column(String)
    reptiles = relationship("Reptile",secondary=reptile_biblio,back_populates="bibliography")

    def __init__(self, cols ):
        self.bib_id = cols[0]
        self.bib_authors = cols[1]
        self.bib_year = int(cols[2])
        self.bib_title = cols[3]
        self.bib_url = cols[4]

    def __repr__(self):
        return f"<Biblio(bib_id={self.bib_id}), {self.bib_authors} {self.bib_year}>"
    
class AdminUser(Base):
    __tablename__ = 'admin_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f"<AdminUser(username={self.username})>"
