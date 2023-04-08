from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required
from ui.models import Question, Choice
from inference_engine.models import GHQ12Question, GHChoice
from django.views import generic
from .forms import  *
# import all forms instead
#from inference_engine.models import GHQ12Response

from knowledge_base.models import Psych_D_symptoms, Disorder_Diagnosis
import rules 


@login_required(login_url='/accounts/login/')
def d_test_view(request):
    # backward chaining <-- required 
    
   
    # a dictionary can be used to store all the disorders and implement the rules
    disorders = { 'social_anxiety': {'score': 0, 'likelihood': '', 'description': Disorder_Diagnosis.objects.get(id=1)},
        'depression': {'score': 0, 'likelihood': '', 'description':Disorder_Diagnosis.objects.get(id=3)},
        'ocd': {'score': 0, 'likelihood': '', 'description':Disorder_Diagnosis.objects.get(id=5)},
        'ptsd': {'score': 0, 'likelihood': '', 'description':Disorder_Diagnosis.objects.get(id=4)},
        'gen_anxiety': {'score': 0, 'likelihood': '', 'description':Disorder_Diagnosis.objects.get(id=6)}, 
        'anti_social': {'score': 0, 'likelihood': '', 'description':Disorder_Diagnosis.objects.get(id=7)},
        'bipolar': {'score': 0, 'likelihood': '', 'description':Disorder_Diagnosis.objects.get(id=2)}  
        }
    
    # add instructions before starting the test 
    sa_questions = Question.objects.all()[0:5]
    gen_anxiety_qs = Question.objects.all()[6:11]
    depression_qs = Question.objects.all()[31:37]
    ptsd_qs = Question.objects.all()[12:18]
    ocd_qs = Question.objects.all()[18:23]
    anti_social_qs = Question.objects.all()[23:30]
    #bipolar_qs -- incomplete 
    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lose interest', 'Yes i gained/lost a lot of weight ', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            ptsd_options = ['Direct experience', ' Witnessing the event occurring to someone else', ' Finding out that a close family member or close friend experienced the horrific event(s)']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent ', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not'
            'I did not get exposed ']
            if choice.choice_text in agreements and ptsd_options:
                choices[choice.choice_text]= 2
            elif choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
    # add more questions (5 or 6 more for each disorder) 
        questions[question.question_text] = choices
    if request.method == "POST":
        form = Social_Anxiety(request.POST)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
            # calculating score 
            for question_text, choice_text in selected_choices:
                for disorder in disorders.values():
                    disorder['score'] += questions[question_text][choice_text]
            #  store the questions of each disorder in a list 
            # goal --> display the results according to the type of questions -- done 
            # eg. bipolar results when given bipolar related questions
            # gen questions direct to specific questions based on sco
            #if form displays d1 (d=disorder) qs THEN get results for that disorder -- done 
            if sa_questions and sa_questions[0].id == int(list(form.cleaned_data.keys())[0]):
                #iterate over the the disorder dictionary
                #for disorder in disorders.values():
                disorder_context = determine_disorder(disorders['social_anxiety']) 
                # Render results page for each disorder
                template_name = "Screening_pgs/new_results.html"
                return render(request, template_name, disorder_context)
           
            
            
    form = Social_Anxiety()
    context = {
        'questions_form': form, 
    }
    return render(request, "Screening_pgs/diagnosis_test.html", context)

def  anxiety_page_view(request):

    gen_anxiety = {'score': 0, 'likelihood': '', 
            'description':Disorder_Diagnosis.objects.get(id=6)
            }
    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lose interest', 'Yes i gained/lost a lot of weight ', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent ', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not' ,'I did not get exposed ']
            if choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
            elif choice.choice_text in agreements:
                choices[choice.choice_text] = 2
            else:
                choices[choice.choice_text] = 0
    
        questions[question.question_text] = choices
   
    if request.method=="POST":
        form = Anxiety_Form(request.POST)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
           
            for question_text, choice_text in selected_choices:
                gen_anxiety['score'] += questions[question_text][choice_text]

            
            #for disorder in disorders.values():
            disorder_context = determine_disorder(gen_anxiety)  
            # Render results page for each disorder
            template_name = "Screening_pgs/new_results.html"
            return render(request, template_name, disorder_context)
            
    form = Anxiety_Form()
    context = {
        'a_questions_form': form
    }
    return render(request,"Screening_pgs/disorders_questions/anxiety.html", context)

