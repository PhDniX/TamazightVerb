V = ['a', 'i', 'u', 'v']
C = ['k', 'g', 'j', 'b', 't', 'd', '6', '9', '3', 'f', 'x', 'h', '7', 's', 'c', 'z', '2', 'm', 'n', 'l', 'r', 'w'] #Consonants ordered by sonority.
K = ['K', 'G', 'J', 'B', 'T', 'D', '&', 'Q', '#', 'F', 'X', 'H', '&', 'S', 'C', 'Z', '@', 'M', 'N', 'L', 'R', 'Gw'] #Tense consonants by sonority.
#Scale = K + C + V
#Sibilant = ['s','c','z','j','S','Z']
#CCpfCCv  = ['s9']
LexHeavy = ['fhm', 'dzv', 'na9', 'zwu']
Stative  = ['m9ur', 'mlil']

#Phonetic evaluation
def Sonority(x):
	value = 0
	for phoneme in Scale:
		if x == consonant:
			value += 1
			return value
		else:
			value += 1

def StemWeight(x):
	weight = 0
	if x in LexHeavy:
		weight += 2
	if x[len(x)-1] in V:
		weight -= 1
	if x[0] in V:
		weight -= 1
	if x[len(x)-1] == 'v':
		weight += 1
	for phoneme in x:
		if phoneme in V:
			weight += 2
		if phoneme in C:
			weight += 1
		if phoneme in K:
			weight += 2
	return weight

#Stem checks
def IsRedup(x):
	if x[:len(x)-2] == x[len(x)-2:]:
		return True
	else:
		return False

def IsValidOnset(x):
	if x[0] in K or x[0] in V:
		return False
	else:
		return True

#Morphological Functions
def Gem(x): #Main Gemination Function
	idx = 0
	for cons in C:
		if x == cons:
			return K[idx]
		else:
			idx +=1

'''def DeGem(x): #Main Gemination Function
	idx = 0
	for cons in K:
		if x == cons:
			return C[idx]
		else:
			idx +=1
'''

def GemC1(x): #Geminates the first consonant of a stem
	if x[0] in C:
		return Gem(x[0]) + x[1:]
	else:
		return x

def GemC2(x): #Geminates the second consonant of a stem
	return x[:1] + Gem(x[1]) + x[2:]

'''def DeGemC1(x): #Degeminates the first consonant of a stem
	if x[0] in K:
		return DeGem(x[0]) + x[1:]
	else:
		return x'''

def Harmonize(x): #Makes all plain vowels the same as the first in the stem.
	pos = 0
	harmony = ''
	for phoneme in x:
		if phoneme in V:
			break
		pos += 1
	harmony = x[pos]
	for phoneme in x:
		if phoneme in V:
			x = x.replace(phoneme, harmony)
	return x

def MelodyA(x): #Replace all unspecified vowels with a. Final v and internal V need to be distinguished. Final v never harmonizes with preceding long vowels, but DOES receive melody A in the end...
	x = x.replace('v', 'a')
	return  x

def PolarizeV(x): #For perfective aker > uker.
	for phoneme in x:
		if phoneme == 'a':
			x = x.replace(phoneme, 'u')
		if phoneme == 'u' or phoneme == 'i': 
			x = x.replace(phoneme, 'a')
	return x #For perfective: mmiRG pf. mmaRG (dus ook I/A nodig)

def PrefixT(x):
	return 'T' + x

def InsertV(x): #Inserts an unspecified long long vowel. before the last stem consonant.
	if x[len(x)-2] in V:
		return x
	if x[len(x)-1] in C:
		x = x[:len(x)-1] + 'v' + x[len(x)-1:]
	return x

def InsertI(x): #For negative perfective and reduplicated imperfectives.
	if x[len(x)-1] == 'v':
		return x[:len(x)-1] + 'i'
	if x[len(x)-1] in C and x[len(x)-2] in C:
		return x[:len(x)-1] + 'i' + x[len(x)-1:]
	else:
		return x

#Stem formation
def Aor(x): #At a certain stem weight, both Pf and Aor need to apply GemC1 to stems.
	stem = x
	if StemWeight(stem) >= 6:
		x = GemC1(x)
	return x

def Pf(x):
	stem = x
	#I-initial stems need a lot of mutation.
	#if x[0] == 'i':
	#	x = x[1:]
	#Not sure yet

	if StemWeight(x) <= 4:
		x = PolarizeV(x)
	if StemWeight(stem) >= 6:
		x = GemC1(x)
	if stem in Stative:
		return 'NoPf'

	#If initial i You need to remove it, and perhaps some other stuff
	#If IsGemStat: GemC2
	return x

