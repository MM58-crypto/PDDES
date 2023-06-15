# PDDES [Psychlogical Disorders Diagnosis Expert System] 
(Final Year Project) 

## Brief description:
A comprehensive expert system designed to assist in the assessment of psychological disorders. This system utilizes a knowledge base and user responses to generate appropriate conclusions or diagnoses. It caters to both mental health professionals and general users. 
Additionally, it benefits individuals who may face financial constraints or lack access to nearby mental health clinics. The diagnostic questions employed in the system adhere to the criteria outlined in the DSM (Diagnostic and Statistical Manual of Mental Disorders)

## It is crucial to emphasize that this system is not intended to substitute or replace experts, but rather to provide valuable support.


Built using python (Django framework) for backend and HTML + CSS + Javascript for the frontend.
Only diagnoses or predicts 7 disorders.
Uses rule-based approach along with backward chaining in reaching the conclusion.

## Main Features: 
- User-friendly interface designed for both experts and general users.
- Comprehensive psychological disorder questionnaires/tests available for seven disorders: social anxiety, generalized anxiety disorder, OCD, PTSD, bipolar disorder, and antisocial personality disorder.
- General assessment tool provided for normal users to determine a specific disorder, guiding them to specific disorder-related questions based on their responses.
- Knowledge base interface accessible to experts, allowing them to modify or view disorder data in the database.
- Individual disorder tests exclusively accessible to experts.
- Integration of the Google Maps API, enabling users who obtain high scores on the tests to locate nearby mental health clinics using GPS functionality toggled by the user.

## Limitations: 
 - The system is only providing results related to 7 disorders. Due to the great number of psychological disorders out there (approx. 300), it is quite challenging to include details/data about each one
 - An obvious limitation is the fact that the system can not operate without internet .
 - 