def socialanxiety_page_view(request):

    social_anxiety =  {'score': 0, 'likelihood': '', 
    'description': Disorder_Diagnosis.objects.get(id=1)}
    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lose interest', 'Yes i gained/lost a lot of weight ', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent ', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not'
            'I did not get exposed ']
            if choice.choice_text in agreements:
                choices[choice.choice_text]= 2
            elif choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
    
        questions[question.question_text] = choices
    
    if request.method=="POST":
        form = Social_Anxiety(request.POST)
        selected_choices = form.get_selected_choices()
        if form.is_valid():
            for question_text, choice_text in selected_choices:
                
                social_anxiety['score'] += questions[question_text][choice_text]

           
            #for disorder in disorders.values():
            disorder_context = determine_disorder(social_anxiety) 
            # Render results page for each disorder
            template_name = "Screening_pgs/new_results.html"
            return render(request, template_name, disorder_context)
            
    
    form = Social_Anxiety() 
    context = {
        'sa_questions_form': form
    }
    return render(request,"Screening_pgs/disorders_questions/sa.html", context)

def  depression_page_view(request):

    depression =  {'score': 0, 'likelihood': '', 
   'description':Disorder_Diagnosis.objects.get(id=3)}

    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lost interest', 'Yes i gained/lost a lot of weight', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent ', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not'
            'I did not get exposed ']
            if choice.choice_text in agreements:
                choices[choice.choice_text]= 2
            elif choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
    
        questions[question.question_text] = choices
   
    if request.method=="POST":
        form = Depression_Form(request.POST)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
            for question_text, choice_text in selected_choices:
                
                depression['score'] += questions[question_text][choice_text]

            
            #for disorder in disorders.values():
            disorder_context = determine_disorder(depression) 
            # Render results page for each disorder
            template_name = "Screening_pgs/new_results.html"
            return render(request, template_name, disorder_context)
            
    
    form = Depression_Form() # change later 
    context = {
        'depression_questions_form': form
    }
    return render(request,"Screening_pgs/disorders_questions/depression.html", context)


def ocd_view(request):

    ocd =  {'score': 0, 'likelihood': '', 
   'description':Disorder_Diagnosis.objects.get(id=5)}

    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lose interest', 'Yes i gained/lost a lot of weight ', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent ', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not'
            'I did not get exposed ']
            if choice.choice_text in agreements:
                choices[choice.choice_text]= 2
            elif choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
    
        questions[question.question_text] = choices
    

    if request.method=="POST":
        form = ocd_Form(request.POST)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
            for question_text, choice_text in selected_choices:
                ocd['score'] += questions[question_text][choice_text]

                #for disorder in disorders.values():
            disorder_context = determine_disorder(ocd) 
            # Render results page for each disorder
            template_name = "Screening_pgs/new_results.html"
            return render(request, template_name, disorder_context)
            
    
    form = ocd_Form() 
    context = {
        'ocd_questions_form': form
    }
    return render(request,"Screening_pgs/disorders_questions/ocd.html", context)


def antisocial_view(request):

    anti_social =  {'score': 0, 'likelihood': '', 
   'description':Disorder_Diagnosis.objects.get(id=5)}

    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lose interest', 'Yes i gained/lost a lot of weight ', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent ', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not'
            'I did not get exposed ']
            if choice.choice_text in agreements:
                choices[choice.choice_text]= 2
            elif choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
    
        questions[question.question_text] = choices
   

    if request.method=="POST":
        form = Antisocial_Form(request.POST)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
            for question_text, choice_text in selected_choices:
                
                anti_social['score'] += questions[question_text][choice_text]

            
            #for disorder in disorders.values():
            disorder_context = determine_disorder(anti_social) 
            # Render results page for each disorder
            template_name = "Screening_pgs/new_results.html"
            return render(request, template_name, disorder_context)
            
    
    form = Antisocial_Form() 
    context = {
        'antisocial_questions_form': form
    }
    return render(request,"Screening_pgs/disorders_questions/anti_social.html", context)


