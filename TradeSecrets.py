from MainClasses import *

def adf():
    
    """
    creates the ADF for the domain
    """
    
    adf = ADF('TradeSecrets')
    
    #non-leaf factors
    adf.addNodes('Decide',['( not DefendantOwnershipRights ) and ( TradeSecretMisappropriation and ( ImproperMeans or ConfidentialRelationship ) )'],['a trade secret was misappropriated, find for plaintiff','no trade secret was misappropriated, find for defendant'])
    adf.addNodes('TradeSecretMisappropriation',['EffortstoMaintainSecrecy and InfoValuable and not InfoKnownOrAvailiable'],['information was a trade secret','information was not a trade secret']) 
    adf.addNodes('EffortstoMaintainSecrecy',['SecurityMeasures or MaintainSecrecyDefendant or MaintainSecrecyOutsiders or not NoSecurityMeasures'],['efforts were taken to maintain secrecy','no efforts were taken to maintain secrecy'])
    adf.addNodes('InfoValuable',['UniqueProduct or CompetitiveAdvantage or not InfoKnownOrAvailiable'],['the information was valuable','the information was not valuable'])
    adf.addNodes('InfoKnownOrAvailiable',['InfoKnown or InfoAvailiableElsewhere'],['the information was known or availiable','the information was neither known nor availiable'])
    adf.addNodes('InfoKnown',['InfoKnownToCompetitors and not UniqueProduct'],['information is known','information is not known'])
    adf.addNodes('InfoAvailiableElsewhere',['( InfoReverseEngineerable or InfoObtainableElsewhere ) and not ( InfoReverseEngineerable and ( RestrictedMaterialsUsed or IdenticalProducts ) )'],['the information was availiable elsewhere','the information was not availiable elsewhere'])
    adf.addNodes('ImproperMeans',['QuestionableMeans and not LegitimatelyObtainable'],['improper means were used','improper means were not used'])
    adf.addNodes('QuestionableMeans',['( not InfoReverseEngineered and not InfoIndependentlyGenerated ) and ( InvasiveTechniques or Deception or RestrictedMaterialsUsed or BribeEmployee )'],['questionable means were used','questionable means were not used'])
    adf.addNodes('InfoUsed',['BroughtTools or IdenticalProducts or CompetitiveAdvantage or not InfoIndependentlyGenerated'],['the information was used','the information was not used'])
    adf.addNodes('ConfidentialRelationship',['NoticeOfConfidentiality or ConfidentialityAgreement'],['there was a confidential relationship','there was no confidential relationship'])
    adf.addNodes('NoticeOfConfidentiality',['WaiverOfConfidentiality or KnewInfoConfidential or RestrictedMaterialsUsed or NoncompetitionAgreement or AgreedNotToDisclose'],['defendant was on notice of confidentiality','defendant was not on notice of confidentiality']) 
    adf.addNodes('LegitimatelyObtainable',['InfoKnownOrAvailiable and not QuestionableMeans'],['the information was legitimately obtained','the information was not legitimately obtained'])   
    adf.addNodes('ConfidentialityAgreement',['AgreedNotToDisclose and not WaiverOfConfidentiality'],['there was a confidentiality agreement','there was no confidentiality agreement']) 
    adf.addNodes('MaintainSecrecyDefendant',['AgreedNotToDisclose'],['efforts made vis a vis defendant','no efforts made vis a vis defendant']) 
    adf.addNodes('MaintainSecrecyOutsiders',['OutsiderDisclosuresRestricted'],['efforts made vis a vis outsiders','no efforts made vis a vis outsiders']) 
    adf.addNodes('DefendantOwnershipRights',['EmployeeSoleDeveloper'],['defendant is owner of secret','defendant is not owner of secret'])
    
    #leaf factors and questions
    adf.addNodes('BribeEmployee',question='Did the defendant offer the plaintiff\'s current or former employee an incentive to work for the defendant?')
    adf.addNodes('EmployeeSoleDeveloper',question='Was the defendant the sole developer of the product whilst employed by the plaintiff?') 
    adf.addNodes('AgreedNotToDisclose',question='Had the defendant entered into a non-disclosure agreement with the plaintiff?')
    adf.addNodes('SecurityMeasures',question='Did the plaintiff take measures to ensure the security of its information?') 
    adf.addNodes('BroughtTools',question='Did an employee of the plaintiff give product development information to the defendant?') 
    adf.addNodes('CompetitiveAdvantage',question='Did the plaintiff\'s product information allow the defendant to save time or expense?')
    adf.addNodes('OutsiderDisclosuresRestricted',question='Was the plaintiff\'s disclosure to outsiders subject to confidential restrictions?')
    adf.addNodes('NoncompetitionAgreement',question='Had the plantiff and the defendant entered into a noncompetition agreement?')
    adf.addNodes('RestrictedMaterialsUsed',question='Did the defendant use materials that were subject to confidentiality restrictions?')
    adf.addNodes('UniqueProduct',question='Is the product of the plaintiff unique?')
    adf.addNodes('InfoReverseEngineerable',question='Could the plaintiff\'s product information have been learned by reverse engineering?')
    adf.addNodes('InfoIndependentlyGenerated',question='Did the defendant develop its product through independent research?')
    adf.addNodes('IdenticalProducts',question='Was the defendant\'s product identical to the plaintiff\'s?')
    adf.addNodes('NoSecurityMeasures',question='Did the plaintiff not adopt any security measures to maintain the secrecy of their information?')
    adf.addNodes('InfoKnownToCompetitors',question='Was the plaintiff\'s information known to competitors?')
    adf.addNodes('KnewInfoConfidential',question='Did the defendant know the plaintiff\'s information was confidential?') 
    adf.addNodes('InvasiveTechniques',question='Did the defendant use invasive techniques to gain access to the plaintiff\'s information? ')
    adf.addNodes('WaiverOfConfidentiality',question='Had the plaintiff entered into an agreement that waived confidentiality?')
    adf.addNodes('InfoObtainableElsewhere',question='Could the information have been obtained from publicly availiable sources?')
    adf.addNodes('InfoReverseEngineered',question='Did the defendant discover the plaintiff\'s product information through reverse engineering?' )
    adf.addNodes('Deception',question='Did the defendant obtain the plaintiff\'s information through deception?')
    
    adf.questionOrder = ['BribeEmployee','EmployeeSoleDeveloper','AgreedNotToDisclose','SecurityMeasures','BroughtTools','CompetitiveAdvantage','OutsiderDisclosuresRestricted','NoncompetitionAgreement','RestrictedMaterialsUsed','UniqueProduct','InfoReverseEngineerable','InfoReverseEngineered','InfoIndependentlyGenerated','IdenticalProducts','NoSecurityMeasures','InfoKnownToCompetitors','KnewInfoConfidential','InvasiveTechniques','WaiverOfConfidentiality','InfoObtainableElsewhere','Deception']
    
    return adf

