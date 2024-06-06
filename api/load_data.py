import csv
import chardet
import sys
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

# Import your SQLAlchemy session factory and model classes
from database import Session,session
from models import Reptile, Synonym, Comment, Common_Name, Distribution, Diagnosis, External_Link, Specimen, Etymology, Taxa, Biblio, load_file, AdminUser

source_database_txt = "reptile_database_2023_09.txt"
source_bibliography_txt = "reptile_database_bibliography_2023_09.txt"

#raw_db = load_file( source_database_txt )
#raw_bib = load_file( source_bibliography_txt)
                     
def load_reptile( session, row ):
    """ load a reptile into table """

    reptile = Reptile( row )
    session.add(reptile)
 #   session.commit()

    # Clean up and split the bibliographies
    bibs = row[14].replace("\x1d", "").split("\x0b")
    # Loop over array.
    for bib in bibs:
        # check if ID is found in biblio DB
        found_bib = (
            session.query(Biblio)
            .filter(Biblio.bib_id == bib)
            ).one_or_none()
        # If not found, we just found a bug in the original DB
        if found_bib is None:
            pass
##            logger.debug(f"Bib ID :{bib}: not found in biblio table" )

        # If found, make the connections between the records.
        # This represents the SQLAlchemy magic.
        else:
            reptile.bibliography.append(found_bib)
            found_bib.reptiles.append(reptile)
#            session.commit()

    # Working with higher-taxa
    higher_taxa = row[0]
#    logger.debug(f"Searching for {higher_taxa}")
    found_taxa = (session.query(Taxa).filter(Taxa.value==higher_taxa)).one_or_none()
    # If not found, add a new record to taxa table
    if found_taxa is None:
       # logger.debug(f"Adding new taxa: {higher_taxa}")
        found_taxa = Taxa(value=row[0])
        session.add(found_taxa)
#        session.commit()
    # connect reptile and taxa
    reptile.taxa = found_taxa
#    found_taxa.reptiles.append( reptile )

    # Working with synonyms
    synonyms = row[6].replace("\u001d","").split("\u000b")
    if synonyms is not None:
        for syn in synonyms:
            new_syn = Synonym( syn )
            session.add(new_syn)
#            session.commit()
            reptile.synonyms.append( new_syn )

    # Working with common names
    names = row[8].replace("\u001d","").split("\u000b")
    if names is not None:
        for name in names:
            if len(name)>0:
                new_name = Common_Name( name )
                session.add(new_name)
#                session.commit()
                reptile.common_names.append( new_name )

    # Working with distributions
    distributions = row[9].replace("\u001d","").split("\u000b")
    if distributions is not None:
        for dist in distributions:
            if len(dist)>0:
                new_dist = Distribution( dist )
                session.add(new_dist)
                reptile.distributions.append( new_dist )

    # Working with comments
    comments = row[10].replace("\u001d","").split("\u000b")
    if comments is not None:
        for comm in comments:
            if len(comm)>0:
                new_comm = Comment( comm )
                session.add(new_comm)
#                session.commit()
                reptile.comments.append( new_comm )

    # Working with diagnoses
    diagnoses = row[11].replace("\u001d","").split("\u000b")
    if diagnoses is not None:
        for diag in diagnoses:
            if len(diag)>0:
                new_diag = Diagnosis( diag )
                session.add(new_diag)
                reptile.diagnoses.append( new_diag )

    # Working with external_links
    urls = row[13].replace("\u001d","").split("\u000b")
    if urls is not None:
        for url in urls:
            if len(url)>0:
                new_url = External_Link( url )
                session.add(new_url)
                reptile.external_links.append( new_url )

    # Working with etymologies
    etymologies = row[15].replace("\u001d","").split("\u000b")
    if etymologies is not None:
        for ety in etymologies:
            if len(ety)>0:
                new_ety = Etymology( ety )
                session.add(new_ety)
                reptile.etymologies.append( new_ety )

    # Working with specimens
    specimens = row[12].replace("\u001d","").split("\u000b")
    if specimens is not None:
        for spec in specimens:
            if len(spec)>0:
                new_spec = Specimen( spec )
                session.add(new_spec)
                reptile.specimens.append( new_spec )
    

#    session.commit()

# Clear out the old table before loading.  This minimizes primary key errors

session.query(Reptile).delete()

logger.debug(f"rows to process: {len(raw_db)}")

for i,row in enumerate(raw_db):
    try:
        load_reptile( session, row )
    except ValueError as e:
        logger.warning(f"reptile record {i}: {e}")

    if i % 100 == 0:
        logger.debug(f"{i:5}")

    if (True and not i<300):
       # logger.warning(f"TESTING: subset of records loaded.  See line referenced by this warning.")
       break
        
# Admin setup
new_admin_username = 'Peter'
new_admin_password = 'Password1'

# Check if the admin user already exists to avoid duplicates
existing_admin_user = session.query(AdminUser).filter_by(username=new_admin_username).first()
if not existing_admin_user:
    new_admin_user = AdminUser(username=new_admin_username, password=new_admin_password)
    session.add(new_admin_user)
    #session.commit()
    logger.info("New admin user created.")
else:
    logger.info("Admin user already exists.")

session.commit()
