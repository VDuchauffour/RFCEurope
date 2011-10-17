// selectionGroupAI.cpp

#include "CvGameCoreDLL.h"
#include "CvSelectionGroupAI.h"
#include "CvPlayerAI.h"
#include "CvMap.h"
#include "CvPlot.h"
#include "CvTeamAI.h"
#include "CvDLLEntityIFaceBase.h"
#include "CvGameCoreUtils.h"
#include "FProfiler.h"
#include "CVInfos.h"

// Public Functions...

CvSelectionGroupAI::CvSelectionGroupAI()
{
	AI_reset();
}


CvSelectionGroupAI::~CvSelectionGroupAI()
{
	AI_uninit();
}


void CvSelectionGroupAI::AI_init()
{
	AI_reset();

	//--------------------------------
	// Init other game data
}


void CvSelectionGroupAI::AI_uninit()
{
}


void CvSelectionGroupAI::AI_reset()
{
	AI_uninit();

	m_iMissionAIX = INVALID_PLOT_COORD;
	m_iMissionAIY = INVALID_PLOT_COORD;

	m_bForceSeparate = false;

	m_eMissionAIType = NO_MISSIONAI;

	m_missionAIUnit.reset();

	m_bGroupAttack = false;
	m_iGroupAttackX = -1;
	m_iGroupAttackY = -1;
}


void CvSelectionGroupAI::AI_separate()
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);

		pLoopUnit->joinGroup(NULL);
		if (pLoopUnit->plot()->getTeam() == getTeam())
		{
			pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
		}
	}
}

void CvSelectionGroupAI::AI_seperateNonAI(UnitAITypes eUnitAI)
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();
	int iCounter = 0; //Rhye (loop fix)
	while (pEntityNode != NULL)
	{
		iCounter++; //Rhye (fix)
		if (iCounter > 20) break; //Rhye (fix)
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);
		if (pLoopUnit->AI_getUnitAIType() != eUnitAI)
		{
			pLoopUnit->joinGroup(NULL);
			if (pLoopUnit->plot()->getTeam() == getTeam())
			{
				pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
			}
		}
	}
}

