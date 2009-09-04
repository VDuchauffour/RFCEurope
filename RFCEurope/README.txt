
Changes for Alpha 7
Incorporated 6.1 patch (from micbic)
New text entries for encyclopedia (compiled by merijn_v1)
Map modifications from St. Lucifer
New UHV reference maps
New Moscow city-name-map from Ptitsa Consul
Fixed bug with Arab UU



Changes since last version:
- Fixed Venician bug not allowing them to declare war to Independents
- Fixed a bug with the Crusaders conqering Jerusalem
- Changed the Spanish spawn date to 912AD, with Kiev and Hungary there were too many civs spawning too close to each other (chronologically)
- Nerfed the British Barbs
- Various Code optimizations to speed up the game
- UHVs are now readable under the victory info screen (almost entirely)
- Changed the names of Byzantium and Hungary to Romaii and Magyars
- Spanish spaw date moved to 912 (+1 turn), there were too many natoins (Hungary, Kiev and Spain) spawning too close to each other (more work is needed on this bug)
- Fixed a bug allowing a nation to resurect the next turn after they are conquered, the wait is now minimum 30 turns
- Resurections are generally less common
- Upon conversion to Protestantism, not all Buildings in a city get converted and some Faith is generated
- Some nations have high probability to start at war from spawn (i.e. Spain - Cordoba, Byzantium - Bulgaria)
- Slowed down the tech rate as Myri suggested, which nerfed Kiev reasonably
- Your advisor no longer suggests that you should liberate cities to the Pope
- Units leaving for the Crusade: fewer leave altogether, even fewer for newly spawned nations, 3 units in a city would no leave
- Mercenaries don't go on Crusades
- Taking over leadership for the Crusade and aiming it to Jerusalem, no longer wrongfully targets Burgundy
- The AI is less likely to change religions as it is aware of the loss of Faith Points
- Jewish Quartes give +1 Culture (we all know the Jews + Money jokes, but Jews contributed more than just trade and commerce to Mediaeval Europe)
- Barbs and Indipendents no longer build Prosecutors
- The AI doesn't go after Barbs and Indies outside its WarsMap, i.e. no more random French cities in eastern Russia
- Respawning civs can no longer make peace with the Barbs (this is RFC bug actually)
- Galleas now carry units + enter rival territory. Graphics should be better now. General Venecian sea units cannot enter foreign sea (i.e. removed the RFC Dutch UP form Venice)
- The AI should recognize Galleas and Gogge as transports
- Addes olives and modified version of Michael Vick's map (removed most of the roads mainly)
- Merged the map with the Updated Russian Map
- Added some Mediterranean Pirates, they will need to be balanced
- Bulgarian start moved to the accurate 680AD (since they are now strong enough) and Cordoban start moved to the more accurate 712AD
- Fixed the German UHV

Old changes for Alpha 5:
- Fixed a bug with the gold for the Human player taking over the Crusade
- Fixed a bug with the Genoa UHV
- Fixed a bug with the plague not being removed form cities flipping on spawn
- Fixed a bug making a lot of the colonies to be "National" Projects
- Fixed a bug that made Lousiana not require AA
- Lousiana now moved to the North American region
- Fixed a bug wrongly defining the continents, now the entire map is considered one continent (even Africa and Middle East)
- Nerfed the Viking and German barbs
- Added Faith Points, please read the Civilopedia
- Updated Civilopedia with information about Religions and Crusades
- One can no longer "liberate" cities to the Pope
- The non-Catholic AI is less likely to OB with the Pope
- the Pope is more likely to bribe for OB
- the Pope can now remove religion from the cities of a non-Catholic player (without asking)
- the free Great Artist moved from Music to Drama
- Added the Hungarian updated map. Hungary now looks much better

Old changes for Alpha 4:
- Fixed a bug regarding the Cordoban UHVs
- Removed the Longbowman city defense bonus, currently it is strong enough
- Fixed Cordoban and Genoa UHV bugs
- Arabia can now use their coffee resource.
- New colonies and access resources
- Fixed a bug giving Franks and Burgundians twice the normal starting force
- Increased the combat strength of the Norse Berserker to account for the improved defense of the Archers
- Map update by Jessicat, mainly Iceland (including update to the Norse UHV)
- You no longer have to be richer than the Pope to take over a Crusade, only richer than the rest of the Catholics
- Fixed a Dutch, Turkey and Sweden culture bug
- Balance tweaks: workers and settlers are cheaper, Byzantines have a slightly higher unit production penalty ....
- Fixed a Hungarian UHV bug (there might be more)
- Added light version of the mod. For people with weak machines that cannot read the new leaderheads: in Assets\XML\Civilzations, delete the file CIV4LeaderHeadInfos.xml and rename to CIV4LeaderHeadInfos.xml_light so that you remove the _light


