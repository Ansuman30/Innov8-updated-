# Innov8-updated-

This was one of the PS given in hackathon Innov8 2.0 at IITD Final Round.

#Problem Statement
So problem was that a large company say have thousands of resume as well as recommendation letter coming and it is very difficult for the company to go through each of them and reject the fraudulent one. Fradulent can be defined as resume not according to job,highly exaggerated statement given by recommender,circular endorsment i.e A person recommending B and B recommending A hence increasing the no of recommendation.

#Data Format
2 Zip file one of Recommendation another one of Resume with each of this zip file containing folder with the ID mentioned. Resume  was in pdf. Whereas recommendation was in the form of text and in text file the IDs who have recommended the given ID is mentioned .

#Solution
PDF and text file extracted into a CSV file . Certain exaggerted words were observed and after few observation was used as counter to see the repetition which was eventually used to score out exaggeration score. No of cicular endorsment counted, No of recommendation, years of experience,and finally similarity score was used to judge resume and create resume score.
A final score metrics was calculated by manually giving weights to each of the factor and keeping a threshold of greater than 0.5 as genuine. 

#Code
final.ipynb file explains the calculation and several csv file created . Each of the csv file shows the each individual factor and later on merged on mostfinaloutput.csv to label Approved and Fraud.

#Website
For convienience streamlit app has been created and hosted online and one could access through this link https://tjfcp6ggnhhzhtqhtvzynx.streamlit.app/   
Search feature, checking each of the score as well as the content present in resume of that ID. Distribution of classification in the form of number as well as in pie chart.

#Further Development
Allowing the user to upload their zip file provided they follow the same format as it is used . LLM integration to humanize what might be the reason for this number what further action company needs to take.

