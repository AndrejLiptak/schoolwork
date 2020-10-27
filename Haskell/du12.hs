-- IB015 2019 - Kostra řešení dvanácté domácí úlohy
--   * V kostře nahraďte ‚undefined‘ vlastní implementací.
--   * Definicím funkcí můžete přidávat formální parametry.
--   * DULEŽITÉ: Zadané datové typy nemodifikujte.
--   * DŮLEŽITÉ: Zadaným funkcím neměňte typové signatury.
--   * DŮLEŽITÉ: Ke všem globálně definovaným funkcím uvádějte typovou signaturu.
--   * Řešení si zkuste spustit na Aise s GHC 8.6.
--   * Vyřešenou úlohu nahrajte do odevzdávárny své seminární skupiny.
-- Před tento řádek nic nepřidávejte
import Text.Read
import Data.List (words)


---------------------------------------------------
--      Z A D A N É   D A T O V É   T Y P Y      --
---------------------------------------------------

-- loď se seznamem příslušných koordinátů s pravdivostní hodnotou
-- podle toho, zda jsou zasaženy (True = zasažen, False = nezasažen)
data Ship = Ship [(Coord, Status)]
          deriving (Eq, Show)

-- moře jsou čtvercová
data ShipsPlan = ShipPlan Int [Ship]
               deriving (Eq, Show)

type Coord = (Int, Int)

data ShipOrientation = Horizontal
                     | Vertical
                     deriving Show

type ShipSize = Int

data Status = AsNew
            | Damaged
            deriving (Eq, Show)

data ShotResult = Ocean
                | Hit
                | Sunk
                deriving (Show, Eq)


---------------------------------------------------
--   F U N K C E   K   I M P L E M E N T A C I   --
---------------------------------------------------

isEmpty :: ShipsPlan -> Bool
isEmpty (ShipPlan _ []) = True
isEmpty (ShipPlan _ _) = False


addToShip :: Coord -> Ship -> Ship
addToShip (x,y) (Ship xs) = Ship (xs ++ [((x,y), AsNew)])

makeShip :: Coord -> ShipOrientation -> ShipSize -> Ship -> Ship
makeShip (x,y) _ 0 ship = ship
makeShip (x,y) Vertical size ship = makeShip (x,y+1) Vertical (size-1) (addToShip (x,y+1) ship)
makeShip (x,y) Horizontal size ship = makeShip (x+1,y) Horizontal (size-1) (addToShip (x+1,y) ship)


toShip :: Coord -> ShipOrientation -> ShipSize -> Ship
toShip (x,y) orient size =  makeShip (x,y) orient (size - 1) (Ship [((x,y), AsNew)])

fits :: Coord -> ShipOrientation -> ShipSize -> ShipsPlan -> Bool
fits (x,y) Vertical size (ShipPlan s _) = x <= s && y + size -1 <= s && x >= 1 && y >= 1
fits (x,y) Horizontal size (ShipPlan s _) = x + size -1 <= s && y <= s && x >= 1 && y >= 1

checkShip :: Coord -> ShipOrientation -> ShipSize -> Ship -> Bool
checkShip _ _ _ (Ship []) = True
checkShip (x,y) Vertical size (Ship (((x1, y1), _ ):xs)) = (x /= x1 || (x == x1 && y + size - 1 < y1) || (x == x1 && y  > y1)) && checkShip (x,y) Vertical size (Ship (xs))
checkShip (x,y) Horizontal size (Ship (((x1, y1), _):xs)) = (y /= y1 || (y == y1 && x + size - 1 < x1) || (y == y1 && x  > x1)) && checkShip (x,y) Horizontal size (Ship (xs))

notCollide :: Coord -> ShipOrientation -> ShipSize -> ShipsPlan -> Bool
notCollide (x,y) _ _ (ShipPlan _ []) = True
notCollide (x,y) orient size (ShipPlan m (s:xs)) = (checkShip (x,y) orient size s) && notCollide (x,y) orient size (ShipPlan m xs)


canInsert :: Coord -> ShipOrientation -> ShipSize -> ShipsPlan -> Bool
canInsert cord orient size plan = (fits cord orient size plan) && notCollide cord orient size plan

insertShip :: Ship -> ShipsPlan -> ShipsPlan
insertShip ship (ShipPlan x xs) =  ShipPlan x (ship : xs)

placeShip :: Coord -> ShipOrientation -> ShipSize -> ShipsPlan -> Maybe ShipsPlan
placeShip cord orient size plan =  if not (canInsert cord orient size plan) then Nothing
                                   else if size < 1 then Nothing
                                   else Just (insertShip (toShip cord orient size) plan)