def NegPf(x):
	if x == 'NoPf':
		return x
	if x[len(x)-1] == 'v':
		return InsertI(Pf(x))
	if StemWeight(x) <= 4:
		return InsertI(Pf(x))
	else:
		return Pf(x)

def Impf(x):
	stem = x
	weight = StemWeight(x)
	if IsValidOnset(x) == False:
		return MelodyA(PrefixT(x)) #These verbs are super extra-systemic. That sucks.
	if weight <= 2:
		x = GemC1(InsertV(x))
	if weight == 3:
		x = GemC2(x)
	if weight >= 4:
		x = PrefixT(x)
	if weight > 4:
		x = Harmonize(InsertV(x))
	if IsRedup(stem) == True:
		x = InsertI(x)
	x = MelodyA(x)
	return x

def Conj(x):
	print Aor(x) + ' | ' + Pf(x) + ' | ' + NegPf(x) + ' | ' + Impf(x)

Conj('amz')
Conj('afv')
Conj('aJv')
Conj('ackv')
Conj('i2il') #Fails in Pf
Conj('iri')  #Fails in Pf
Conj('i2ri') #Fails in Pf
Conj('annay')
Conj('ujd') #Fails in Pf.
Conj('lalv')
Conj('gaLv')
Conj('Du')
Conj('9udu')
Conj('3Du')
Conj('zwu')
Conj('b6u')
Conj('sal') #Should not have apophony.
Conj('cil')
Conj('mun') #Should not have apophony.
Conj('na9') 
Conj('fafa')
Conj('rBa')
Conj('xalf')
Conj('miz6')
Conj('7udr')
Conj('7rury')
Conj('glugl') #Should not geminate.
Conj('m9ur')
Conj('mlil') #Fails in the Pf.
Conj('krz')
Conj('gn')
Conj('Kr')
Conj('n9n9')
Conj('fhm')
Conj('s9v') #Wrong Impf. But irregular.
Conj('n9v')
Conj('dzv')
Conj('9ymv') #If we interpret as 9ymv (which is historically correct), we get the right form.
Conj('fstv')
Conj('bDv')



#print Aor('9imv')
#print Aor('na9') #Na9 fails to geminate. It is too light, can't change the stemweight restraint, because 'sal', 'cib', 'mun' do not geminate. na9 is 'heavier' than it should be.
#print Aor('gaLv')
#print Pf('akr')
#print Pf('Du')
#print NegPf('Du')
#print NegPf('akr')
#print NegPf('sal')
#print Pf('sal')
#print Impf('akr') #akir is fine in all dialects but not ayt wirra... Weight doesn't quite work out because belle9 has belli9...
#print Impf('Kr')
#print Impf('Du') #Illegal onset > PrefixT is dus ook nodig voor MA.... jammer.

#print Impf('na9')
#print Impf('DuBz')
#print Impf('gaLv') #Fails, is just as heavy as KuFu in the count right now... which it isn't in practice.
#Onderliggend: gaLv?
#print Impf('9imv') #Arabic qq stays qq?
#Onderliggend: 9im ~ je wil dus qym eigenlijk.
#print Impf('dukl')
#print Impf('Ridu') #Fails, because r can't degeminate.
#print Impf('kasv')
#print Impf('KuFu')

#print Impf('am2')
#print Impf('asv')
#print Impf('aJv')
#print Impf('ackv')

#print Impf('i2il')
#print Impf('iri')
#print Impf('i2irv') Fails but not in Oussikoum. In Penchoen it is already unique
#print Impf('annay')
#print Impf('ujd') #This verb is totally going to fail in the perfective.
#print Impf('lalv')

#print Impf('bDv')

#print Impf('Du')
#print Impf('9udu')
#print Impf('3Du')
#print Impf('zwu') #Fails, in Ayt Ndhir. Not in Ayt Wirra. Ayt Ndhir has ttezwu
#print Impf('bdu')
#print Impf('sal')
#print Impf('cib')
#print Impf('mun')

#print Impf('fafa')
#print Impf('rBa')
#print Impf('xalf')
#print Impf('miz6')
#print Impf('7udr')
#print Impf('7rury')
#print Impf('glugl') #Should not 

#print Impf('Drf') #Gaat goed
#print Impf('m9ur')
#print Impf('krz')
#print Impf('gn')
#print Impf('Kr')
#print Impf('ngng') Has no insertion in Ayt Ndhir, but the very is not in Ayt Wirra
#print Impf('sLv') #Impf. is tiselli in Ayt Wirra irregular? 'to listen' normaly: 'slv'

