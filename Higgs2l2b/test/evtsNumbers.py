
import sys
sys.argv.append('-b')
import ROOT

from HiggsAnalysis.Higgs2l2b.scaleFactors import scale

ROOT.gROOT.Reset();
ROOT.gROOT.SetStyle('Plain')

ROOT.gROOT.SetBatch()


def integ(histo, lower, upper):
    bmin = histo.GetXaxis().FindBin(lower)
    bmax = histo.GetXaxis().FindBin(lower)
    integ = histo.Integral(bmin,bmax)
    integ =-histo.GetBinContent(bmin)*(lower - histo.GetXaxis().GetBinLowEdge(bmin))/ histo.GetXaxis().GetBinWidth(bmin)
    integ =-histo.GetBinContent(bmax)*(histo.GetXaxis().GetBinUpEdge(bmax) -upper)/ histo.GetXaxis().GetBinWidth(bmax)
    return integ



def evalNumEvts(histosBkg, histosSig, mass):
    
    low = 0.94*mass
    up = 1.10*mass
    signal = "GluGluToHToZZTo2L2Q_M-"+str(mass)+"_8TeV"
    nEvts = dict([(s,integ(h, low, up) ) for s, h in histosBkg.iteritems()])
    nEvts[signal] =integ(histosSig[signal], low, up)

    print "MASS: ", str(mass)
    print "Event numbers in the mass window: [",str(low),", ",str(up), " ]"
    for (s, num) in nEvts.iteritems():
        print s, ": ", str(num)  

def evalNumEvtsMassWind(var, ch):

    bkgSamples = [ "WW", "WZ", "ZZ", "TT", "DYJetsToLL_M-50"]
    masses = [200, 210, 250, 275, 300, 325, 350, 400, 600]
    sigSamples = ["GluGluToHToZZTo2L2Q_M-"+str(m)+"_8TeV" for m in masses]

    ### Take histograms for bkg and signal
    bkg_hist = dict([ (s, ROOT.TFile.Open("NoNorm_"+ch+"/" + s+"EdmNtp.root").Get(var)) for s in bkgSamples])
    #[h.Rebin(rebin) for h in bkg_hist.values()]
    [h.Scale(scale[k]) for k, h in bkg_hist.iteritems()]
    
    sig_hist = dict([ (s, ROOT.TFile.Open("NoNorm_"+ch+"/" + s+"EdmNtp.root").Get(var)) for s in sigSamples])
    #[h.Rebin(rebin) for h in sig_hist.values()]
    [h.Scale(scale[k]) for k, h in sig_hist.iteritems()]
    
    ### Evaluate the number of events in the mass windows for signal and bakground
    ### for variable "var" (correspondig to a btag category) and for channel "ch"

    print "CATEGORY: ", var
    print "Channel: ", ch
    print " "
    [evalNumEvts(bkg_hist, sig_hist, m) for m in masses]
    print "*"*40

def evalNumEvtsAllRange(var, ch):
    bkgSamples = [ "WW", "WZ", "ZZ", "TT", "DYJetsToLL_M-50"]
    masses = [200, 210, 250, 275, 300, 325, 350, 400, 600]
    sigSamples = ["GluGluToHToZZTo2L2Q_M-"+str(m)+"_8TeV" for m in masses]

    ### Take histograms for bkg and signal
    bkg_hist = dict([ (s, ROOT.TFile.Open("NoNorm_"+ch+"/" + s+"EdmNtp.root").Get(var)) for s in bkgSamples])
    #[h.Rebin(rebin) for h in bkg_hist.values()]
    [h.Scale(scale[k]) for k, h in bkg_hist.iteritems()]
    
    sig_hist = dict([ (s, ROOT.TFile.Open("NoNorm_"+ch+"/" + s+"EdmNtp.root").Get(var)) for s in sigSamples])
    #[h.Rebin(rebin) for h in sig_hist.values()]
    [h.Scale(scale[k]) for k, h in sig_hist.iteritems()]
    
    ### Evaluate the number of events in the mass windows for signal and bakground
    ### for variable "var" (correspondig to a btag category) and for channel "ch"

    print "CATEGORY: ", var
    print "Channel: ", ch
    print " "
    nEvts = dict([(s,h.Integral() ) for s, h in bkg_hist.iteritems() ])
    for s,h in sig_hist.iteritems():
        nEvts[s]=h.Integral()

    print "Event numbers"
    for (s, num) in nEvts.iteritems():
        print s, ": ", str(num)
    print "*"*40



    
ch = "El"
evalNumEvtsAllRange("lljjmass", ch)
evalNumEvtsAllRange("lljjmass_1btag", ch)
evalNumEvtsAllRange("lljjmass_0btag", ch)