def ptsd_page_view(request):

    ptsd =  {'score': 0, 'likelihood': '', 
   'description':Disorder_Diagnosis.objects.get(id=4)}

    questions = {}
    for question in Question.objects.all():
        choices = {}
        for choice in Choice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            agreements = ['Yes', 'Frequently' ,'Agree', 'Always', 'True', 'I did lose interest', 'Yes i gained/lost a lot of weight ', 'Yes, Frequently', 'Yes i have stolen/hurt and I feel sorry about it.', 'Yes i have stolen/hurt', 'Yes, I have repeatedly performed such acts.' , 'Yes, I have']
            ptsd_options = ['Direct experience', 'Witnessing the event occuring to someone else ', ' Finding out that a close family member or close friend experienced the horrific event(s)',  'I did not get exposed']
            sometimes = ['Sometimes', 'Occasionally', 'From time to time' , 'Such thoughts occur to me occasionally ']
            disagreements = ['No', 'Not really', 'Rarely', 'Never, always focused', 'Disagree', 'False', 'No, my weight did not drastically change', 'No, I havent', 'No, I have not repeatedly performed such acts.', 'No, i dont experience distressing memories', 'I dont experience such thoughts or urges', 'No, I have not'
            'I did not get exposed ']
            if choice.choice_text in agreements and ptsd_options:
                choices[choice.choice_text]= 2
            elif choice.choice_text in sometimes:
                choices[choice.choice_text] = 1
            elif choice.choice_text in disagreements:
                choices[choice.choice_text] = 0
    
        questions[question.question_text] = choices
    ptsd_qs = Question.objects.all()[12:18]

    if request.method=="POST":
        form = ptsd_Form(request.POST)
        if form.is_valid():
            selected_choices = form.get_selected_choices()
            for question_text, choice_text in selected_choices:
                
                ptsd['score'] += questions[question_text][choice_text]

            
            #for disorder in disorders.values():
            disorder_context = determine_disorder(ptsd) 
            # Render results page for each disorder
            template_name = "Screening_pgs/new_results.html"
            return render(request, template_name, disorder_context)
            
    
    form = ptsd_Form() 
    context = {
        'ptsd_questions_form': form
    }
    return render(request,"Screening_pgs/disorders_questions/ptsd.html", context)


def determine_disorder(disorder):

    if disorder['score'] >= 10:
        disorder['likelihood'] = 'Highly Likely'
    elif disorder['score'] >= 5: 
        disorder['likelihood'] = 'Possible'                        
    else:
        disorder['likelihood'] = 'Unlikely'
    desc = disorder['description']
    score = disorder['score']
    context = {
         'likelihood': disorder['likelihood'], 
         'description': desc,
         'score': score,
         'disorder': disorder,
     }
    return context 

