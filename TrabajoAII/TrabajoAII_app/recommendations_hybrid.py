#encoding: latin1

from TrabajoAII_app.models import Genre, SteamTag, Rating

def hybridRecommendation(collaborativeFilteringRecommendations):
    recommendations = list()
    
    for g in collaborativeFilteringRecommendations:
        genres = set()
        tags = set()
        
        for genre in Genre.objects.all():
            if g in genre.games.all():
                genres.add(genre.name)
        
        for tag in SteamTag.objects.all():
            if g in tag.games.all():
                tags.add(tag.tagName)
                
        intersection = genres.intersection(tags)
        ratingByCoincidences = len(intersection)
        
        ratings = Rating.objects.filter(game = g)
        ratingByAssessments = 0
        
        for r in ratings:
            ratingByAssessments += r.rating
            
        totalRating = ratingByCoincidences + ratingByAssessments
        gameAndRating = (g, totalRating)
                
        recommendations.append(gameAndRating)
    
    fixedRecommendations = list()
    if len(recommendations) > 10:
        fixedRecommendations = sortRecommendationsByRating(recommendations)[0:9]
    else:
        fixedRecommendations = recommendations
    
    result = list()
    for recom in fixedRecommendations:
        result.append(recom[0])
    
    print(result)
        
    return result
        

def sortRecommendationsByRating(recommendations):
    return sorted(recommendations, key=lambda recom: recom[1])
        