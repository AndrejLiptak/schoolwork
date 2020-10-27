-- IB015 2019 - Kostra řešení čtvrté domácí úlohy
--   * V kostře nahraďte ‚undefined‘ vlastní implementací.
--   * Definicím funkcí můžete přidávat formální parametry.
--   * DŮLEŽITÉ: Neodstraňujte žádné zadané funkce.
--   * DŮLEŽITÉ: Ke všem funkcím uvádějte typovou signaturu.
--   * Řešení si zkuste spustit na Aise s GHC 8.6.
--   * Vyřešenou úlohu nahrajte do odevzdávárny své seminární skupiny.

-- Před tento řádek nic nepřidávejte
import Data.List

type ShowID = Int
type ShowName = String
type Rating = Int
type EpisodeNumber = Int
type Year = Int
type EpisodeName = String

type ShowInfo = (ShowID, ShowName, Rating)
type EpisodeInfo = (ShowID, EpisodeNumber, Year, EpisodeName)

type Shows = [ShowInfo]
type Episodes = [EpisodeInfo]

-- Get funckie

getShowName :: ShowInfo -> ShowName
getShowName (_, x, _) = x

getShowIdFromShows :: Shows -> ShowID
getShowIdFromShows [] = -1
getShowIdFromShows ((x,_,_):xs) = x

getEpYear :: EpisodeInfo -> Year
getEpYear (_, _, x, _) = x

episodeGetShowId :: EpisodeInfo -> ShowID
episodeGetShowId (x, _, _, _) = x

getRating :: ShowInfo -> Rating
getRating (_, _, r) = r

highestR :: Shows -> Rating
highestR sh = maximum $ map getRating sh

lowestR :: Shows -> Rating
lowestR sh = minimum $ map getRating sh

getEpName :: EpisodeInfo -> EpisodeName
getEpName (_, _, _, x) = x

getShowId :: ShowInfo -> ShowID
getShowId (x, _, _) = x

getShowNameByShowID :: Shows -> ShowID -> ShowName
getShowNameByShowID sh wanted = getShowName $ head $ filter (\x -> getShowId x == wanted) sh

-- Fukncie k implemetnacii

findShowId :: Shows -> ShowName -> ShowID
findShowId sh wantedName = getShowIdFromShows $ filter fun sh
                       where fun episode = getShowName episode == wantedName

getEpisodes :: Episodes -> ShowID -> Episodes
getEpisodes ep myId = filter fun ep
                      where fun episode = episodeGetShowId episode == myId

countEpisodes :: Episodes -> ShowID -> Int
countEpisodes ep wanted= length $ filter fun ep
                         where fun episode = episodeGetShowId episode == wanted

isShowContiguous :: Episodes -> ShowID -> Bool
isShowContiguous ep wanted = all (\(x, y) -> x == y || x +1 == y) $ myZip $ sort $ map getEpNum $ filter isEqual ep
                            where isEqual x = episodeGetShowId x == wanted
                                  getEpNum (_, x, _, _) = x
                                  myZip x = zip (head x : x)  x

publicationRange :: Episodes -> ShowID -> (Year, Year)
publicationRange ep wanted = years $ map getEpYear $ filter (\x -> episodeGetShowId x == wanted) ep
                            where years x = (minimum x, maximum x)

bestRating :: Shows -> ShowName
bestRating sh = head $ map getShowName $ filter (\x -> getRating x == highestR sh ) sh

worstRating :: Shows -> ShowName
worstRating sh = head $ map getShowName $ filter (\x -> getRating x == lowestR sh ) sh

sortByYearOfPublication :: Episodes -> Episodes
sortByYearOfPublication eps = sortOn getEpYear eps


showEpisodes :: Shows -> Episodes -> [(ShowName, [EpisodeName])]
showEpisodes sh ep =map f $ [(i,j) | i <- map getShowId sh,
                                     j <- [map getEpName $ getEpisodes ep i]]
                    where f (x,y) = (getShowNameByShowID sh x,y)

join :: Shows -> Episodes -> [(ShowName, EpisodeName)]
join sh ep = map changeIdForName $ [(i,j) | i <- map getShowId sh,
                              j <- map getEpName (getEpisodes ep i) ]
                 where changeIdForName (x,y) = (getShowNameByShowID sh x,y)

-- 8< -----------------------------------------------------------------------
-- Testovací data (doporučujeme přidat vlastní)

shs :: Shows
shs = [(  4, "Ajtaci",         88)
      ,( 45, "Mentalista",     70)
      ,( 48, "Miranda",        84)
      ,( 51, "Vondra",          84)
      ,(129, "Zdivocela zeme", 71)
      ,(16,"\"Edge Cases\"",-42)
      ,(17,"\"Edge Cases\"",-42)
      ]

eps :: Episodes
eps = [( 4,   1, 2006, "Vcerejsi odpad")
      ,(45,  56, 2010, "Vesely rudy skritek")
      ,( 4,   4, 2006, "Cervene dvere")
      ,(45, 124, 2013, "Rudy John")
      ,(48,   8, 2010, "Smutecni rec")
      ,(51,   4, 2019, "")
      ,( 4,   6, 2006, "Prijizdi teta Irma")
      ,( 4,   2, 2006, "Kalamity Jen")
      ,(51,   3, 2019, "")
      ,(45,   2, 2008, "Rude vlasy a stribrna paska")
      ,(48,   4, 2009, "Dovolena")
      ,(45,  77, 2011, "Rude probleskujici svetlo")
      ,(51,   5, 2019, "")
      ,(16, 2, 2018, "Almsot same")
      ]