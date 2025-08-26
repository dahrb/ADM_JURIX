from MainClasses import *

def adf():
    """
    the adf for the domain
    """
    adf = ADF('WildAnimals')
    
    #non-leaf factors
    adf.addNodes('Decide',['Ownership or ( RightToPursue and IllegalAct and not NoBlame )','RightToPursue and IllegalAct'],['find for the plaintiff, find against the defendant','do not find for the plaintiff, the defendant did not act illegally, do not find against the defendant','do not find for the plaintiff, find for the defendant'])
    adf.addNodes('RightToPursue',['OwnsLand or ( ( HotPursuit and PMotive ) or ( PMotive and ( not DMotive ) ) )'],['plaintiff had a right to pursue the quarry','plaintiff had no right to pursue the quarry'])
    adf.addNodes('Ownership',['( OwnsLand and Resident ) or Convention or Capture'],['the plaintiff owned the quarry','the plaintiff did not own the quarry'])
    adf.addNodes('IllegalAct',['Trespass or Assault'],['an illegal act was committed','no illegal act was committed'])
    adf.addNodes('Trespass',['LegalOwner and AntiSocial'],['defendant committed trespass','defendant committed no trespass'])
    adf.addNodes('AntiSocial',['( Nuisance or Impolite ) and ( not DMotive )'],['defendant committed an antisocial act','defendant committed no antisocial acts'])
    adf.addNodes('PMotive',['PLiving or ( ( PSport or PGain ) and ( not DLiving ) )'],['plaintiff has good motive','plantiff has no good motive'])
    adf.addNodes('DMotive',['not Malice and ( DLiving or DSport or DGain )'],['defendant has good motive','defendant has no good motive'])
    adf.addNodes('Capture',['not NotCaught'],['the plaintiff had captured the quarry','the plaintiff had not captured the quarry'])
    adf.addNodes('OwnsLand',['LegalOwner'],['plaintiff owned the land','plaintiff did not own the land'])    
    
    #questions
    adf.addNodes('NoBlame',question='Was the defendant blameless in the interference of the plaintiff\'s pursuit?')
    adf.addNodes('Resident',question='Did the quarry reside on the land?')
    adf.addNodes('Convention',question='Is the possession of the quarry governed by convention?')
    adf.addNodes('Assault',question='Did an assault prevent the plaintiff from retaining possession of the quarry?')
    adf.addNodes('LegalOwner',question='Was the plaintiff the legal owner of the land?')
    adf.addNodes('Nuisance',question='Did the defendant\'s interference with the plaintiff\'s pursuit amount to a nuisance?')
    adf.addNodes('Impolite',question='Was the interference of the defendant in the plaintiff\'s pursuits impolite?')
    adf.addNodes('PLiving',question='Was the plaintiff pursuing the quarry for their livelihood?')
    adf.addNodes('PSport',question='Was the plaintiff pursuing the quarry for sport?')
    adf.addNodes('PGain',question='Did the plaintiff seek to personally gain from the quarry?')
    adf.addNodes('DLiving',question='Was the defendant pursuing the quarry for their livelihood?')
    adf.addNodes('Malice',question='Was the defendant malicious in their motive?')
    adf.addNodes('DSport',question='Was the defendant pursuing the quarry for sport?')
    adf.addNodes('DGain',question='Did the defendant seek to personally gain from the quarry?')
    adf.addNodes('NotCaught',question='Was the quarry not caught by the plaintiff?')
    adf.addNodes('HotPursuit',question='Was the plaintiff in hot pursuit of the quarry?')

    adf.questionOrder = ['PSport','PGain','PLiving','DSport','DGain','DLiving','Malice','HotPursuit','NotCaught','LegalOwner','Impolite','Nuisance','Assault','Resident','Convention','NoBlame']

    return adf

def cases(): 
    """
    test cases
    """
        
    keeble = ['NotCaught','LegalOwner','Malice','Nuisance','DSport','PLiving']
    pierson = ['NotCaught','HotPursuit','Impolite','PSport','Vermin']
    young = ['NotCaught','HotPursuit','Impolite','PLiving','DLiving']
    ghen = ['NotCaught','Convention','NoBlame','PLiving','DLiving']
    popov = ['NotCaught','HotPursuit','Assault','NoBlame','PGain','DGain']
    
    cases = {'Keeble v Hickeringill':keeble,'Pierson v Post':pierson,'Young v Hitchens':young,'Ghen v Rich':ghen,'Popov v Hayashi':popov}
    
    return cases

def expectedOutcomeCases():
    """
    first factor is the outcome - the other factors are those from the prolog program of the domain 
    """
    keeble = ['find for the plaintiff, find against the defendant','IllegalAct','Trespass','AntiSocial','RightToPursue','OwnsLand','PMotive','NotCaught','LegalOwner','Malice','Nuisance','DSport','PLiving']   
    pierson = ['do not find for the plaintiff, find for the defendant','AntiSocial','RightToPursue','PMotive','NotCaught','HotPursuit','Impolite','PSport','Vermin']
    young = ['do not find for the plaintiff, find for the defendant','RightToPursue','DMotive','PMotive','NotCaught','HotPursuit','Impolite','PLiving','DLiving']
    ghen = ['find for the plaintiff, find against the defendant','DMotive','PMotive','Ownership','NotCaught','Convention','NoBlame','PLiving','DLiving']
    popov = ['do not find for the plaintiff, the defendant did not act illegally, do not find against the defendant','IllegalAct','RightToPursue','DMotive','PMotive','NotCaught','HotPursuit','Assault','NoBlame','PGain','DGain']
    
    cases = {'Keeble v Hickeringill':keeble,'Pierson v Post':pierson,'Young v Hitchens':young,'Ghen v Rich':ghen,'Popov v Hayashi':popov}
    
    return cases











