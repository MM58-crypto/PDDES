from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from ui.models import Question, Choice
from django.views import generic
from .forms import QuestionForm, GHQ12Form
from inference_engine.models import GHQ12Response

from knowledge_base.models import Psych_D_symptoms, Disorder_Diagnosis
#from knowledge_base.models import System_rules
import rules 


""" 
Current rules defined in the rules model : 
 1. IF Q1 == 'Frequently' AND Q2 == 'Yes' OR Q2 == 'Sometimes' AND Q3 == " Yes" AND Q4 == "Yes" AND Q5 == "Yes"
THEN C1 ==  "Social Anxiety"
 2.  IF Q6 == 'True' AND Q7 == 'Yes' OR Q7 == 'Occasionally' AND Q8 == 'Yes' AND Q9 == 'Yes' AND Q10 == 'Agree'  AND Q11 == 'Always' OR Q11 =='Occasionally'
THEN C2 ==  "Generalized Anxiety Disorder"
 3.   IF Q12 == 'Yes' AND Q13 == 'Direct experience' OR Q13 == 'Witnessing the event occurring to someone else' OR Q13 == 'Finding out that a close family member or close friend experienced the horrific event(s)' AND Q14 == 'Yes' AND Q15 == 'Frequently' OR Q15 == 'Occasionally' AND Q16 == 'Yes'  AND Q17 == 'Yes' OR Q18 == 'No'
THEN C3 ==  "Post Traumatic Stress Disorder"
 4.  IF Q19 == 'Yes' AND Q20 == 'Yes' AND Q21 == 'Yes' AND Q22 == 'Yes'  AND Q23 == 'Yes'  
THEN C4 ==  "Obsessive Compulsive Disorder"
 5.  IF (Q24 == 'Yes' AND Q25 == 'Yes' AND Q26 == 'Yes' AND Q27 == 'Yes'  AND Q28 == 'Yes)'  AND( Q29 == 'Yes'  OR  Q30 == 'Yes')
THEN C5 ==  "Anti social personality disorder"
 6.  IF Q31 == 'Yes' AND Q32 == 'I did lose interest' AND Q33 == 'Yes i gained/lost a lot of weight' AND Q34 == 'Yes'  AND Q35 == 'Yes' OR Q35 == 'Such thoughts occur to me occasionally'  AND Q36 == 'Yes'  OR  37 == 'Yes' 
THEN C6 ==  "Depression"
 7.  IF Q38 == 'Yes' AND Q39 == 'Yes' AND Q40 == 'Yes' AND Q41 == 'Yes'  AND Q42 == 'Yes' AND Q43 == 'Yes'  AND Q44 == 'Yes'  AND  45 == 'Yes' 
THEN C7 ==  "Bipolar disorder" 

"""

