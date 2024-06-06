from flask import Flask, jsonify, request
from database import get_db_session
from collections import OrderedDict
from sqlalchemy import or_, distinct, create_engine
from sqlalchemy import distinct
from sqlalchemy.orm import aliased, joinedload, scoped_session, sessionmaker
from werkzeug.security import check_password_hash
from flask_cors import CORS  # Import CORS

from models import Base, Reptile, Synonym, Comment, Common_Name, Distribution, Diagnosis, External_Link, Specimen, Etymology, Taxa, Biblio, AdminUser
##from load_data import load_reptile


## Create the flask app 

app = Flask(__name__)
CORS(app)


def unique(items):
    seen = set()
    return [x for x in items if x not in seen and not seen.add(x)]

def serialize_reptile(reptile):
    reptile_data = OrderedDict([
        ("id", reptile.id),
        ("subspecies_1", reptile.subspecies_1),
        ("reproduction", reptile.reproduction),
        ("subspecies_2", reptile.subspecies_2),
        ("subspecies_finder", reptile.subspecies_finder),
        ("subspecies_year", reptile.subspecies_year),
        ("IUCN", reptile.col17),
        ("taxa", reptile.taxa.value if reptile.taxa else None),
        ("synonyms", unique([synonym.value for synonym in reptile.synonyms])),
        ("comments", unique([comment.value for comment in reptile.comments])),
        ("common_names", unique([common_name.value for common_name in reptile.common_names])),
        ("distributions", unique([distribution.value for distribution in reptile.distributions])),
        ("diagnoses", unique([diagnosis.value for diagnosis in reptile.diagnoses])),
        ("external_links", unique([external_link.value for external_link in reptile.external_links])),
        ("etymologies", unique([etymology.value for etymology in reptile.etymologies])),
        ("specimens", unique([specimen.value for specimen in reptile.specimens])),
        ("bibliography", [{
            "bib_id": bib.bib_id,
            "bib_authors": bib.bib_authors,
            "bib_year": bib.bib_year,
            "bib_title": bib.bib_title,
            "bib_journal": bib.bib_journal,
            "bib_url": bib.bib_url
        } for bib in reptile.bibliography])
    ])
    return reptile_data

@app.route('/reptiles/<int:reptile_id>', methods=['GET'])
def get_reptile(reptile_id):
    session = get_db_session()
    reptile = session.query(Reptile).filter(Reptile.id == reptile_id).first()
    if reptile:
        reptile_data = serialize_reptile(reptile)
        session.close()
        return jsonify(reptile_data)
    else:
        session.close()
        return jsonify({"error": "Reptile not found"}), 404

# Add other routes here...

@app.route('/hello',methods=['GET'])
def hello():
    return jsonify("Hello!"), 200


@app.route('/reptiles/search/<string:query>', methods=['GET'])
def search_reptiles(query):
    session = get_db_session()
    synonym_alias = aliased(Synonym)  # Creating an alias for the Synonym table to use in the join

    # Explicitly joining Reptile with Synonym using an outer join to include reptiles that may not have synonyms
    reptiles = session.query(Reptile).outerjoin(
        synonym_alias, Reptile.id == synonym_alias.reptile_id
    ).filter(
        or_(
            Reptile.subspecies_1.ilike(f"%{query}%"),
            Reptile.subspecies_2.ilike(f"%{query}%"),
            synonym_alias.value.ilike(f"%{query}%")
        )
    ).all()  # Using distinct() to avoid duplicate results due to the join

    if reptiles:
        reptiles_data = [serialize_reptile(reptile) for reptile in reptiles]
        session.close()
        return jsonify(reptiles_data)
    else:
        session.close()
        return jsonify({"error": "No reptiles found matching the query"}), 404

    
@app.route('/reptiles/search/subspeciesfinder/<string:query>', methods=['GET'])
def search_reptiles_by_subspecies_finder(query):
    session = get_db_session()
    reptiles = session.query(Reptile).filter(
        Reptile.subspecies_finder.ilike(f"%{query}%")
    ).all()

    if reptiles:
        reptiles_data = [serialize_reptile(reptile) for reptile in reptiles]
        session.close()
        return jsonify(reptiles_data)
    else:
        session.close()
        return jsonify({"error": "No reptiles found matching the query"}), 404
    