void CvSelectionGroupAI::AI_seperateAI(UnitAITypes eUnitAI)
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();

	int iCounter = 0; //Rhye (possible loop fix)
	while (pEntityNode != NULL)
	{
		iCounter++; //Rhye (fix)
		if (iCounter > 20) break; //Rhye (fix)
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);
		if (pLoopUnit->AI_getUnitAIType() == eUnitAI)
		{
			pLoopUnit->joinGroup(NULL);
			if (plot()->getTeam() == getTeam())
			{
				pLoopUnit->getGroup()->pushMission(MISSION_SKIP);
			}
		}
	}
}
// Returns true if the group has become busy...
bool CvSelectionGroupAI::AI_update()
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;
	bool bDead;
	bool bFollow;

	PROFILE("CvSelectionGroupAI::AI_update");

	FAssert(getOwnerINLINE() != NO_PLAYER);

	//GC.getGameINLINE().logMsg(" AI_UPDATE Here 1 %d %d",getX(),getY()); // 3Miro
	/*if ( ( getX() == 94) && ( getY() == 6) ){
		GC.getGameINLINE().logMsg(" AI_Update Group Size %d",getNumUnits() ); // 3Miro
	};*/
	if (!AI_isControlled())
	{
		/*if ( ( getX() == 94) && ( getY() == 6) ){
			GC.getGameINLINE().logMsg(" AI_Update return controlled " ); // 3Miro
		};*/
		return false;
	}

	if (getNumUnits() == 0)
	{
		return false;
	}

	if (isForceUpdate())
	{
		/*if ( ( getX() == 94) && ( getY() == 6) ){
			GC.getGameINLINE().logMsg(" AI_Update is Forced Update " ); // 3Miro
		};*/
		clearMissionQueue(); // XXX ???
		setActivityType(ACTIVITY_AWAKE);
		setForceUpdate(false);

		// if we are in the middle of attacking with a stack, cancel it
		AI_cancelGroupAttack();
	}

	/*if ( ( getX() == 94) && ( getY() == 6) ){
		GC.getGameINLINE().logMsg(" AI_Update HERE 1" ); // 3Miro
	};*/

	FAssert(!(GET_PLAYER(getOwnerINLINE()).isAutoMoves()));

	int iTempHack = 0; // XXX

	bDead = false;
	
	//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2 "); // 3Miro
	bool bFailedAlreadyFighting = false;
	/*if ( ( getX() == 94) && ( getY() == 6) ){
		GC.getGameINLINE().logMsg(" AI_Update HERE 2" ); // 3Miro
	};*/
	while ((m_bGroupAttack && !bFailedAlreadyFighting) || readyToMove())
	{
		//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.1 "); // 3Miro
		iTempHack++;
		if (iTempHack > 100)
		{
			FAssert(false);
			CvUnit* pHeadUnit = getHeadUnit();
			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" head Unit: %d",pHeadUnit->getUnitType()); // 3Miro
			};*/
			if (NULL != pHeadUnit)
			{
				if (GC.getLogging())
				{
					TCHAR szOut[1024];
					CvWString szTempString;
					getUnitAIString(szTempString, pHeadUnit->AI_getUnitAIType());
					sprintf(szOut, "Unit stuck in loop: %S(%S)[%d, %d] (%S)\n", pHeadUnit->getName().GetCString(), GET_PLAYER(pHeadUnit->getOwnerINLINE()).getName(),
						pHeadUnit->getX_INLINE(), pHeadUnit->getY_INLINE(), szTempString.GetCString());
					gDLL->messageControlLog(szOut);
				}
				//GC.getGameINLINE().logMsg(" AI_UPDATE Stuck HERE Unit type: %d at %d %d",pHeadUnit->getUnitType(),pHeadUnit->getX(),pHeadUnit->getY() ); // 3Miro
				pHeadUnit->finishMoves();
			}
			break;
		}

		//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2 "); // 3Miro
		// if we want to force the group to attack, force another attack
		if (m_bGroupAttack)
		{
			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" AI_Update HERE 3: groupAttack" ); // 3Miro
			};*/
			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.1 "); // 3Miro
			m_bGroupAttack = false;

			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.2 "); // 3Miro
			groupAttack(m_iGroupAttackX, m_iGroupAttackY, MOVE_DIRECT_ATTACK, bFailedAlreadyFighting);
			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.3 "); // 3Miro
		}
		// else pick AI action
		else
		{
			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" AI_Update HERE 4: not groupAttack" ); // 3Miro
			};*/
			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.4 "); // 3Miro
			CvUnit* pHeadUnit = getHeadUnit();
			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.5 "); // 3Miro
			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" AI_Update HERE 4.1: head unit %d",pHeadUnit->getUnitType() ); // 3Miro
			};*/

			if (pHeadUnit == NULL || pHeadUnit->isDelayedDeath())
			{
				//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.6 "); // 3Miro
				break;
			}

			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" AI_Update HERE 4.2 " ); // 3Miro
			};*/

			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.7 "); // 3Miro
			resetPath();
			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.8 "); // 3Miro

			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" AI_Update HERE 4.3 " ); // 3Miro
			};*/

			if (pHeadUnit->AI_update())
			{
				/*if ( ( getX() == 94) && ( getY() == 6) ){
					GC.getGameINLINE().logMsg(" AI_Update HERE AI_Update foe hrad Unit " ); // 3Miro
				};*/
				// AI_update returns true when we should abort the loop and wait until next slice
				//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.9 "); // 3Miro
				break;
			}
			//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.2.10 "); // 3Miro
			/*if ( ( getX() == 94) && ( getY() == 6) ){
				GC.getGameINLINE().logMsg(" AI_Update HERE 4.4 " ); // 3Miro
			};*/
		}
			

		//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.3 "); // 3Miro
		if (doDelayedDeath())
		{
			bDead = true;
			break;
		}

		// if no longer group attacking, and force separate is true, then bail, decide what to do after group is split up
		// (UnitAI of head unit may have changed)
		//GC.getGameINLINE().logMsg(" AI_UPDATE Here 2.4 "); // 3Miro
		if (!m_bGroupAttack && AI_isForceSeparate())
		{
			AI_separate();	// pointers could become invalid...
			return true;
		}
	}

	//GC.getGameINLINE().logMsg(" AI_UPDATE Here 3 "); // 3Miro
	if (!bDead)
	{
		if (!isHuman())
		{
			bFollow = false;

			// if we not group attacking, then check for follow action
			if (!m_bGroupAttack)
			{
				pEntityNode = headUnitNode();

				while ((pEntityNode != NULL) && readyToMove(true))
				{
					pLoopUnit = ::getUnit(pEntityNode->m_data);
					pEntityNode = nextUnitNode(pEntityNode);

					if (pLoopUnit->canMove())
					{
						resetPath();

						if (pLoopUnit->AI_follow())
						{
							bFollow = true;
							break;
						}
					}
				}
			}

			if (doDelayedDeath())
			{
				bDead = true;
			}

			if (!bDead)
			{
				if (!bFollow && readyToMove(true))
				{
					pushMission(MISSION_SKIP);
				}
			}
		}
	}

	//GC.getGameINLINE().logMsg(" AI_UPDATE Here 4 "); // 3Miro
	if (bDead)
	{
		return true;
	}

	return (isBusy() || isCargoBusy());
}