#print Impf('b3j') #Fails, Ayt Ndhir has tteb3ij. However, Oussikoum does not have this verb. Does the type exist?
#print Impf('s9') #Irregular, behaves like s9 in impf. but like sgv in aor/pf.
#print Impf('n9v')
#print Impf('dzv') #Fails, Tdza not dZa, Seems lexically determined. (weight is 4 instead of 3 for (no?) reason) perhaps it's sonority: edz versus ne9?
#print Impf('fstv')
#print Impf('bDv')

#print Impf('gjgj')
#print Impf('crcr') #Fails, with emphatic r, = ttceRcaR. Maybe not originally reuplicated: kercer or cerker?
#print Impf('gZr') #Fails should be TgZar
#print Impf('KF6') #Fails, shouldn't shorten.
#print Impf('mmi2d') #Fails, ttmiZZid (unexpectedly has lengthning)

#print Impf('Ridu')

#print Impf('Cv') #Fails: conjugates like ttettv ~` kinda
#print Impf('swv') #Fails: conjugates like sv
#print Impf('cv') #Fails: conjugates like akka... not like anything.

#print Impf('slv')
#print Impf('dr')
#print Impf('sal')
#print Impf('fhm')
#print Impf('lmd')
#print Impf('bdu') #Fails because same weight as sal, Tbdu insted of bDu. Maybe final syllable weight should be measured instead?


#fru ttifri fra/i fri 'peercevoir par l'ouie: entendre
#fru ferru  fra/i fri 'venger'

#Degemination or not:
#Only degem in: KVCC, KVC*, KVC (1x), KVK*
'''Heath analyses this not as degemination, but as gemination of really long stems in the pf. and aor. Would that work?
So everything that keeps gemination, has a lexical geminate. Those that do not, have a lexical single cons. If all verbs with alternation have a similar shape, that solves the matter.

duqeR
Diqs
Gimv
kasv
gafy
Gabl
Gar

gallv




'''

#D: + dduqeR ttduquR
#6: + DDiqs ttDiqis, DDukWel ttDukkul
#K: + kkasv ttkasa
#K: - kkucm ttekkucum, (KVKV is kind of expected to be as heavy as kkuffu ttekkuffu)
#G: + ggafy Tgafay, ggallv ttgalla Tgalla, ggannv ttganna 
#Q: + qqabl ttGabal, qqaR ttGaR, qqimv ttGima, qqu tteqqu, qqubbez tteqqubuz, qqum tteqqum, qqucce3 tteqqucce3
#Q: - qqabH tteqqabaH, qqadm tteqqadam, qqam tteqqam, qqil tteqqil, qqis tteqqis, qqic tteqqic (real counter examples: all Arabic?)
#M: + mmawd ttmawad, mmater ttmatar, mmitsv ttmitsi, mmulleZ ttmulluZ, mmuReDs ttmuRuTS, mmutter ttmuttur, mmuttey ttmuttuy, mmiZd ttmiZZid, mmiRG ttmiRiG, mmutter, mmuReTS, mmuttey
#N: + Na9 Tna9, Nalv ttnala, nnurz ttnuruz, 
#N: - (nniza ttenniza, KVKV should be the same weight but isn't...)
#2: + ZZallv ttZalla
#J: + djawR ttjawar
#Y: + djawn ttyawan


#M: - mmu3DeR
#K: - kkummec ttekkummuc, kkurrem ttekkurrum, 
#D: - ddu, tteddu, ddubbez tteddubbuz, dduhdu ttedduhdu. ddukkwel tteddukkul
#J: - jju ttejju
# : - ZZu tteZZu
#B: - bbuZZe3 ttebbuZZu3
#F: - No examples
#L: - Las TeLas, Ludu TeLudu, llums ttellums, llizem ttellizem
#R: - rridu tterridu, rru tterru
#S: - ssaddv ttssadda, ssu ttessu
#C: - ccur tteccur
#T: - ttilley ttettilliy, ttu ttettu, tturets, ttetturuts, ttuttey ttettuttuy, ttujy ttettujuy, ttu3a ttettu3a
#7: - TTay tteTTay, TTubb3 tteTTubbu3, TTuffey tteTTuffuy, TTummeR tteTTummuR, TTuRq tteTTuRuq, TTuRRef tteTTuRRuf, TTuRRey tteTTuRRuy, 
#X: - xxu ttexxu, xxun ttexxun, xxuc ttexxuc
#Z: - No examples
#j.:- JJu tteJJu


#For perfective: mmiRG pf. mmaRG (dus ook I/A nodig)