@app.route('/reptiles/search/year/<int:year>', methods=['GET'])
def search_reptiles_by_year(year):
    session = get_db_session()
    reptiles = session.query(Reptile).filter(
        Reptile.subspecies_year == year
    ).all()

    if reptiles:
        reptiles_data = [serialize_reptile(reptile) for reptile in reptiles]
        session.close()
        return jsonify(reptiles_data)
    else:
        session.close()
        return jsonify({"error": "No reptiles found matching the year"}), 404
    
@app.route('/reptiles/search/taxa/<string:taxa_query>', methods=['GET'])
def search_reptiles_by_taxa(taxa_query):
    session = get_db_session()
    reptiles = session.query(Reptile).join(Taxa).filter(
        Taxa.value.ilike(f"%{taxa_query}%")
    ).all()

    if reptiles:
        reptiles_data = [serialize_reptile(reptile) for reptile in reptiles]
        session.close()
        return jsonify(reptiles_data)
    else:
        session.close()
        return jsonify({"error": "No reptiles found matching the taxa"}), 404





@app.route('/reptiles/search/advanced', methods=['GET'])
def advanced_search():
    session = get_db_session()
    query = session.query(Reptile)

    # Retrieve query parameters
    taxa = request.args.get('higher-taxa')
    genus = request.args.get('genus')
    species = request.args.get('species')
    subspecies = request.args.get('subspecies')
    author = request.args.get('author')
    year = request.args.get('year')  # Get the year as a string
    if year:
        year = int(year)  # Convert year to an integer
    common_name = request.args.get('common-name')
    distribution = request.args.get('distribution')
    types = request.args.get('types')
    references = request.args.get('references')

    # Dynamically build the query based on the presence of parameters
    if taxa:
        query = query.join(Taxa).filter(Taxa.value.ilike(f"%{taxa}%"))
    if genus:
    # Join with the Synonym table and filter on the synonym value
        query = query.join(Reptile.synonyms).filter(Synonym.value.ilike(f"%{genus}%"))
    if species:
        query = query.filter(or_(
            Reptile.subspecies_1.ilike(f"%{subspecies}%"),
            Reptile.subspecies_2.ilike(f"%{subspecies}%")
            ))
    if subspecies:
         query = query.filter(or_(
            Reptile.subspecies_1.ilike(f"%{subspecies}%"),
            Reptile.subspecies_2.ilike(f"%{subspecies}%")
            ))
    if author:
        query = query.filter(Reptile.subspecies_finder.ilike(f"%{author}%"))
    if year:
        query = query.filter(Reptile.subspecies_year == year)
    if common_name:
        query = query.join(Common_Name).filter(Common_Name.value.ilike(f"%{common_name}%"))
    if distribution:
        query = query.join(Distribution).filter(Distribution.value.ilike(f"%{distribution}%"))
    if types:
        query = query.filter(Reptile.types.ilike(f"%{types}%"))
    if references:
        query = query.filter(Reptile.references.ilike(f"%{references}%"))

    results = query.all()
    if results:
        # Correctly use the serialize_reptile function
        serialized_results = [serialize_reptile(reptile) for reptile in results]
        return jsonify(serialized_results), 200
    else:
        return jsonify({"error": "No results found"}), 404    

#Adding new reptile API call
@app.route('/reptiles/add', methods=['POST'])
def add_reptile_api():
    data = request.json
    session = get_db_session()
    try:
        row_data = [
        data.get('taxa'),
        data.get('subspecies_1'),
        data.get('subspecies_2'),
        data.get('subspecies_finder'),
        str(data.get('subspecies_year')),
         data.get('col05', ''),  # Default to empty string if not provided,  # Assuming this is a string; adjust if it's a list
        ", ".join(data.get('synonyms', [])),
        data.get('col07', ''),  # Assuming this is a string; adjust if it's a list
        ", ".join(data.get('common_names', [])),
        ", ".join(data.get('distributions', [])),
        "\n".join(data.get('comments', [])),  # Using newline for comments
        ", ".join(data.get('diagnoses', [])),
        ", ".join(data.get('specimens', [])),
        "\n".join(data.get('external_links', [])),  # Newline for external links
        ", ".join(data.get('bibliography_ids', [])),  # Adjust if this is not a list or handled differently
        "\n".join(data.get('etymologies', [])),  # Newline for etymologies
        data.get('col16'),  # Assuming this is a string; adjust if it's a list
        data.get('col17'),  # Assuming this is a string; adjust if it's a list
        data.get('reproduction'),  # Assuming this is a string; adjust if it's a list
]
        
        # Load the reptile using the structured row_data
        load_reptile(session, row_data)
        session.commit()
        return jsonify({'success': 'Reptile added successfully'}), 201
    
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Failed to add reptile', 'details': str(e)}), 400
    
    finally:
        session.close()