def ghq_view(request):
    gen_questions = {}
    
    for question in GHQ12Question.objects.all():
        choices = {}
        for choice in GHChoice.objects.filter(question=question):
            # assigning score for each option
            # eg: yes/agreements, no/disagreements, neutral/sometimes/not sure)
            # if the selected choice contains any of these assign score**
            high_score = ["Nearly every day", "Yes, completely," "Almost every night", "Yes, a great deal",  "Almost every day"]
            hmid_score = ["More than half the days, Yes, quite a bit", "Several times a week"]
            low_score = ["Several days", "Yes, but just a little", "Occasionally"]
            zero = ["Not at all", "No, not at all", "Never"]
            if choice.choice_text in high_score:
                choices[choice.choice_text]= 3
            elif choice.choice_text in hmid_score:
                choices[choice.choice_text] = 2
            elif choice.choice_text in low_score:
                choices[choice.choice_text] = 1
            elif choice.choice_text in zero:
                choices[choice.choice_text] = 0 

        gen_questions[question.question_text] = choices
        #
    disorders_q_scores = {
        'social_anxiety':{'score':0},
        'depression':{'score':0},
        'gen_anxiety':{'score':0},
        'ptsd':{'score':0},
        'ocd':{'score':0},
        'bipolar':{'score':0},
        'anti_social':{'score':0},

    }
    if request.method =="POST":
        form = GHQ12Form(request.POST)
        if form.is_valid():
            
           selected_choices = form.get_selected_choices()
           # if choice in q1 == choice.choice_text
            # change it to be list compatible
            # this is if the user scores high or selects the extreme option from questions
           if ('Over the past two weeks, how often have you felt down, depressed, or hopeless?', 'Nearly every day') in selected_choices and ('Over the past two weeks, have you lost interest or pleasure in activities you normally enjoy?', 'Yes, completely') in selected_choices and ('Over the past two weeks, have you experienced a noticeable decrease or increase in your appetite or weight?', 'Yes, a great deal') in selected_choices:
             disorders_q_scores['depression']['score'] += 3
           # add elifs later
           elif ('Over the past two weeks, how often have you felt down, depressed, or hopeless?', 'Nearly every day') in selected_choices or ('Over the past two weeks, have you lost interest or pleasure in activities you normally enjoy?', 'Yes, completely') in selected_choices or ('Over the past two weeks, have you experienced a noticeable decrease or increase in your appetite or weight?', 'Yes, a great deal') in selected_choices:
             disorders_q_scores['depression']['score'] += 1
            

           if ('Over the past two weeks, how often have you felt nervous, anxious, or on edge?', 'Nearly every day') in selected_choices and ('Over the past two weeks, have you avoided situations or activities because of fear or anxiety? ', 'Yes, completely') in selected_choices:
               disorders_q_scores['gen_anxiety']['score'] += 2

           elif ('Over the past two weeks, how often have you felt nervous, anxious, or on edge?', 'Nearly every day') in selected_choices or ('Over the past two weeks, have you avoided situations or activities because of fear or anxiety? ', 'Yes, completely') in selected_choices:
               disorders_q_scores['gen_anxiety']['score'] += 1
           
           if (' Over the past two weeks, how often have you experienced intrusive, unwanted, or distressing thoughts? ', 'Almost every day') in selected_choices and ('Over the past two weeks, have you experienced any physical or emotional reactions when something reminded you of a traumatic event from your past, such as nightmares, flashbacks, intense feelings of distress, or physical sensations like sweating or trembling?', 'Yes, a great deal'):
               disorders_q_scores['ptsd']['score'] += 2

           elif (' Over the past two weeks, how often have you experienced intrusive, unwanted, or distressing thoughts? ', 'Almost every day') in selected_choices or ('Over the past two weeks, have you experienced any physical or emotional reactions when something reminded you of a traumatic event from your past, such as nightmares, flashbacks, intense feelings of distress, or physical sensations like sweating or trembling?', 'Yes, a great deal'):
               disorders_q_scores['ptsd']['score'] += 1
           
           if ('Over the past two weeks, have you engaged in repetitive behaviors or mental acts to reduce anxiety or distress?', 'Yes, a great deal') in selected_choices and ('Over the past two weeks, have you engaged in any obsessive or compulsive behaviors that interfere with your daily activities or cause significant distress, such as excessive hand-washing, checking or re-checking, or intrusive thoughts?', 'Yes, a great deal') in selected_choices:
               disorders_q_scores['ocd']['score'] += 2

           elif ('Over the past two weeks, have you engaged in repetitive behaviors or mental acts to reduce anxiety or distress?', 'Yes, a great deal') in selected_choices or ('Over the past two weeks, have you engaged in any obsessive or compulsive behaviors that interfere with your daily activities or cause significant distress, such as excessive hand-washing, checking or re-checking, or intrusive thoughts?', 'Yes, a great deal') in selected_choices:
               disorders_q_scores['ocd']['score'] += 1
           
           if ('Over the past two weeks, how often have you felt worried or anxious about social situations? ', 'Nearly every day') in selected_choices and ('Over the past two weeks, have you avoided situations or activities because of fear or anxiety?', 'Yes, completely') in selected_choices:
               disorders_q_scores['social_anxiety']['score'] += 2

           elif ('Over the past two weeks, how often have you felt worried or anxious about social situations? ', 'Nearly every day') in selected_choices or ('Over the past two weeks, have you avoided situations or activities because of fear or anxiety?', 'Yes, completely') in selected_choices:
               disorders_q_scores['social_anxiety']['score'] += 1
           
           if ('Over the past two weeks, have you experienced any sudden or extreme changes in mood or energy levels? ', 'Yes, a great deal') in selected_choices:
               disorders_q_scores['bipolar']['score'] += 1
           
           if ('Over the past two weeks, have you disregarded or violated the rights of others, such as lying, stealing, or engaging in physical fights? ', 'Yes, a great deal') in selected_choices and ('Have you ever manipulated or conned others for personal gain, or acted in ways that are dishonest or deceitful?', 'Yes, a great deal') in selected_choices:
              disorders_q_scores['anti_social']['score'] += 2

           elif ('Over the past two weeks, have you disregarded or violated the rights of others, such as lying, stealing, or engaging in physical fights? ', 'Yes, a great deal') in selected_choices or ('Have you ever manipulated or conned others for personal gain, or acted in ways that are dishonest or deceitful?', 'Yes, a great deal') in selected_choices:
              disorders_q_scores['anti_social']['score'] += 1

           # use max to find the disorder with the highest score
           # direct user to the specific questions of the disorder with the highest score
           disorder = max(disorders_q_scores, key=lambda k: disorders_q_scores[k]['score']) 
           
           if disorder == "social_anxiety":
            return redirect('/test/') 

           elif disorder =="depression":
            return redirect('/depression_test/')
           
           elif disorder =="gen_anxiety":
            return redirect('/anxiety_test/')
           
           elif disorder =="ptsd":
            return redirect('/ptsd_test/')
           
           elif disorder =="ocd":
            return redirect('/ocd_test/')
           
           elif disorder =="anti_social":
            return redirect('/antisocial_test/')
           
           elif disorder =="bipolar":
            return redirect('/bipolar_test/')

           
           else:
                # temp
                message = "It doesnt seem that you suffer from  significant psychological distress"
                context = {
                    'message': message
                }
           return render(request, 'Screening_pgs/ghq_result.html', context)
        
        
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
    
    return render(request, "Screening_pgs/new_results.html", context) 
 
 #score = calculate_ghq12_score()
           
           #if score <= 11:
           #    message = "Your score suggests that you are not currently experiencing significant psychological distress."
           #    delete_all_objs(GHQ12Response)
           #elif score <= 23:
           #    message = "Your score suggests that you may be experiencing some psychological distress. We recommend that you seek further evaluation from a mental health professional."
           #    delete_all_objs(GHQ12Response)
           #else:
           #    message = "Your score suggests that you are experiencing significant psychological distress. We strongly recommend that you seek further evaluation from a mental health professional."
           #    delete_all_objs(GHQ12Response)

    '''
           print(selected_choices) # for testing purposes 
            after submission show the disorder qs with the highest score and redirect user to disorder specific questions (eg. via button)
            if user scores high in q1 and q2 --> depression
            elif user scores high in q5 and q6 --> gen anxiety
            elif user scores high in q7 --> ptsd
            elif user scores high in q5 and q9 --> social anxiety
            elif user scores high in q10 --> bipolar 
            elif user scores high in q11 --> ocd
            elif user scores high in q12  --> antisocial
            if selected choice value is ==3 then score conuter increment
           rint(selected_choices)
        '''