@login_required(login_url='/accounts/login/')
def d_test_view(request):
    # backward chaining <-- required 
    
    # add levels (eg. Highly likely, Likely, possible, unlikely, highly unlikely)
    # general questions first then shift to specific questions based on the input
    # a dictionary can be used to store all the disorders and implement the rules
    disorders = {'social_anxiety':False, 'ptsd':False, 'bipolar': False, 'anti_social':False, 'ocd':False, 'anxiety': False, 'depression': False}
    #social_anxiety = False
    if request.method == "POST":
        form = QuestionForm(request.POST)
        # this approach is not quite efficient and time consuming
        # there must be an easier way to do this (maybe the score method)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
            # social anxiety, highly likely
            if selected_choices.get('2') == '6' and selected_choices.get('3') =='7' and selected_choices.get('4') == '10' and selected_choices.get('5') == '13' and selected_choices.get('6') == '16':
                sa_desc = Disorder_Diagnosis.objects.get(id=1)
                likelihood = "very high"
                disorders['social_anxiety'] = True
                context = {'social_anxiety': disorders['social_anxiety'],
                 'sa_desc':sa_desc, 'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # possible 
            elif selected_choices.get('2') == '5' and selected_choices.get('3') =='9' and selected_choices.get('4') == '12' and selected_choices.get('5') == '15' and selected_choices.get('6') == '17':
                sa_desc = Disorder_Diagnosis.objects.get(id=1)
                likelihood = "possible "
                disorders['social_anxiety'] = True
                context = {'social_anxiety': disorders['social_anxiety'],
                 'sa_desc':sa_desc, 'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # unlikely 
            elif selected_choices.get('2') == '4' and selected_choices.get('3') =='8' and selected_choices.get('4') == '11' and selected_choices.get('5') == '14' and selected_choices.get('6') == '17':
                sa_desc = Disorder_Diagnosis.objects.get(id=1)
                likelihood = "unlikely "
                disorders['social_anxiety'] = True
                context = {'social_anxiety': disorders['social_anxiety'],
                 'sa_desc':sa_desc, 'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # anxiety , 
            # highly likely
            if selected_choices.get('7') == '18' and selected_choices.get('8') =='20' or selected_choices.get('8') =='22'  and selected_choices.get('9') == '23' and selected_choices.get('10') == '25' and selected_choices.get('11') == '28'and selected_choices.get('12') == '30' or selected_choices.get('12') == '31':
                aa_desc = Disorder_Diagnosis.objects.get(id=6)
                likelihood = "very high"
                disorders['anxiety'] = True
                context = {'anxiety': disorders['anxiety'],
                 'aa_desc':aa_desc, 'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # possible 
            elif selected_choices.get('7') == '18' and selected_choices.get('8') =='22'   and selected_choices.get('9') == '24' and selected_choices.get('10') == '27' and selected_choices.get('11') == '29'and selected_choices.get('12') == '31' or selected_choices.get('12') == '32':
                aa_desc = Disorder_Diagnosis.objects.get(id=6)
                likelihood = "possible"
                disorders['anxiety'] = True
                context = {'anxiety': disorders['anxiety'],
                 'aa_desc':aa_desc, 'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # unlikely
            elif selected_choices.get('7') == '18' and selected_choices.get('8') =='20' or selected_choices.get('8') =='22'  and selected_choices.get('9') == '23' and selected_choices.get('10') == '25' and selected_choices.get('11') == '28'and selected_choices.get('12') == '30' or selected_choices.get('12') == '31':
                aa_desc = Disorder_Diagnosis.objects.get(id=6)
                likelihood = "unlikely"
                disorders['anxiety'] = True
                context = {'anxiety': disorders['anxiety'],
                 'aa_desc':aa_desc, 'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # ptsd, highly likely
            if selected_choices.get('13') == '34' and (selected_choices.get('14') =='36' or selected_choices.get('14') =='37' or selected_choices.get('14') == '38') and selected_choices.get('15') == '39'  and selected_choices.get('17') == '44' or selected_choices.get('17') == '45' and selected_choices.get('18') == '47' and selected_choices.get('19') == '50'and selected_choices.get('20') == '52' :
                ptsd_desc = Disorder_Diagnosis.objects.get(id=4)
                likelihood = "very high"
                disorders['ptsd'] = True
                context = {'ptsd': disorders['ptsd'], 'likelihood':likelihood,
                 'ptsd_desc': ptsd_desc
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # possible 
            elif selected_choices.get('13') == '34' and (selected_choices.get('14') =='36' or selected_choices.get('14') =='37' or selected_choices.get('14') == '38') and selected_choices.get('15') == '40'  and (selected_choices.get('17') == '45' or selected_choices.get('17') == '46') and selected_choices.get('18') == '48' and selected_choices.get('19') == '49'and selected_choices.get('20') == '52' :
                ptsd_desc = Disorder_Diagnosis.objects.get(id=4)
                likelihood = "possible"
                disorders['ptsd'] = True
                context = {'ptsd': disorders['ptsd'], 'likelihood':likelihood,
                 'ptsd_desc': ptsd_desc
                }
                return render(request, "Screening_pgs/prediction_result.html", context)
            # unlikely
            elif selected_choices.get('13') =='35' :
                ptsd_desc = Disorder_Diagnosis.objects.get(id=4)
                likelihood = "Unlikely"
                disorders['ptsd'] = False # maybe it should be false
                context = {'ptsd': disorders['ptsd'], 'likelihood':likelihood,
                 'ptsd_desc': ptsd_desc , 
                }
                return render(request, "Screening_pgs/prediction_result.html", context)

            # ocd, highly likely 
            if selected_choices.get('21') == '53' and selected_choices.get('22') =='55' and selected_choices.get('23') == '57' and selected_choices.get('24') == '59' and selected_choices.get('25') == '61':
                ocd_desc = Disorder_Diagnosis.objects.get(id=5)
                likelihood = "very high"
                disorders['ocd'] = True
                context = {'ocd': disorders['ocd'], 'ocd_desc': ocd_desc,
                'likelihood':likelihood, 
                }
                return render(request, "Screening_pgs/prediction_result.html", context)

            # possible (ocd)
            elif selected_choices.get('21') == '53' and selected_choices.get('22') =='55'   and selected_choices.get('23') == '57' and selected_choices.get('24') == '59' and selected_choices.get('25') == '61':
                ocd_desc = Disorder_Diagnosis.objects.get(id=5)
                likelihood = "possible"
                disorders['ocd'] = True
                context = {'ocd': disorders['ocd'], 'ocd_desc': ocd_desc,
                'likelihood':likelihood}
                return render(request, "Screening_pgs/prediction_result.html", context) 
            # unlikely (ocd)
            elif selected_choices.get('21') == '54' and selected_choices.get('22') =='56'   and selected_choices.get('23') == '58' and selected_choices.get('24') == '60' and selected_choices.get('25') == '62':
                ocd_desc = Disorder_Diagnosis.objects.get(id=5)
                likelihood = "unlikely"
                disorders['ocd'] = True
                context = {'ocd': disorders['ocd'], 'ocd_desc': ocd_desc,
                'likelihood':likelihood }
                return render(request, "Screening_pgs/prediction_result.html", context) 
            # anti_social highly likely
            if selected_choices.get('26') == '113' and selected_choices.get('27') =='65' and selected_choices.get('28') =='67' and selected_choices.get('29') == '69' and (selected_choices.get('30') == '71' or selected_choices.get('30')=='112') and selected_choices.get('31') == '73' and selected_choices.get('32') == '75':
                anti_social_desc = Disorder_Diagnosis.objects.get(id=7)
                likelihood = "very high"
                disorders['anti_social'] = True
                context = {'anti_social': disorders['anti_social'],'anti_social_desc':anti_social_desc,
                'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 
            # anti_social possible
            elif selected_choices.get('26') == '63' and selected_choices.get('27') =='66' and selected_choices.get('28') =='67'  and selected_choices.get('29') == '69' and (selected_choices.get('30') == '71' or selected_choices.get('30') =='112') and selected_choices.get('31') == '74' and selected_choices.get('32') == '75':
                anti_social_desc = Disorder_Diagnosis.objects.get(id=7)
                likelihood = "possible"
                disorders['anti_social'] = True
                context = {'anti_social': disorders['anti_social'],'anti_social_desc':anti_social_desc,
                'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 
            # anti social unlikely 
            elif (selected_choices.get('26') == '64' or selected_choices.get('26')=='63') and selected_choices.get('27') =='66' and selected_choices.get('28') =='68'  and selected_choices.get('29') == '70' and (selected_choices.get('30') == '71' or selected_choices.get('30') =='112') and selected_choices.get('31') == '74' and selected_choices.get('32') == '76':
                anti_social_desc = Disorder_Diagnosis.objects.get(id=7)
                likelihood = "unlikely"
                disorders['anti_social'] = True
                context = {'anti_social': disorders['anti_social'],'anti_social_desc':anti_social_desc,
                'likelihood': likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 
            # depression highly likely 
            if selected_choices.get('34') == '80' and (selected_choices.get('35') =='82' or selected_choices.get('35') =='83') and selected_choices.get('36') =='84'  and (selected_choices.get('37') == '86' or  selected_choices.get('37') == '87') and selected_choices.get('38') == '89' and selected_choices.get('39') == '91':
                depression_desc = Disorder_Diagnosis.objects.get(id=3)
                likelihood = "very high"
                disorders['depression'] = True
                context = {'depression': disorders['depression'], 'depression_desc':depression_desc,
                'likelihood': likelihood, 
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 
             # depression possible 
            elif selected_choices.get('34') == '80' and selected_choices.get('35') =='83' and (selected_choices.get('36') =='85' or selected_choices.get('36') =='84')  and selected_choices.get('37') == '86'  and selected_choices.get('38') == '90' and selected_choices.get('39') == '92':
                depression_desc = Disorder_Diagnosis.objects.get(id=3)
                likelihood = "possible"
                disorders['depression'] = True
                context = {'depression': disorders['depression'], 'depression_desc':depression_desc,
                'likelihood': likelihood, 
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 
             # depression unlikely  
            elif selected_choices.get('34') == '81' and  selected_choices.get('35') =='83' and selected_choices.get('36') =='85'  and selected_choices.get('37') == '88'  and selected_choices.get('38') == '90' and selected_choices.get('39') == '92':
                depression_desc = Disorder_Diagnosis.objects.get(id=3)
                likelihood = "unlikely"
                disorders['depression'] = True
                context = {'depression': disorders['depression'], 'depression_desc':depression_desc,
                'likelihood': likelihood, 
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 

            # bipolar highly likely 
            if selected_choices.get('40') == '93' and selected_choices.get('41') =='95' and selected_choices.get('42') =='97'  and selected_choices.get('43') == '99' and selected_choices.get('44') == '101' and selected_choices.get('45') == '103'and selected_choices.get('46') == '105' and selected_choices.get('47') == '107' and selected_choices.get('48') == '109':
                likelihood = "very high"
                bipolar_desc = Disorder_Diagnosis.objects.get(id=2)
                disorders['bipolar'] = True
                context = {'bipolar': disorders['bipolar'],
                'bipolar_desc': bipolar_desc, 'likelihood':likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 

            # bipolar  possible
            elif selected_choices.get('40') == '94' and selected_choices.get('41') =='96' and selected_choices.get('42') =='97'  and selected_choices.get('43') == '99' and selected_choices.get('44') == '102' and selected_choices.get('45') == '104'and selected_choices.get('46') == '105' and selected_choices.get('47') == '108' and (selected_choices.get('48') == '109' or selected_choices.get('48')=='111'):
                likelihood = "possible"
                bipolar_desc = Disorder_Diagnosis.objects.get(id=2)
                disorders['bipolar'] = True
                context = {'bipolar': disorders['bipolar'],
                'bipolar_desc': bipolar_desc, 'likelihood':likelihood
                }
                return render(request, "Screening_pgs/prediction_result.html", context) 

            # bipolar unlikely 
            elif selected_choices.get('40') == '94' and selected_choices.get('41') =='96' and selected_choices.get('42') =='98'  and selected_choices.get('43') == '100' and selected_choices.get('44') == '102' and selected_choices.get('45') == '104'and selected_choices.get('46') == '106' and selected_choices.get('47') == '108' and selected_choices.get('48') == '110':
               likelihood = "unlikely"
               bipolar_desc = Disorder_Diagnosis.objects.get(id=2)
               disorders['bipolar'] = True
               context = {'bipolar': disorders['bipolar'],
               'bipolar_desc': bipolar_desc, 'likelihood':likelihood
               }
               return render(request, "Screening_pgs/prediction_result.html", context) 
            

            

       #return redirect('/results')
    
    form = QuestionForm()
    context = {
        'questions_form': form, 

    }
    return render(request, "Screening_pgs/diagnosis_test.html", context)
def ghq_view(request):
    if request.method =="POST":
        form = GHQ12Form(request.POST)
        if form.is_valid():
           form.save()
            
           score = calculate_ghq12_score()
           if score <= 11:
               message = "Your score suggests that you are not currently experiencing significant psychological distress."
               delete_all_objs(GHQ12Response)
           elif score <= 23:
               message = "Your score suggests that you may be experiencing some psychological distress. We recommend that you seek further evaluation from a mental health professional."
               delete_all_objs(GHQ12Response)
           else:
               message = "Your score suggests that you are experiencing significant psychological distress. We strongly recommend that you seek further evaluation from a mental health professional."
               delete_all_objs(GHQ12Response)
           return render(request, 'Screening_pgs/ghq_result.html', {'score': score, 'message': message})

        
    else:
        form = GHQ12Form()
    context = {'gen_questions': form}
    # might add an additional page to display ghq results 
    return render(request,"Screening_pgs/ghq.html", context)

def calculate_ghq12_score():
    responses = GHQ12Response.objects.all()
    total_score = sum(response.response for response in responses)

    return total_score

def delete_all_objs(self):
    GHQ12Response.objects.all().delete()

# this function returns to the user the result once the form is submitted
# user input along with the system rules will be used to reach the conclusion
def results_view (request):

    #questions = Question.objects.all()
    #question_choices = Choice.objects.all()
    #
    #context : {
    #    'questions': questions,
    #    'choices': question_choices
    #}
    
    return render(request, "Screening_pgs/prediction_result.html", context) 
 
