############ BAT Functions ############
from flask import redirect, url_for, flash
from sqlalchemy import or_

from .models import db, Dossier
from .dummy import dummyData



# Refractor function that handles the terminal command arguments and initializes relevant funcitons
def Refractor(command, variable):
    output = []

    # Initiator of test command
    if command.lower() in ['t', 'test']:
        for word in ['test command', 'was run', 'with the variable:', variable]:
            output.append(word)

    # Initiator of search function
    elif command.lower() in ['s', 'search']:
        keyword = ':'
        searchTerm, keyword, numberInstances = variable.partition(keyword)
        output = Search(searchTerm, numberInstances)

    # Initiator of Dossier model populator
    elif command.lower() in ['fm', 'fillmodel']:
        output.append(FillModel())

    # Initiator of link function
    elif command.lower() in ['l', 'link']:
        linkKeyword = ','
        strengthKeyword = ':'
        words, strengthKeyword, linkStrength = variable.partition(strengthKeyword)
        wordArray = words.split(linkKeyword)

        output = Link(wordArray, linkStrength)


    # Return value if the command is incorrect or lacking necessary variable(s)
    else:
        flash('Refractor error interpreting command, try writing it again.')
        output = []

    # Returns the output of the Refractor function
    return output



def FillModel():
    # Checks if Dossier model already is populated with dummy data
    for element in dummyData:
        populatedQuery = Dossier.query.filter(Dossier.title.contains(element["title"])).first()

        # If the model does not contain a dossier with element's dummyData the function adds it
        if populatedQuery is None:
            dossier = Dossier(
                title=element["title"],
                protocol=element["protocol"],
                poi=element["poi"],
                attachment=element["attachment"],
            )
            db.session.add(dossier)
        
        # Warns if dossier with dummyData already has been added to the model
        else:
            flash(element["title"] + ' already exists in the model')
        
    # Commits the added dossiers
    db.session.commit()
    return 'Successfully populated model with dossiers!'


def Search(term, requiredInstances):
    matches = []
    
    # if requiredInstances is an empty string or lower than 1, sets it to 1
    if (requiredInstances == '') or (int(requiredInstances) <= 1):
        requiredInstances = 1

    # Makes sure the search term is not empty or whitespaces
    if (len(term) == 0) or term.isspace():
        matches.append('Invalid search term.')
    
    else:
        # a case insensitive query that checks if the dossier contains the search term in one, or multiple of the columns, and returns the results
        termQuery = Dossier.query.filter(
            or_(
                Dossier.title.contains(term),
                Dossier.protocol.contains(term),
                Dossier.poi.contains(term),
                Dossier.attachment.contains(term)
                )
            ).all()    
            
        # Checks if the dossier match from the query is greater than requiredInstances 
        for element in termQuery:
            count = 0

            count += element.title.count(term)
            count += element.protocol.count(term)
            count += element.poi.count(term)
            count += element.attachment.count(term)

            if count >= int(requiredInstances):
                titleColumn = str(element.title)
                protocolColumn = str(element.protocol)
                poiColumn = str(element.poi)
                attachmentColumn = str(element.attachment)

                dossierCopy = str(
                    titleColumn + '<br>' +
                    protocolColumn + '<br>' +
                    poiColumn + '<br>' +
                    attachmentColumn
                )

                # Highlights the term searched for in matches
                highlightedTerm = '<mark>' + term + '</mark>'
                dossierCopy = dossierCopy.replace(term, highlightedTerm)

                matches.append(
                    dossierCopy
                )

        if len(matches) == 0:
            matches.append('No dossiers were found with search criteria.')


    return matches


def Link(words, correlationCoefficient):
    links = []

    # If the correlationCoefficient is not set, it's set to a default value of 0.5
    if (correlationCoefficient == '') or (len(correlationCoefficient) == 0):
        correlationCoefficient = float(0.5)

    # Makes sure the words list is not empty or only containing whitespaces
    if (len(words) == 0) or (all('' == s or s.isspace() for s in words)):
        links.append('Invalid link term.')

    else:
        # If the correlationCoefficient and words is given as input, they're converted to the correct types
        float(correlationCoefficient)
        list(words)

        # Lists for storing query results
        queryResults = []

        # This currently works, but is inefficient as it queries the whole database model for each word in words 
        for word in words:
            columnLinkQuery = Dossier.query.filter(
                or_(
                    Dossier.title.contains(word),
                    Dossier.protocol.contains(word),
                    Dossier.poi.contains(word),
                    Dossier.attachment.contains(word),
                    )
                ).all()

            for result in columnLinkQuery:
                # Checks if the element already is in the list before adding it
                if result not in queryResults:
                    queryResults.append(result)

        
        for element in queryResults:
            titleColumn = str(element.title)
            protocolColumn = str(element.protocol)
            poiColumn = str(element.poi)
            attachmentColumn = str(element.attachment)

            # Checks for sameColumn links
            if (
                (all(w in titleColumn for w in words)) or
                (all(w in protocolColumn for w in words)) or
                (all(w in poiColumn for w in words)) or
                (all(w in attachmentColumn for w in words))
            ):

                dossierCopy = str(
                    titleColumn + '<br>' +
                    protocolColumn + '<br>' +
                    poiColumn + '<br>' +
                    attachmentColumn
                )

                for word in words:
                    replacedWord = '<mark>' + word + '</mark>'
                    dossierCopy = dossierCopy.replace(word, replacedWord)
        
                # Algorithm to determine link strength, as of now returns all sameColumn links as they are classified as strong links
                
                # Adds the dossier with highlighted links from sameColumn 
                links.append(
                    dossierCopy
                )


    return links