@app.route('/login', methods=['POST'])
def login():
    # Extract username and password from the request
    username = request.json.get('username')
    password = request.json.get('password')
    session = get_db_session()

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Query your database for the user
    admin_user = session.query(AdminUser).filter_by(username=username).first()

    if admin_user and admin_user.check_password(password):
        # If the check passes, return a success response
        return jsonify({"message": "Login successful"}), 200
    else:
        # If the user doesn't exist or password is wrong
        return jsonify({"error": "Invalid username or password"}), 401

@app.route('/reptiles/update/<int:reptile_id>', methods=['PUT'])
def update_reptile(reptile_id):
    data = request.json
    session = get_db_session()
    try:
        reptile = session.query(Reptile).filter_by(id=reptile_id).one()
        
        # Taxa handling
        taxa_value = data.get('taxa')
        if taxa_value:
            taxa = session.query(Taxa).filter_by(value=taxa_value).one_or_none()
            if not taxa:
                taxa = Taxa(value=taxa_value)
                session.add(taxa)
            reptile.taxa = taxa

        # Simple string fields
        reptile.subspecies_1 = data.get('subspecies_1', reptile.subspecies_1)
        reptile.subspecies_2 = data.get('subspecies_2', reptile.subspecies_2)
        reptile.subspecies_finder = data.get('subspecies_finder', reptile.subspecies_finder)
        reptile.subspecies_year = data.get('subspecies_year', reptile.subspecies_year)
        reptile.reproduction = data.get('reproduction', reptile.reproduction)
        reptile.col16 = data.get('col16', reptile.col16)
        reptile.col17 = data.get('col17', reptile.col17)

        # Binary fields
        col05_data = data.get('col05')
        if col05_data:
            reptile.col05 = col05_data.encode('utf-16')

        col07_data = data.get('col07')
        if col07_data:
            reptile.col07 = col07_data.encode('utf-16')

        # List fields
        def update_model_list(model, attr, data_key):
            current_items = getattr(reptile, attr)
            session.query(model).filter(model.reptile_id == reptile.id).delete()
            new_items = [model(value=item) for item in data.get(data_key, [])]
            setattr(reptile, attr, new_items)

        update_model_list(Synonym, 'synonyms', 'synonyms')
        update_model_list(Common_Name, 'common_names', 'common_names')
        update_model_list(Distribution, 'distributions', 'distributions')
        update_model_list(Comment, 'comments', 'comments')
        update_model_list(Diagnosis, 'diagnoses', 'diagnoses')
        update_model_list(External_Link, 'external_links', 'external_links')
        update_model_list(Specimen, 'specimens', 'specimens')
        update_model_list(Etymology, 'etymologies', 'etymologies')

        # Commit the transaction
        session.commit()
        return jsonify({'success': 'Reptile updated successfully'}), 200
    
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Failed to update reptile', 'details': str(e)}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
    finally:
        session.close()

@app.route('/reptiles/delete/<int:reptile_id>', methods=['DELETE'])
def delete_reptile(reptile_id):
    session = get_db_session()
    try:
        reptile = session.query(Reptile).filter_by(id=reptile_id).one()
        session.delete(reptile)
        session.commit()
        return jsonify({'success': 'Reptile deleted successfully'}), 200
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': 'Failed to delete reptile', 'details': str(e)}), 400
    except NoResultFound:
        return jsonify({'error': 'Reptile not found'}), 404
    finally:
        session.close()


if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")
