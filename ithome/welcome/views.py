from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from collections import OrderedDict
from .XGBoost import *
#from keras.models import load_model


import numpy as np
import pandas as pd
import os 
#from .forms import RawVendorForm # 新增 RawVendorForm
# Create your views here.
#model = load_model("final_models_司\民法259(回復原狀=返還價金)_final_司.h5")
input = np.zeros((1,11))
money = np.zeros((1,1))
#model.predict(input)


law = pd.read_csv(os.path.join(os.getcwd(),'Input_ver1.csv'),encoding = 'big5hkscs')


def best_match(x_input, law):
    dicta = {}
    law_values = law.iloc[:,2:13].replace('移轉後才自殺', '1').values
    law_values = law_values.astype(float)
    pos = list(law.地點)
    values = list(law.案件代號)
    for i in range(len(values)):
      score = np.sum(x_input[0] == law_values[i])
      dicta[pos[i]+" "+values[i]] = score
    return sorted(dicta, key=dicta.get, reverse=True)[:5]
    #return max(dicta, key = dicta.get)

def index(request):
    return HttpResponse("Hello Django.")
def hahaLaw(request):
    return render(request, "haha_law.html")
def hahaIndex(request):
    return render(request, "haha_index.html")
def hahaInput(request):
    return render(request, "haha_input.html")
def hahaFriend(request):
    return render(request, "haha_friend.html")
def hahaOutput(request):
    form = request.POST
    if form:
        for i in range(1,12):
            input[0,i-1] = float(form['Q{}'.format(i)])
        money[0,0] = float(form['money'])
        
        output = predict_proba(input, money)
        best_case = best_match(input, law)
    form = {'best_case':best_case,
            'output':output}
    return render(request, "haha_output.html", form)
    