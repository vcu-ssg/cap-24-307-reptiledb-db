# Create SQLAlchemy objects
from sqlalchemy import Column, Integer, String, ForeignKey, Table, LargeBinary, UniqueConstraint, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker, Session
from sqlalchemy.orm import declarative_base

Base = declarative_base()

reptile_biblio = Table(
    "reptile_biblio",
    Base.metadata,
    Column("reptile_id", Integer, ForeignKey("reptiles.id"),index=True),
    Column("biblio_id", String(30), ForeignKey("bibliography.bib_id"),index=True),
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
    value = Column(String(4096))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value[:4096]
    def __repr__(self):
        return f"<Synonym(id={self.id}), {self.value}>"

class Column7( Base ):
    __tablename__ = "column7"

    id = Column(Integer, primary_key=True, autoincrement=True,index=True)
    value = Column(String(255))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value[:255]
    def __repr__(self):
        return f"<Synonym(id={self.id}), {self.value}>"


class Comment( Base ):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(8192))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = str(value).replace("\u001d","")[:8000]
#        self.value = self.value.encode("utf-8")
    def __repr__(self):
        return f"<Comment(id={self.id}), {self.value}>"

class Common_Name( Base ):
    __tablename__ = "common_names"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(4096))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value[:4096]
    def __repr__(self):
        return f"<Common_Name(id={self.id}), {self.value}>"

class Distribution( Base ):
    __tablename__ = "distributions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(4096))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value[:4096]
    def __repr__(self):
        return f"<Distribution(id={self.id}), {self.value}>"

class Diagnosis( Base ):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Text(65336))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = str(value)[:65335]
    def __repr__(self):
        return f"<Diagnosis(id={self.id}), {self.value}>"

class External_Link( Base ):
    __tablename__ = "external_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(4096))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value[:4096]
    def __repr__(self):
        return f"<External_Link(id={self.id}), {self.value}>"

class Specimen( Base ):
    __tablename__ = "specimens"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(9000))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = str(value).replace("\u001d","")[:8900]
    def __repr__(self):
        return f"<Specimen(id={self.id}), {self.value}>"

class Etymology( Base ):
    __tablename__ = "etymologies"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    value = Column(String(4096))
    reptile_id = Column( Integer, ForeignKey("reptiles.id") )
    
    def __init__( self, value ):
        self.value = value[:4096]
    def __repr__(self):
        return f"<Etymology(id={self.id}), {self.value}>"


class Taxa( Base ):
    __tablename__ = "taxa"

    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(String(255),index=True,unique=True)

    def __init__( self, cols ):
        self.value = cols[0][:255]
    def __repr__(self):
        return f"<Taxa(id={self.id}), {self.value}>"

    __table_args__ = (
        UniqueConstraint('value', name='uq_taxa_value'),
    )

class Reptile(Base):
    __tablename__ = 'reptiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
#remove    higher_taxa_species = Column(String(4096))
    subspecies_1 = Column(String(255))
    subspecies_2 = Column(String(255))
    subspecies_finder = Column(String(255))
    subspecies_year = Column(Integer)
    col05 = Column(String(255))
#remove    synonym_string = Column(String(4096))
#remove    col07 = Column(Text(65536))
#remove    common_names_string = Column(String(4096))
#remove distribution_string = Column(String(4096))
#remove    comment_string = Column(String(4096))
#remove    diagnosis_string = Column(String(4096))
#remove    types_string = Column(String(4096))
#remove    external_links_string = Column(String(4096))
#remove    bibliography_ids = Column(String(4096))
#remove    etymology_string = Column(String(4096))
    col16 = Column(String(255))
    col17 = Column(String(255))
    reproduction = Column(String(2048))
    bibliography = relationship(
        "Biblio",secondary=reptile_biblio,back_populates="reptiles"
    )
    taxa_id = Column( Integer, ForeignKey("taxa.id") )
    taxa = relationship('Taxa', foreign_keys=[taxa_id], uselist=False)

    synonyms = relationship("Synonym",backref=backref("reptiles"))
    column7s = relationship("Column7",backref=backref("reptiles"))
    comments = relationship("Comment",backref=backref("reptiles"))
    common_names = relationship("Common_Name",backref=backref("reptiles"))
    distributions = relationship("Distribution",backref=backref("reptiles"))
    diagnoses = relationship("Diagnosis",backref=backref("reptiles"))
    external_links = relationship("External_Link",backref=backref("reptiles"))
    etymologies = relationship("Etymology",backref=backref("reptiles"))
    specimens = relationship("Specimen",backref=backref("reptiles"))

    def __init__(self, cols ):
#remove        self.higher_taxa_species = cols[0]
        self.subspecies_1 = str(cols[1])
        self.subspecies_2 = str(cols[2])
        self.subspecies_finder = str(cols[3])
        self.subspecies_year = int(cols[4])
        self.col05 = str(cols[5])
#remove        self.synonym_string = cols[6]
#remove        self.col07 = cols[7].replace("\u001d","")[:65000]
#remove        self.common_names_string = cols[8]
#remove        self.distribution_string = cols[9]
#remove        self.comment_string = cols[10]
#remove        self.diagnosis_string = cols[11]
#remove        self.types_string = cols[12]
#remove        self.external_links_string = cols[13]
#remove        self.bibliography_ids = cols[14]
#remove        self.etymology_string = cols[15]
        self.col16 = str(cols[16])
        self.col17 = str(cols[17])
        self.reproduction = str(cols[18])

    __table_args__ = (
        UniqueConstraint('subspecies_1', 'subspecies_2', name='uq_subspecies_1_subspecies_2'),
    )
    
    def __repr__(self):
        return f"<Reptile(id={self.id}), {self.subspecies_1} {self.subspecies_2}>"


class Biblio( Base ):
    __tablename__ = 'bibliography'

    bib_id = Column(String(30), primary_key=True,index=True )
    bib_authors = Column(String(5000))
    bib_year = Column(String(255))
    bib_title = Column(Text(65536))
    bib_journal = Column(String(512))
    bib_url = Column(String(2048))
    reptiles = relationship("Reptile",secondary=reptile_biblio,back_populates="bibliography")

    def __init__(self, cols ):
        self.bib_id = cols[0]
        self.bib_authors = cols[1][:2048]
        self.bib_year = int(cols[2])
        self.bib_title = cols[3].replace("\u001d","")[:65000]
        self.bib_journal = cols[4][:2048]
        self.bib_url = cols[5][:2048]

    def __repr__(self):
        return f"<Biblio(bib_id={self.bib_id}), {self.bib_authors} {self.bib_year}>"