def cases():
    """
    test cases
    """
    arco = ['SecretsDisclosedOutsiders', 'InfoReverseEngineerable','InfoKnownToCompetitors'] #pass
    boeing = ['AgreedNotToDisclose','SecurityMeasures','OutsiderDisclosuresRestricted','RestrictedMaterialsUsed','KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders'] #pass
    bryce = ['AgreedNotToDisclose','SecurityMeasures','IdenticalProducts','KnewInfoConfidential','DisclosureInNegotations'] #pass
    collegeWatercolour = ['UniqueProduct','Deception','DisclosureInNegotations'] #pass
    denTalEz = ['AgreedNotToDisclose','SecurityMeasures','KnewInfoConfidential','Deception','DisclosureInNegotations'] #pass
    ecolgix = ['KnewInfoConfidential','DisclosureInNegotations','NoSecurityMeasures','WaiverOfConfidentiality'] #pass
    emery = ['IdenticalProducts','KnewInfoConfidential','SecretsDisclosedOutsiders'] #pass
    ferranti = ['BribeEmployee','InfoIndependentlyGenerated','NoSecurityMeasures','InfoKnownToCompetitors','DisclosureInPublicForum'] #pass
    robinson = ['IdenticalProducts','Deception','DisclosureInNegotations','SecretsDisclosedOutsiders','NoSecurityMeasures'] #pass
    sandlin = ['DisclosureInNegotations','SecretsDisclosedOutsiders','InfoReverseEngineerable','NoSecurityMeasures','DisclosureInPublicForum'] #pass
    sheets = ['IdenticalProducts','NoSecurityMeasures','DisclosureInPublicForum'] #pass
    spaceAero = ['CompetitiveAdvantage','UniqueProduct','IdenticalProducts','DisclosureInNegotations','NoSecurityMeasures'] #pass
    televation = ['SecurityMeasures','OutsiderDisclosuresRestricted','UniqueProduct','IdenticalProducts','KnewInfoConfidential','SecretsDisclosedOutsiders','InfoReverseEngineerable'] #pass
    yokana = ['BroughtTools','SecretsDisclosedOutsiders','InfoReverseEngineerable','DisclosureInPublicForum'] #pass
    cm1 = ['AgreedNotToDisclose','SecurityMeasures','InfoKnownToCompetitors','InfoIndependentlyGenerated','InfoReverseEngineerable','SecretsDisclosedOutsiders','DisclosureInPublicForum'] #pass
    digitalDevelopment = ['SecurityMeasures','CompetitiveAdvantage','UniqueProduct','IdenticalProducts','KnewInfoConfidential','DisclosureInNegotations'] #pass
    fmc = ['AgreedNotToDisclose','SecurityMeasures','BroughtTools','OutsiderDisclosuresRestricted','SecretsDisclosedOutsiders','VerticalKnowledge'] #pass
    forrest = ['SecurityMeasures','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations'] #pass
    goldberg = ['KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders','DisclosureInPublicForum'] #pass
    kg = ['SecurityMeasures','RestrictedMaterialsUsed','UniqueProduct','IdenticalProducts','KnewInfoConfidential','InfoReverseEngineerable','InfoReverseEngineered'] #pass
    laser = ['SecurityMeasures','OutsiderDisclosuresRestricted','KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders'] #pass
    lewis = ['CompetitiveAdvantage','KnewInfoConfidential','DisclosureInNegotations'] #pass
    mbl = ['AgreedNotToDisclose','SecurityMeasures','NoncompetitionAgreement','AgreementNotSpecific','SecretsDisclosedOutsiders','InfoKnownToCompetitors'] #pass
    mason = ['SecurityMeasures','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations','InfoReverseEngineerable'] #pass
    mineralDeposits = ['IdenticalProducts','RestrictedMaterialsUsed','DisclosureInNegotations','InfoReverseEngineerable','InfoReverseEngineered'] #pass
    nationalInstruments = ['IdenticalProducts','KnewInfoConfidential','DisclosureInNegotations'] #pass
    nationalRejectors = ['BroughtTools','UniqueProduct','IdenticalProducts','SecretsDisclosedOutsiders','InfoReverseEngineerable','NoSecurityMeasures','DisclosureInPublicForum'] #pass
    reinforced = ['AgreedNotToDisclose','SecurityMeasures','CompetitiveAdvantage','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations'] #pass
    scientology = ['AgreedNotToDisclose','SecurityMeasures','OutsiderDisclosuresRestricted','SecretsDisclosedOutsiders','VerticalKnowledge','InfoKnownToCompetitors'] #pass
    technicon = ['SecurityMeasures','OutsiderDisclosuresRestricted','RestrictedMaterialsUsed','KnewInfoConfidential','SecretsDisclosedOutsiders','InfoReverseEngineerable','InfoReverseEngineered'] #pass
    trandes = ['AgreedNotToDisclose','SecurityMeasures','OutsiderDisclosuresRestricted','DisclosureInNegotations','SecretsDisclosedOutsiders'] #pass
    valcoCincinnati = ['SecurityMeasures','OutsiderDisclosuresRestricted','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders'] #pass
    
    cases = {'Arco Industries Corp v Chemcast Corp':arco, 'The Boeing Company v Sierracin Corp':boeing,'M. Bryce & Associates Inc v Gladstone':bryce, 'College Watercolour Group Inc v William H. Newbauer':collegeWatercolour,'Den-Tal-Ez Inc v Siemens Capital Corp':denTalEz,'Ecolgix Inc v Fantsteel Inc':ecolgix,'A.H. Emery Co v Marcon Products Corp':emery,'Ferranti Electric Inc v Harwood':ferranti,'Commonwealth v Robinson':robinson,'Sandlin v Johnson':sandlin,'Sheets v Yamaha Motors Corp':sheets,'Space Aero Products Corp v R.E. Darling Corp':spaceAero,'Televation Telecommunications Systems Inc v Saindon':televation,'Midland-Ross Corp v Yokana':yokana,'CMI Corp v Jakob':cm1,'Digital Development Corp v International Memory Systems':digitalDevelopment,'FMC Corp v Taiwan Tainan Giant Ind Co Ltd':fmc,'Forest Laboratories Inc v Formulations Inc':forrest,'Goldberg v Medtronic':goldberg,'K & G Oil Tool & Services Co v G & G':kg,'Laser Industries Ltd v Eder Instrument Co':laser,'Computer Print Systems v Lewis':lewis,'MBL (USA) Corp v Diekman':mbl,'Mason v Jack Daniel Distillery':mason,'Mineral Deposits Ltd v Zigan':mineralDeposits,'National Instruments Labs Inc v Hycel Inc':nationalInstruments,'National Rejectors Inc v Trieman':nationalRejectors,'Reinforced':reinforced,'Scientology':scientology, 'Technicon Data Systems Corp v Curtis':technicon,'Trandes Corp v Guy F. Atkinson Co':trandes,'Valco Cincinnati Inc v N & D Machining Service Inc':valcoCincinnati}
    
    return cases