// Returns attack odds out of 100 (the higher, the better...)
int CvSelectionGroupAI::AI_attackOdds(const CvPlot* pPlot, bool bPotentialEnemy) const
{
	CvUnit* pAttacker;

	FAssert(getOwnerINLINE() != NO_PLAYER);

	if (pPlot->getBestDefender(NO_PLAYER, getOwnerINLINE(), NULL, !bPotentialEnemy, bPotentialEnemy) == NULL)
	{
		return 100;
	}
	
	int iOdds = 0;
	pAttacker = AI_getBestGroupAttacker(pPlot, bPotentialEnemy, iOdds);

	if (pAttacker == NULL)
	{
		return 0;
	}

	return iOdds;
}


CvUnit* CvSelectionGroupAI::AI_getBestGroupAttacker(const CvPlot* pPlot, bool bPotentialEnemy, int& iUnitOdds, bool bForce, bool bNoBlitz) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	CvUnit* pBestUnit;
	int iPossibleTargets;
	int iValue;
	int iBestValue;
	int iOdds;
	int iBestOdds;

	iBestValue = 0;
	iBestOdds = 0;
	pBestUnit = NULL;

	pUnitNode = headUnitNode();

	bool bIsHuman = (pUnitNode != NULL) ? GET_PLAYER(::getUnit(pUnitNode->m_data)->getOwnerINLINE()).isHuman() : true;
			
	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (!pLoopUnit->isDead())
		{
			bool bCanAttack = false;
			if (pLoopUnit->getDomainType() == DOMAIN_AIR)
			{
				bCanAttack = pLoopUnit->canAirAttack();
			}
			else
			{
				bCanAttack = pLoopUnit->canAttack();

				if (bCanAttack && bNoBlitz && pLoopUnit->isBlitz() && pLoopUnit->isMadeAttack())
				{
					bCanAttack = false;
				}
			}

			if (bCanAttack)
			{
				if (bForce || pLoopUnit->canMove())
				{
					if (bForce || pLoopUnit->canMoveInto(pPlot, /*bAttack*/ true, /*bDeclareWar*/ bPotentialEnemy))
					{
						iOdds = pLoopUnit->AI_attackOdds(pPlot, bPotentialEnemy);
						
						iValue = iOdds;
						FAssertMsg(iValue > 0, "iValue is expected to be greater than 0");

						if (pLoopUnit->collateralDamage() > 0)
						{
							iPossibleTargets = std::min((pPlot->getNumVisibleEnemyDefenders(pLoopUnit) - 1), pLoopUnit->collateralDamageMaxUnits());

							if (iPossibleTargets > 0)
							{
								iValue *= (100 + ((pLoopUnit->collateralDamage() * iPossibleTargets) / 5));
								iValue /= 100;
							}
						}

						// if non-human, prefer the last unit that has the best value (so as to avoid splitting the group)
						if (iValue > iBestValue || (!bIsHuman && iValue > 0 && iValue == iBestValue))
						{
							iBestValue = iValue;
							iBestOdds = iOdds;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}
	
	iUnitOdds = iBestOdds;
	return pBestUnit;
}

CvUnit* CvSelectionGroupAI::AI_getBestGroupSacrifice(const CvPlot* pPlot, bool bPotentialEnemy, bool bForce, bool bNoBlitz) const
{
	int iBestValue = 0;
	CvUnit* pBestUnit = NULL;

	CLLNode<IDInfo>* pUnitNode = headUnitNode();
	while (pUnitNode != NULL)
	{
		CvUnit* pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (!pLoopUnit->isDead())
		{
			bool bCanAttack = false;
			if (pLoopUnit->getDomainType() == DOMAIN_AIR)
			{
				bCanAttack = pLoopUnit->canAirAttack();
			}
			else
			{
				bCanAttack = pLoopUnit->canAttack();

				if (bCanAttack && bNoBlitz && pLoopUnit->isBlitz() && pLoopUnit->isMadeAttack())
				{
					bCanAttack = false;
				}
			}

			if (bCanAttack)
			{
				if (bForce || pLoopUnit->canMove())
				{
					if (bForce || pLoopUnit->canMoveInto(pPlot, true))
					{
                        int iValue = pLoopUnit->AI_sacrificeValue(pPlot);
						FAssertMsg(iValue > 0, "iValue is expected to be greater than 0");

						// we want to pick the last unit of highest value, so pick the last unit with a good value
						if (iValue >= iBestValue)
						{
							iBestValue = iValue;
							pBestUnit = pLoopUnit;
						}
					}
				}
			}
		}
	}

	return pBestUnit;
}

// Returns ratio of strengths of stacks times 100
// (so 100 is even ratio, numbers over 100 mean this group is more powerful than the stack on a plot)
int CvSelectionGroupAI::AI_compareStacks(const CvPlot* pPlot, bool bPotentialEnemy, bool bCheckCanAttack, bool bCheckCanMove) const
{
	FAssert(pPlot != NULL);

	int	compareRatio;
	DomainTypes eDomainType = getDomainType();

	// if not aircraft, then choose based on the plot, not the head unit (mainly for transport carried units)
	if (eDomainType != DOMAIN_AIR)
	{
		if (pPlot->isWater())
			eDomainType = DOMAIN_SEA;
		else
			eDomainType = DOMAIN_LAND;

	}

	compareRatio = AI_sumStrength(pPlot, eDomainType, bCheckCanAttack, bCheckCanMove);
	compareRatio *= 100;

	PlayerTypes eOwner = getOwnerINLINE();
	if (eOwner == NO_PLAYER)
	{
		eOwner = getHeadOwner();
	}
	FAssert(eOwner != NO_PLAYER);
	
	int defenderSum = pPlot->AI_sumStrength(NO_PLAYER, getOwnerINLINE(), eDomainType, true, !bPotentialEnemy, bPotentialEnemy);
	compareRatio /= std::max(1, defenderSum);

	return compareRatio;
}

int CvSelectionGroupAI::AI_sumStrength(const CvPlot* pAttackedPlot, DomainTypes eDomainType, bool bCheckCanAttack, bool bCheckCanMove) const
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;
	int	strSum = 0;

	pUnitNode = headUnitNode();

	while (pUnitNode != NULL)
	{
		pLoopUnit = ::getUnit(pUnitNode->m_data);
		pUnitNode = nextUnitNode(pUnitNode);

		if (!pLoopUnit->isDead())
		{
			bool bCanAttack = false;
			if (pLoopUnit->getDomainType() == DOMAIN_AIR)
				bCanAttack = pLoopUnit->canAirAttack();
			else
				bCanAttack = pLoopUnit->canAttack();

			if (!bCheckCanAttack || bCanAttack)
			{
				if (!bCheckCanMove || pLoopUnit->canMove())
					if (!bCheckCanMove || pAttackedPlot == NULL || pLoopUnit->canMoveInto(pAttackedPlot, /*bAttack*/ true, /*bDeclareWar*/ true))
						if (eDomainType == NO_DOMAIN || pLoopUnit->getDomainType() == eDomainType)
							strSum += pLoopUnit->currEffectiveStr(pAttackedPlot, pLoopUnit);
			}
		}
	}

	return strSum;
}

void CvSelectionGroupAI::AI_queueGroupAttack(int iX, int iY)
{
	m_bGroupAttack = true;

	m_iGroupAttackX = iX;
	m_iGroupAttackY = iY;
}

inline void CvSelectionGroupAI::AI_cancelGroupAttack()
{
	m_bGroupAttack = false;
}

inline bool CvSelectionGroupAI::AI_isGroupAttack()
{
	return m_bGroupAttack;
}

bool CvSelectionGroupAI::AI_isControlled()
{
	return (!isHuman() || isAutomated());
}


bool CvSelectionGroupAI::AI_isDeclareWar(const CvPlot* pPlot)
{
	FAssert(getHeadUnit() != NULL);

	if (isHuman())
	{
		return false;
	}
	else
	{
		bool bLimitedWar = false;
		if (pPlot != NULL)
		{
			TeamTypes ePlotTeam = pPlot->getTeam();
			if (ePlotTeam != NO_TEAM)
			{
				WarPlanTypes eWarplan = GET_TEAM(getTeam()).AI_getWarPlan(ePlotTeam);
				if (eWarplan == WARPLAN_LIMITED)
				{
					bLimitedWar = true;
				}
			}
		}

		CvUnit* pHeadUnit = getHeadUnit();

		if (pHeadUnit != NULL)
		{
			switch (pHeadUnit->AI_getUnitAIType())
			{
			case UNITAI_UNKNOWN:
			case UNITAI_ANIMAL:
			case UNITAI_SETTLE:
			case UNITAI_WORKER:
				break;
			case UNITAI_ATTACK_CITY:
			case UNITAI_ATTACK_CITY_LEMMING:
				return true;
				break;

			case UNITAI_ATTACK:
			case UNITAI_COLLATERAL:
			case UNITAI_PILLAGE:
				if (bLimitedWar)
				{
					return true;
				}
				break;
				
			case UNITAI_PARADROP:
			case UNITAI_RESERVE:
			case UNITAI_COUNTER:
			case UNITAI_CITY_DEFENSE:
			case UNITAI_CITY_COUNTER:
			case UNITAI_CITY_SPECIAL:
			case UNITAI_EXPLORE:
			case UNITAI_MISSIONARY:
			case UNITAI_PROPHET:
			case UNITAI_ARTIST:
			case UNITAI_SCIENTIST:
			case UNITAI_GENERAL:
			case UNITAI_MERCHANT:
			case UNITAI_ENGINEER:
			case UNITAI_SPY:
			case UNITAI_ICBM:
			case UNITAI_WORKER_SEA:
				break;

			case UNITAI_ATTACK_SEA:
			case UNITAI_RESERVE_SEA:
			case UNITAI_ESCORT_SEA:
				if (bLimitedWar)
				{
					return true;
				}
				break;
			case UNITAI_EXPLORE_SEA:
				break;

			case UNITAI_ASSAULT_SEA:
				if (hasCargo())
				{
					return true;
				}
				break;

			case UNITAI_SETTLER_SEA:
			case UNITAI_MISSIONARY_SEA:
			case UNITAI_SPY_SEA:
			case UNITAI_CARRIER_SEA:
			case UNITAI_MISSILE_CARRIER_SEA:
			case UNITAI_PIRATE_SEA:
			case UNITAI_ATTACK_AIR:
			case UNITAI_DEFENSE_AIR:
			case UNITAI_CARRIER_AIR:
			case UNITAI_MISSILE_AIR:
				break;

			default:
				FAssert(false);
				break;
			}
		}
	}

	return false;
}


CvPlot* CvSelectionGroupAI::AI_getMissionAIPlot()
{
	return GC.getMapINLINE().plotSorenINLINE(m_iMissionAIX, m_iMissionAIY);
}


bool CvSelectionGroupAI::AI_isForceSeparate()
{
	return m_bForceSeparate;
}


void CvSelectionGroupAI::AI_makeForceSeparate()
{
	m_bForceSeparate = true;
}


MissionAITypes CvSelectionGroupAI::AI_getMissionAIType()
{
	return m_eMissionAIType;
}


void CvSelectionGroupAI::AI_setMissionAI(MissionAITypes eNewMissionAI, CvPlot* pNewPlot, CvUnit* pNewUnit)
{
	//GC.getGameINLINE().logMsg(" set mission AI Here 1 "); // 3Miro
	m_eMissionAIType = eNewMissionAI;

	//GC.getGameINLINE().logMsg(" set mission AI Here 2 "); // 3Miro
	if (pNewPlot != NULL)
	{
		m_iMissionAIX = pNewPlot->getX_INLINE();
		m_iMissionAIY = pNewPlot->getY_INLINE();
	}
	else
	{
		m_iMissionAIX = INVALID_PLOT_COORD;
		m_iMissionAIY = INVALID_PLOT_COORD;
	}

	//GC.getGameINLINE().logMsg(" set mission AI Here 3 "); // 3Miro
	if (pNewUnit != NULL)
	{
		m_missionAIUnit = pNewUnit->getIDInfo();
	}
	else
	{
		m_missionAIUnit.reset();
	}
	//GC.getGameINLINE().logMsg(" set mission AI Here 4 "); // 3Miro
}


CvUnit* CvSelectionGroupAI::AI_getMissionAIUnit()
{
	return getUnit(m_missionAIUnit);
}

bool CvSelectionGroupAI::AI_isFull()
{
	CLLNode<IDInfo>* pUnitNode;
	CvUnit* pLoopUnit;

	if (getNumUnits() > 0)
	{
		UnitAITypes eUnitAI = getHeadUnitAI();
		// do two passes, the first pass, we ignore units with speical cargo
		int iSpecialCargoCount = 0;
		int iCargoCount = 0;
		
		// first pass, count but ignore special cargo units
		pUnitNode = headUnitNode();

		while (pUnitNode != NULL)
		{
			pLoopUnit = ::getUnit(pUnitNode->m_data);
			pUnitNode = nextUnitNode(pUnitNode);
			if (pLoopUnit->AI_getUnitAIType() == eUnitAI)
			{
				if (pLoopUnit->cargoSpace() > 0)
				{
					iCargoCount++;
				}

				if (pLoopUnit->specialCargo() != NO_SPECIALUNIT)
				{
					iSpecialCargoCount++;
				}
				else if (!(pLoopUnit->isFull()))
				{
					return false;
				}
			}
		}
		
		// if every unit in the group has special cargo, then check those, otherwise, consider ourselves full
		if (iSpecialCargoCount >= iCargoCount)
		{
			pUnitNode = headUnitNode();
			while (pUnitNode != NULL)
			{
				pLoopUnit = ::getUnit(pUnitNode->m_data);
				pUnitNode = nextUnitNode(pUnitNode);
				
				if (pLoopUnit->AI_getUnitAIType() == eUnitAI)
				{
					if (!(pLoopUnit->isFull()))
					{
						return false;
					}
				}
			}
		}

		return true;
	}

	return false;	
}


CvUnit* CvSelectionGroupAI::AI_ejectBestDefender(CvPlot* pDefendPlot)
{
	CLLNode<IDInfo>* pEntityNode;
	CvUnit* pLoopUnit;

	pEntityNode = headUnitNode();
	
	CvUnit* pBestUnit = NULL;
	int iBestUnitValue = 0;

	while (pEntityNode != NULL)
	{
		pLoopUnit = ::getUnit(pEntityNode->m_data);
		pEntityNode = nextUnitNode(pEntityNode);
		
		if (!pLoopUnit->noDefensiveBonus())
		{
			int iValue = pLoopUnit->currEffectiveStr(pDefendPlot, NULL) * 100;
			
			if (pDefendPlot->isCity(true, getTeam()))
			{
				iValue *= 100 + pLoopUnit->cityDefenseModifier();
				iValue /= 100;
			}

			iValue *= 100;
			iValue /= (100 + pLoopUnit->cityAttackModifier() + pLoopUnit->getExtraCityAttackPercent());
			
			iValue /= 2 + pLoopUnit->getLevel();
			
			if (iValue > iBestUnitValue)
			{
				iBestUnitValue = iValue;
				pBestUnit = pLoopUnit;
			}
		}
	}
	
	if (NULL != pBestUnit && getNumUnits() > 1)
	{
		pBestUnit->joinGroup(NULL);
	}
	
	return pBestUnit;
}


// Protected Functions...

void CvSelectionGroupAI::read(FDataStreamBase* pStream)
{
	CvSelectionGroup::read(pStream);

	uint uiFlag=0;
	pStream->Read(&uiFlag);	// flags for expansion

	pStream->Read(&m_iMissionAIX);
	pStream->Read(&m_iMissionAIY);

	pStream->Read(&m_bForceSeparate);

	pStream->Read((int*)&m_eMissionAIType);

	pStream->Read((int*)&m_missionAIUnit.eOwner);
	pStream->Read(&m_missionAIUnit.iID);

	pStream->Read(&m_bGroupAttack);
	pStream->Read(&m_iGroupAttackX);
	pStream->Read(&m_iGroupAttackY);
}


void CvSelectionGroupAI::write(FDataStreamBase* pStream)
{
	CvSelectionGroup::write(pStream);

	uint uiFlag=0;
	pStream->Write(uiFlag);		// flag for expansion

	pStream->Write(m_iMissionAIX);
	pStream->Write(m_iMissionAIY);

	pStream->Write(m_bForceSeparate);

	pStream->Write(m_eMissionAIType);

	pStream->Write(m_missionAIUnit.eOwner);
	pStream->Write(m_missionAIUnit.iID);

	pStream->Write(m_bGroupAttack);
	pStream->Write(m_iGroupAttackX);
	pStream->Write(m_iGroupAttackY);
}

// Private Functions...