shipHit :: Coord -> Ship -> Bool
shipHit _ (Ship []) = False
shipHit (x,y) (Ship (((x1,y1), _ ):ss)) = (x == x1 && y == y1) || shipHit (x,y) (Ship ss)

checkHit :: Coord -> ShipsPlan -> Bool
checkHit (x,y) (ShipPlan _ []) = False
checkHit (x,y) (ShipPlan m (s:ss)) = shipHit (x,y) s || checkHit (x,y) (ShipPlan m ss)

makeShipHit :: Coord -> [(Coord, Status)] -> [(Coord, Status)]
makeShipHit _ [] = []
makeShipHit (x,y) (((x1,y1), stat ):xs) = if x == x1 && y == y1 then ((x1,y1), Damaged) : xs else ((x1, y1), stat) : (makeShipHit (x,y) xs)


shipList :: Coord -> [Ship] -> [Ship]
shipList _ [] = []
shipList cord ((Ship info):xs) = (Ship (makeShipHit cord info)) : (shipList cord xs)

makeHit :: Coord -> ShipsPlan -> ShipsPlan
makeHit coord (ShipPlan m xs) = ShipPlan m (shipList coord xs)

checkShipSunk :: Ship -> Bool
checkShipSunk (Ship []) = True
checkShipSunk (Ship (( cord , Damaged):xs)) = True && checkShipSunk (Ship xs)
checkShipSunk (Ship (( cord , AsNew):xs)) = False

shouldSunk :: ShipsPlan -> Bool
shouldSunk (ShipPlan _ []) = False
shouldSunk (ShipPlan m (x:xs)) = checkShipSunk x || shouldSunk (ShipPlan m xs)

sunkenPlan :: [Ship] -> [Ship]
sunkenPlan [] = []
sunkenPlan (x:xs) = if checkShipSunk x then sunkenPlan xs else x : (sunkenPlan xs)

sunk :: ShipsPlan -> ShipsPlan
sunk (ShipPlan m xs) = ShipPlan m (sunkenPlan xs)

shoot :: Coord -> ShipsPlan -> (ShipsPlan, ShotResult)
shoot cord plan = if not (checkHit cord plan) then (plan, Ocean)
                  else if shouldSunk (makeHit cord plan) then ((sunk (makeHit cord plan)), Sunk)
                  else ((makeHit cord plan), Hit)


printPlan :: ShipsPlan -> IO ()
printPlan = undefined

game :: IO ()
game = undefined


---------------------------------------------------
--         P O M O C N É   F U N K C E           --
---------------------------------------------------

-- Pomocná funkce pro zpracování řádku načteného pro zadání lodě.
-- Funkce řeší pouze zpracování řádku zadávající loď a v případě,
-- že je tento vstup validní, vrací zpracované parametry zabalené
-- v Maybe. V opačném případě vrací Nothing.
-- Možná vás překvapí do-notace bez IO. Ve skutečnosti tu využíváme
-- toho, že Maybe je stejně jako IO tzv. monádou - podrobnosti pře-
-- sahují rámec tohoto kurzu. Nám stačí vědět, že (stejně jako u IO)
-- pokud nějaký z výpočtů selže (takže funkce z níž si vytahujeme
-- hodnotu pomocí "<-" vrátí Nothing), tak selže celá funkce jako
-- celek -> návratová hodnota bude Nothing. Můžete si zkusit volání
-- vyhodnotit:   parseShipInput "3 4 A 10"
-- (Výsledkem bude Nothing - selže parseOrientation. Všimněte si, že
-- není potřeba po každém volání kontrolovat, zdali volání funkce
-- uspělo - o to se nám postará do-notace, resp. funkce (>>) a (>>=)).
parseShipInput :: String -> Maybe (Coord, ShipOrientation, ShipSize)
parseShipInput input = if length inputs /= 4 then Nothing
                       else do
                            x <- readMaybe str_x
                            y <- readMaybe str_y
                            orientation <- parseOrientation str_or
                            size <- readMaybe str_size
                            return ((x, y), orientation, size)
    where
          inputs = words input
          [str_x, str_y, str_or, str_size] = inputs
          parseOrientation "V" = Just Vertical
          parseOrientation "H" = Just Horizontal
          parseOrientation  _  = Nothing


-- Analogicky pomocná funkce pro zpracování řádku načteného pro zadání souřadnic
-- pro střelbu.
parseShootInput :: String -> Maybe Coord
parseShootInput input = if length inputs /= 2 then Nothing
                        else do
                             x <- readMaybe str_x
                             y <- readMaybe str_y
                             return (x, y)
    where inputs = words input
          [str_x, str_y] = inputs


-- při kompilaci pomocí `ghc zadani12.hs -o <jméno_výstupního_souboru>` a následném
-- spuštění výsledné binárky se nám automaticky zavolá funkce game
main :: IO ()
main = game

