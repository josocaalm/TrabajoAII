#encoding: latin1

from TrabajoAII_app.models import Genre, SteamTag

def gamesRecommendationBasedOnLikedGenres(userApp):
    likedGenres = set()
    recommendations = list()
    
    for genre in Genre.objects.all():
        if userApp in genre.usersApp.all():
            likedGenres.add(genre)
                
    coincidencesBetweenGenresAndTags = set()
    
    for likedGenre in likedGenres:
        for tag in SteamTag.objects.all():
            if likedGenre.name == tag.tagName:
                coincidencesBetweenGenresAndTags.add(tag.tagName)
        
    if coincidencesBetweenGenresAndTags:
        for coincidence in coincidencesBetweenGenresAndTags:
            relatedTag = SteamTag.objects.get(tagName = coincidence)
            recommendations.extend(relatedTag.games.all())
        
    return set(recommendations)