Old changes for Alpha 3:
- The Pope no longer declares war if 2/3 victories have been won (other players still do)
- The Pope does not longer attack the independents
- New Leaderhead for Hungary
- Map change: moved one of the fish resources to fall in Alexandria's BFC (Alexandria was at a very bad location)
- Map change: some small changes on the Balkans, hopefully Simeon will now found Turnovo instead of Krayola and also get Iron
- Fixed Casimir's icon not showing
- Crusaders no longer spawn if Jerusalem changes ownership to Catholic or Orthodox on the way
- New star evaluations for Burgundy to Bulgaria
- Updated UHVs: Arabia, Bulgaria, France, Burgundy, Cordoba, Norse, Hungary, Germany, Venice, Genoa, Hungary, Poland, Kiev, Moscow, Ottomans, Dutch, Spain and Portugal
- Wonders now showing text in Russian
- Decreased the Portugal spawn area, moved one tile north
- Updated the Atlantic Islands, now it is possible to connect the resources.
- New Sound: Bulgarian unit speech and new opening menu song (comment on the song, I will remove it if people don't like it)
- New leader for Moscow: Ivan IV
- Spain now starts with no buildings (to compensate for the earlier start)
- Moscow starts with Granary, Barracks, Herbalist, Forge and Market (to compensate for the late start)
- Moscow starts with 4 workers
- Increased the AI danger awareness range, the AI should no longer lose Workers to Skirmishers and Horse Archers (as often)
- Decreased everyone's tech rate by 10%, this makes the game more interesting
- Decreased Crossbowman's city defence bonus to +25%
- AI is now aware of the incoming starting workers
- Tweaked some of the AI settlement rules, hopefully the AI will settle better now
- New city name map form micbic
- The Imperialism civic has been changes to something hopefully more useful

Old changes for Alpha 2:
- Fixed the bug of everyone having contact with the Pope from the very beginning
- Fixed a bug modifying religious love/hatred based upon the era. Now everything is uniform.
- Fixed the timing for the Kiev's UHV
- Kiev UHV now requires 10 grain resources
- Kiev spelling changes as suggested
- Added the Great Schism: Orthodox and Catholic players treat each other as "brothers in faith" until 1054AD
- Fixed the independent constant war bug, now all independents go to peace after some time
- Fixed a AI vs Independents war bug, used to be the AI wouldn't go to war against some independents
- Now Crusaders get siege Weapons as well (Jerusalem cannot fall otherwise)
- The first Catholic nation that captures Jerusalem gets the 8 tiles adjacent to it, i.e. establishes a small Crusader state and is not immediately devoured by the Arabic culture
- Try to make Crusader spawn not across the river from Jerusalem (less defensive bonuses for the city)
- Religion cannot be purged out of its holy city
- Religious prosecutions are not possible in Jerusalem
- Jerusalem and the various Holy Cities cannot be razed
- Fixed a bug making the AI agree on Defensive Pacts very easily
- Defensive Pacts between players of different religions is much less likely
- Defensive Pact trading now enables with Military Tradition (as opposed to Chivalry)
- Independent culture in cities dissolves with time, no more "... join motherland ..." 200 turns after you have conquered an indy city
- Fixed a bug that made sometimes Mongols in the middle of marshes (where they can get nowhere and no one can get to them)
- Bulgar/Kazan and Samara are no longer in the Moscowan spawn areas (Moscow now flip 4 as opposed to 6 cities)
- The Moscow UP now covers maintenance for the civics as well the cities themselves 
- Moscow UHV1 now requires to capture or destroy all Barbarian (Mongol) cities in what is essentially the territory of the former USSR (Riga doesn't count)
- Moscow UHV2 now requires 15 cities
- Fixed a bug that causes the game to become unstable if one has too many trade routes (especially for the Dutch)
- All colonies now require Atlantic Access (except for the two trading companies)
- All colonies but two require one TC or another (as per Jessiecat's idea)
- Atlantic Access locations have now changed. Only traditional colonial powers get AA, others have to trade or fight for control of Gibraltar or some other strategic location
- Minor map update on the Balkans (the Balkan mountain can now be crossed on several locations)
- The Pope can now build unlimited Missionaries and Prosecutors
- Tweaked the Pope's AI to go for the construction of more Missionaries and Prosecutors
- The Pope now sends his Prosecutors to other catholic nations and gifts them (needs to be tested)
- Updated the AI personalities of all leaders to better match their UHVs and situations
- Techs in the Tech tree have better tags for the AI (i.e. the benefits are correctly recognized as military vs gold vs culture)
- Updated visible areas upon spawn (not everything discussed is in, but being able to see land very far away will have no effect on the gameplay)
- Updated contacts on spawn (Byzantines now know the Pope, Kiev doesn't have to wait to meet Bulgaria and Byzantium and so on)
- New Leaderhead graphics for: Burgundy, Bulgaria, Norse, Kiev, Poland, Swedan and the Pope (still need Hungary, Cordoba, Genoa and Austria)
- Updated city name map from micbic
- Included the Russian Addon (I hope properly). There are only a few tags missing (3 + 1 that needs clarification), I have neither the Russian skill nor the tools to translate anything into the numerical values for Cyrillic, sorry!
- If you select to load the mod from the regular Civ Menu, you should immediately be taken to the Civ selection screen
- Iberian WB map update as Michael Vick requested, I hope I got it right


Old Changes for Alpha 1
- RFCEurope is now compatible with BtS 3.19 (and only with BtS 3.19)
IMPORTANT: This version only works with BtS patch 3.19. It will NOT work with 3.17.
WARNING: Due to the code merge, this version may be less stable than the previous ones. Report bugs.
- Portugal now has a UP (Power of Discovery)
- Fixed the Warmongering Pope bug
- Fixed the Pope demanding cities bug
- Fixed a bug that makes you loose the effect of the Round Church upon load/reload
- Fixed a bug that sometimes prevents you to convert to religion
- Fixed a bug that allows Crusaders to convert away from Catholicism
- All Papal units can enter Independents' territory w/o war
- Nerfed the Barbs on the Balkans
- Nerfed the Barbs on the British Isles
- Nerfed the Mongols
- Archers - Crossbowman - Longbowman - Musketman have a higher city defensive bonus (archers are now useful against Axeman and Horse Archers)
- Bulgarian Konnik now costs less than a Lancer, used to be ridiculously expensive
- Starting year, loading time and UHV/UP information now fully exported to XML, should be easier to update
- Updated the Spanish starting year info
- Also the five star ratings are exported to XML, someone should come up with accurate ratings for each Civ
- Map update on the Balkan terrain around Sofia to better represent the highest Balkan mountains and hopefully make the AI settle there (it was a large city even at that time)
- The Pope starts with Catholicism as State Religion
- The Byzantines start with Orthodoxy (their stability is bad without the extra anarchy)
- Projects generate points just like World Wonders
- The first Catholic player who manages to obtain control over Jerusalem will enter a golden age
- Civs start with their natural area of expansion visible (should help the AI settle better)


---- OLD
This is RFCEurope Test June 7th. RFCEurope is still in alpha. Please provide feedback at http://forums.civfanatics.com/showthread.php?t=298542

Changes:
New AI colony logic (3Miro)
Fixed bug with 2nd Norse UHV
Resurrection of civs now occurs in "Normal" areas, see Reference/Normal.png
Hungary start moved to Budapest
Constantinople has better production
Great scholar can now build Royal Academy
New city-name map (micbic)
Crusades now use Pope's city-name map (Jerusalem instead of Al Quds in announcement)
Spanish rivers and terrain slightly modified
Spanish start moved back to 909AD and start moved to Leon. New start date NOT reflected in starting screen, because I didn't have the latest dll source code.



TODO:
- Work on Stability
- Tweak the Unit cost
- Speed the Papal Prosecutor movement AI- Leaderheads needed for Cordoba, Genoa, Austria
- Temple Mount wonder vs Prosecution
- balance Germany and Austria
- Marocco barbs and pirates from Tunis and Algeres
- Faith Points for colonies?
- Templars as defensive Crusaders
- Attacking indies more aggressively
- German ss and eu
- Bulgarian speech Pohodat - 13 - 14 Voiskata e Gotova
- Check Religious attitude vs Arabia