def expectedOutcomeCases():
    """
    first factor is the outcome, the other factors are the same as in the prolog program 
    """
    arco = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','EffortstoMaintainSecrecy','InfoKnownOrAvailiable','InfoKnown','InfoAvailiableElsewhere','InfoUsed', 'SecretsDisclosedOutsiders', 'InfoReverseEngineerable','InfoKnownToCompetitors']
    boeing = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','ImproperMeans','QuestionableMeans','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant','MaintainSecrecyOutsiders', 'AgreedNotToDisclose','SecurityMeasures','OutsiderDisclosuresRestricted','RestrictedMaterialsUsed','KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders']
    bryce = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant', 'AgreedNotToDisclose','SecurityMeasures','IdenticalProducts','KnewInfoConfidential','DisclosureInNegotations']
    collegeWatercolour = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','ImproperMeans','QuestionableMeans','InfoUsed', 'UniqueProduct','Deception','DisclosureInNegotations']
    denTalEz = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','ImproperMeans','QuestionableMeans','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant', 'AgreedNotToDisclose','SecurityMeasures','KnewInfoConfidential','Deception','DisclosureInNegotations']
    ecolgix = ['no trade secret was misappropriated, find for defendant','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'KnewInfoConfidential','DisclosureInNegotations','NoSecurityMeasures','WaiverOfConfidentiality']
    emery = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'IdenticalProducts','KnewInfoConfidential','SecretsDisclosedOutsiders']
    ferranti = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','InfoKnownOrAvailiable','InfoKnown', 'BribeEmployee','InfoIndependentlyGenerated','NoSecurityMeasures','InfoKnownToCompetitors','DisclosureInPublicForum']
    robinson = ['no trade secret was misappropriated, find for defendant','InfoValuable','ImproperMeans','QuestionableMeans','InfoUsed','IdenticalProducts','Deception','DisclosureInNegotations','SecretsDisclosedOutsiders','NoSecurityMeasures']
    sandlin = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','InfoKnownOrAvailiable','InfoAvailiableElsewhere','InfoUsed','DisclosureInNegotations','SecretsDisclosedOutsiders','InfoReverseEngineerable','NoSecurityMeasures','DisclosureInPublicForum']
    sheets = ['no trade secret was misappropriated, find for defendant','InfoValuable','InfoUsed', 'IdenticalProducts','NoSecurityMeasures','DisclosureInPublicForum']
    spaceAero = ['no trade secret was misappropriated, find for defendant','InfoValuable','InfoUsed', 'CompetitiveAdvantage','UniqueProduct','IdenticalProducts','DisclosureInNegotations','NoSecurityMeasures']
    televation = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','MaintainSecrecyOutsiders', 'SecurityMeasures','OutsiderDisclosuresRestricted','UniqueProduct','IdenticalProducts','KnewInfoConfidential','SecretsDisclosedOutsiders','InfoReverseEngineerable']
    yokana = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','EffortstoMaintainSecrecy','InfoKnownOrAvailiable','InfoAvailiableElsewhere','InfoUsed', 'BroughtTools','SecretsDisclosedOutsiders','InfoReverseEngineerable','DisclosureInPublicForum']
    cm1 = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','EffortstoMaintainSecrecy','InfoKnownOrAvailiable','InfoKnown','InfoAvailiableElsewhere','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant', 'AgreedNotToDisclose','SecurityMeasures','InfoKnownToCompetitors','InfoIndependentlyGenerated','InfoReverseEngineerable','SecretsDisclosedOutsiders','DisclosureInPublicForum']
    digitalDevelopment = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'SecurityMeasures','CompetitiveAdvantage','UniqueProduct','IdenticalProducts','KnewInfoConfidential','DisclosureInNegotations']
    fmc = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant','MaintainSecrecyOutsiders','AgreedNotToDisclose','SecurityMeasures','BroughtTools','OutsiderDisclosuresRestricted','SecretsDisclosedOutsiders','VerticalKnowledge']
    forrest = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'SecurityMeasures','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations']
    goldberg = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders','DisclosureInPublicForum']
    kg = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'SecurityMeasures','RestrictedMaterialsUsed','UniqueProduct','IdenticalProducts','KnewInfoConfidential','InfoReverseEngineerable','InfoReverseEngineered']
    laser = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','MaintainSecrecyOutsiders', 'SecurityMeasures','OutsiderDisclosuresRestricted','KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders']
    lewis = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'CompetitiveAdvantage','KnewInfoConfidential','DisclosureInNegotations']
    mbl = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','EffortstoMaintainSecrecy','InfoKnownOrAvailiable','InfoKnown','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant', 'AgreedNotToDisclose','SecurityMeasures','NoncompetitionAgreement','AgreementNotSpecific','SecretsDisclosedOutsiders','InfoKnownToCompetitors']
    mason = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','EffortstoMaintainSecrecy','InfoValuable','InfoKnownOrAvailiable','InfoAvailiableElsewhere','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'SecurityMeasures','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations','InfoReverseEngineerable']
    mineralDeposits = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'IdenticalProducts','RestrictedMaterialsUsed','DisclosureInNegotations','InfoReverseEngineerable','InfoReverseEngineered']
    nationalInstruments = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality', 'IdenticalProducts','KnewInfoConfidential','DisclosureInNegotations']
    nationalRejectors = ['no trade secret was misappropriated, find for defendant','InfoValuable','InfoUsed', 'BroughtTools','UniqueProduct','IdenticalProducts','SecretsDisclosedOutsiders','InfoReverseEngineerable','NoSecurityMeasures','DisclosureInPublicForum']
    reinforced = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant', 'AgreedNotToDisclose','SecurityMeasures','CompetitiveAdvantage','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations']
    scientology = ['no trade secret was misappropriated, find for defendant','LegitimatelyObtainable','EffortstoMaintainSecrecy','InfoKnownOrAvailiable','InfoKnown','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant','MaintainSecrecyOutsiders', 'AgreedNotToDisclose','SecurityMeasures','OutsiderDisclosuresRestricted','SecretsDisclosedOutsiders','VerticalKnowledge','InfoKnownToCompetitors']
    technicon = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','MaintainSecrecyOutsiders', 'SecurityMeasures','OutsiderDisclosuresRestricted','RestrictedMaterialsUsed','KnewInfoConfidential','SecretsDisclosedOutsiders','InfoReverseEngineerable','InfoReverseEngineered']
    trandes = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','ConfidentialityAgreement','MaintainSecrecyDefendant','MaintainSecrecyOutsiders', 'AgreedNotToDisclose','SecurityMeasures','OutsiderDisclosuresRestricted','DisclosureInNegotations','SecretsDisclosedOutsiders']
    valcoCincinnati = ['a trade secret was misappropriated, find for plaintiff','TradeSecretMisappropriation','EffortstoMaintainSecrecy','InfoValuable','InfoUsed','ConfidentialRelationship','NoticeOfConfidentiality','MaintainSecrecyOutsiders', 'SecurityMeasures','OutsiderDisclosuresRestricted','UniqueProduct','KnewInfoConfidential','DisclosureInNegotations','SecretsDisclosedOutsiders']

    cases = {'Arco Industries Corp v Chemcast Corp':arco, 'The Boeing Company v Sierracin Corp':boeing,'M. Bryce & Associates Inc v Gladstone':bryce, 'College Watercolour Group Inc v William H. Newbauer':collegeWatercolour,'Den-Tal-Ez Inc v Siemens Capital Corp':denTalEz,'Ecolgix Inc v Fantsteel Inc':ecolgix,'A.H. Emery Co v Marcon Products Corp':emery,'Ferranti Electric Inc v Harwood':ferranti,'Commonwealth v Robinson':robinson,'Sandlin v Johnson':sandlin,'Sheets v Yamaha Motors Corp':sheets,'Space Aero Products Corp v R.E. Darling Corp':spaceAero,'Televation Telecommunications Systems Inc v Saindon':televation,'Midland-Ross Corp v Yokana':yokana,'CMI Corp v Jakob':cm1,'Digital Development Corp v International Memory Systems':digitalDevelopment,'FMC Corp v Taiwan Tainan Giant Ind Co Ltd':fmc,'Forest Laboratories Inc v Formulations Inc':forrest,'Goldberg v Medtronic':goldberg,'K & G Oil Tool & Services Co v G & G':kg,'Laser Industries Ltd v Eder Instrument Co':laser,'Computer Print Systems v Lewis':lewis,'MBL (USA) Corp v Diekman':mbl,'Mason v Jack Daniel Distillery':mason,'Mineral Deposits Ltd v Zigan':mineralDeposits,'National Instruments Labs Inc v Hycel Inc':nationalInstruments,'National Rejectors Inc v Trieman':nationalRejectors,'Reinforced':reinforced,'Scientology':scientology, 'Technicon Data Systems Corp v Curtis':technicon,'Trandes Corp v Guy F. Atkinson Co':trandes,'Valco Cincinnati Inc v N & D Machining Service Inc':valcoCincinnati}
    
    return cases    


