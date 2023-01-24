from django.db import models

# Create your models here.

# db table containing symptoms of psych disorders
class Psych_D_symptoms(models.Model):
    symptom_name = models.CharField(max_length=255)
    symptom_desc = models.TextField()
    symptom_keywords = models.CharField(max_length=255)
    class Meta:
        verbose_name = "Symptoms of Disorder"

    def __str__(self):
        return self.symptom_name
# db table containing psych disorders 
""" 
According to the project's scope the system can diagnose only
8 disorders which are: 
Anxiety Disorder, Bipoloar disorder, Social anxiety, 
PTSD, Depression, Obsessive-Compulsive, Schizophrenia, 
Anti-Social personality Disorder 
(Schizophrenia might not be added to this list)
"""
class Disorder_Diagnosis(models.Model):

    disorder_name = models.CharField(
        max_length=255,
        #choices = Disorder_choices,
        #default = 'social_anxiety'
    )
    #models.CharField(max_length=255)
    disorder_desc = models.TextField()
    disorder_keywords = models.CharField(max_length=255)
    symptoms = models.ManyToManyField(Psych_D_symptoms)

    class Meta:
        verbose_name = "Psychological Disorder"

    def __str__(self):
        return self.disorder_name
        
# db table containing rules of the expert system
class System_rules(models.Model):
    rule_name = models.CharField(max_length=255)
    rule_statement = models.TextField()
    conclusion = models.ForeignKey(Disorder_Diagnosis, on_delete=models.CASCADE)
   # symptom = models.ManyToManyField(Psych_D_symptoms)
    class Meta:
        verbose_name = "System rule"
    
    def __str__(self):
        return self.rule_name

#    Disorder_choices = [
#    ('social_anxiety','Social anxiety'),
#    ('bipolar disorder','bipolar disorder'),
#    ('ptsd','PTSD'),
#    ('depression','Depression'),
#    ('obsessive_compulsive','Obsessive Compulsive'),
#    ('anti_social','Anti-Social personality disorder'),
#    ('anxiety','Anxiety'),
#    #('schizophrenia','Schizophrenia')
#]