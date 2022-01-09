import streamlit as st
import pandas as pd
import ipywidgets as widgets
import random
import numpy as np
import matplotlib.pyplot as plt

st.title('Boston Exam School Admissions')

#-----------------------------------------Markdown text that will be displayed in the browser-----------------------------begin
"""
    #### The effect of uneven tier distribution and bonus points on the probability of admission into Boston's exam schools.

    Until 2020, admission to Boston's three 'exam schools' was determined by a combination of a standardized test (the ISEE) and grades. Each of these two criteria was weighted equally. Students competed for these seats in a single combined pool. Thus a city-wide competition based on merit, was the only metric for admission into these selective schools.

    The new admission policy for these schools introduces several changes:
    
     1. Invitations are divided across 8 socio-economic tiers made up of census-tracts with similar socio-economic profiles. These profiles are based on 
     the following five factors: Percentage of persons below poverty, percentage of households not occupied by the owner, percentage of families headed by a single parent, 
     percentage of households where English is not the primary language spoken, and educational attainment. Tiers are sized to include an equal number of fifth-eighth grade students.
     Students are assigned to tiers based on the census-tract their home is located in. Students compete only within their assigned tier, and not across different tiers.
     2. The ISEE is eliminated.
     3. Grades are weighted at 70% and a new test, the NWEA MAP test, is weighted at 30%.
     4. The NWEA MAP test will not be considered for the 2021-22 admission cycle.

    There are 2 features of this plan that will unfairly disadvantage many students. First, the tiers are divided according to the estimated number of school aged children within a specific age range, and not by the number of eligible applicants (eligible applicants are students with a GPA of B or higher). Because the number of eligible students is substantially higher in the upper tiers, students in these tiers will have a lower probability of earning an invitation. Second, every student going to a school with more than 40% economically disadvantaged students will get 10 bonus points (out of a total score of 100) added on to their final score. These bonus points are determined by the school, and not by the socio-economic situation of the student. Since 80% of BPS students attend bonus-points schools, most students will receive the bonus points. Only 20% will not. 

    The above factors, combined with the fact that the MAP test will not be used for this 2021-2022 admission cycle, ensures that many A+ students, particularly in West-Roxbury (where most non-bonus-point-schools are located) will have no chance of being admitted to these selective schools.

    The aim of this project is to demonstrate the effect of bonus points, and of using unevenly distributed tiers, on the probability of admission to selective schools. In this project, we will generate synthetic data (within the bounds of what we know from previous admission cycles) and run repeated simulations to determine the probability distribution of admissions to these schools.
"""

with st.expander("#See Methods"):
     st.write("""
     We will first create synthetic data using two different methods. The first without bonus points, and the second with bonus points. We will create two tier distributions: First, tiers that have the same number of students (Even Distribution); second, with more students in the upper tiers (Skewed Distribution). For the skewed tier distribution, relative distribution of students per tier will be estimated by data presented by the school committee and the exam school task force.

     We will create a form where one can specify the number of applicants, the total number of seats, and the number of trial simulations to run. This will be the input interface for those who want to tinker with the data but are not familiar with the workings of a python notebook.

     Synthetic data creation:
     Two functions to create synthetic data will be written. The only difference between the functions is that one does not use bonus points in calculating the final score, and the other does. Two different methods are used to generate data as we want to explore the impact of bonus points on the probability of admission.

    1. A DataFrame containing n (= number of student) rows will be created.
    2. Raw scores will be randomly generated and assigned to each student. Scores will range from 8 to 11 (grades B to A +).
    3. Scaled scores will be calculated by multiplying raw scores by 100/11. This was the method previously used be BPS, and was employed when they ran simulations for the exam school task force.
    4. Whether or not the student gets bonus points will be generated randomly (yes =1, no =0). The random binary generator will be set such that 80% of the times the number 1 is returned (thus 80% of students get bonus points).
    5. Final scores are calculated by adding 10 points to the scaled score if the bonus points method is used. Alternatively, if the non-bonus point method is used, the final score will be the same as the scaled score.

    Repeated simulations:
    The number of simulations to be run will be specified in the input form. (Running 1000 simulations is recommended, but that will take a few minutes. If you want quick answers, run a 100 simulations).


  """)

    
#----------------------------------------Markwown text displayed in the browser ----------------------------end

#-------------------------------------------Input form---------------begin
form1 = st.sidebar.form(key ='options')

form1.header('Input Parameters')

num_stu = form1.number_input('Total eligible students', min_value = 400, max_value = 6000, value = 3000, step =200)

num_seats = form1.number_input('Total seats available', min_value = 3, max_value = 1500, value = 1000, step = 10)

num_trials = form1.number_input('Trials to run', min_value = 10, max_value = 1000, value = 100, step = 10)

form1.form_submit_button('Submit changes')
#-------------------------------------------Input form----------------end


n_students =  num_stu

total_seats =  num_seats

n_trials =  num_trials

seats_per_tier = total_seats/8

# Evenly distrubuted tier sizes (numbers should add up to 1 as total probability = 1)
tier_even =  p=[.125,.125,.125,.125,.125,.125,.125,.125]

# Unevenly distrubuted tier sizes, with larger tiers at the upper end.
tier_skew =  p=[0.09, 0.1, 0.11, 0.11, 0.12, 0.13, 0.16, 0.18]



def make_data1(tier_prob_dist):
  """
  This function takes in a list with specified array of probablities and generates a dataframe of with n_student rows.
  The columns specify the tiers, absence or presence of bonus points (0,1) and raw scores.

  Raw scores are randomly generated to range from 7 to 12 (grades B to A +).
  Bonus points are 80% randomly assigned to 80% of students.
  Tier is randomly assigned, according to the specified array of probablities.
  Scaled scores are calculated by multiplying raw score by 100/12.
  Final scores are same as scaled score: NO BONUS POINTS.
  
  """
  
  keys_col = np.arange(0,n_students,1)  #student identifier from 0-2500
  tier_col = np.random.choice(np.arange(1, 9),size = [n_students,1], p = tier_prob_dist).flatten().tolist() # generate a list to poppulate the tier column
  bonus_col = np.random.choice(a=[1,0], size=(n_students,1), p=[.8,.2]).flatten().tolist() # generate a list to poppulate the tier column
  raw_score = np.random.randint(8, 12, [n_students,1]).flatten().tolist()

  sim_df = pd.DataFrame(zip(keys_col,tier_col,bonus_col,raw_score), columns = ['keys','tier','bonus','raw_score'])
  sim_df['scaled_score'] = sim_df.raw_score * (100/11)
  sim_df['scaled_score'] = sim_df['scaled_score'].round(2)
  sim_df['final_score'] = sim_df['scaled_score'] + sim_df.bonus * 0
  return sim_df


def make_data2(tier_prob_dist):
  """
  This function takes in a list with specified array of probablities and generates a dataframe of with n_student rows.
  The columns specify the tiers, absence or presence of bonus points (0,1) and raw scores.

  Raw scores are randomly generated to range from 7 to 12 (grades B to A +).
  Bonus points are 80% randomly assigned to 80% of students.
  Tier is randomly assigned, according to the specified array of probablities.
  Scaled scores are calculated by multiplying raw score by 100/12.
  Final scores are calculated by adding 10 points to scaled score if student has bonus points.

  """
  
  keys_col = np.arange(0,n_students,1)  #student identifier from 0-2500
  tier_col = np.random.choice(np.arange(1, 9),size = [n_students,1], p = tier_prob_dist).flatten().tolist() # generate a list to poppulate the tier column
  bonus_col = np.random.choice(a=[1,0], size=(n_students,1), p=[.8,.2]).flatten().tolist() # generate a list to poppulate the tier column
  raw_score = np.random.randint(7, 13, [n_students,1]).flatten().tolist()

  sim_df = pd.DataFrame(zip(keys_col,tier_col,bonus_col,raw_score), columns = ['keys','tier','bonus','raw_score'])
  sim_df['scaled_score'] = sim_df.raw_score * (100/12)
  sim_df['scaled_score'] = sim_df['scaled_score'].round(2)
  sim_df['final_score'] = sim_df['scaled_score'] + sim_df.bonus * 10
  return sim_df



def simulate_trials(input_func, dist_list,cutoff_score):
  """
  The aim of this function is to return a dataframe with each row representing a trial and each column representing a tier with values representing
  the count of students at or above a certain cutoff.
  This function takes in two inputs: 1) Number of trials. 2) List of distribution probablities.
  The list of distribution probablities contains 8 elements, each of which is a numeric, the total of 8 adding up to 1 (total probablity == 1)
  It creates the simulated random data, the specified number of times.
  In this version there are NO BONUS POINTS
  At each run, it calculates the number of students who have scored above a prespecified cutoff, for each tier. The resultant series is stored.
  All of the serieses thus produced are stored in a list. This list is stored in a dataframe. The dataframe is returned.
  """

  results_list = [] # list to aggregate the results
  for i in range(n_trials):
    df_input= input_func(dist_list) # make a simulated random dataframe
    df_input['bonus'] = [0] * len(df_input)  #remove bonus points from all data
    result = df_input[df_input['final_score']>= cutoff_score].groupby('tier')['raw_score'].agg('count') #groupby tiers and count the n that scored above the cutoff score.
    results_list.append(result) #append to list
  sim_df = pd.DataFrame(results_list) #convert the list to a df
  sim_df.columns = ['tier1','tier2','tier3','tier4','tier5','tier6','tier7','tier8',]
  return sim_df



def A_plus_rejected(dist_list):
  """
  The aim of this function is to return a dataframe with each row representing a trial and each column representing a tier with values representing
  the count of students at or above a certain cutoff.
  This function takes in two inputs: 1) Number of trials. 2) List of distribution probablities.
  The list of distribution probablities contains 8 elements, each of which is a numeric, the total of 8 adding up to 1 (total probablity == 1)
  It creates the simulated random data, a specified number of times.
  At each run, it calculates the percent of students who have scored above a prespecified cutoff, for each tier, and not been accepted. The resultant series is stored.
  All of the serieses thus produced are stored in a list. This list is stored in a dataframe. The dataframe is returned.
  """
  
  list_outer = [] # list to aggregate the results. Will be used to make the dataframe
  for i in range(n_trials): #specifies the number of runs
    df_input= make_data2(dist_list) # make a simulated random dataframe
    
    list_inner = []
    for item in np.arange(1,9,1): # each cycle evaluates a tier
      #make working df by subseting by tier and sorting in descending order
      wrk_df = df_input[df_input['tier']== item].sort_values('final_score',ascending = False)
      # Select top 125 students
      accepted_df = wrk_df.iloc[:125]
      # reject the students ranked below 125
      rejected_df = wrk_df.iloc[125:]
      
      # count number of accepted students who are A +
      accepted_num = accepted_df[(accepted_df['raw_score']>11) & (accepted_df['bonus']== 0)]['raw_score'].agg('count')
      # count number of rejected students who are A +
      rejected_num = rejected_df[(rejected_df['raw_score']>11) & (rejected_df['bonus']== 0)]['raw_score'].agg('count')
     
      #Calculate rejection rate, convert to percent and round to 2 decimal places
      reject_rate = round((rejected_num/(rejected_num + accepted_num)) *100,2)
      # Add to inner list
      list_inner.append(reject_rate)
    
    
    list_outer.append(list_inner) # list to aggregate the results. Will be used to make the dataframe------
    
    
  sim_df = pd.DataFrame(list_outer) #convert the list to a df
  sim_df.columns = ['tier1','tier2','tier3','tier4','tier5','tier6','tier7','tier8',]
  return sim_df



df_even_NoBonus_A = simulate_trials(make_data1,tier_even, 90)

df_skew_NoBonus_A = simulate_trials(make_data1,tier_skew, 90)

df_even_NoBonus_Aplus = simulate_trials(make_data1,tier_even, 100)

df_skew_NoBonus_Aplus = simulate_trials(make_data1,tier_skew, 100)

#--------------------------------------------------Markdown text that will be displayed in the browser------------------------------begin

with st.expander(" Explanatory note for the plots"):
     st.write("""
        1. The x-axis shows the number of students with a score at or above a cutoff score. A cutoff score of 90 was used to generate plots in the two left most columns, and a cutoff of 100 was used to generat plots
        for the two right most columns).

        2. The y-axis counts the number of times, out of n repeated trials, a particular result was reached. For example if y-axis = 20 and x-axis = 200, and n_trials = 100, then there were 20
        instances, out of 100 trials, when 200 students scored at or above the cutoff score.

        3. The red line is set at 125, the number of seats available to each tier (calculated by dividing the total seats by the number of tiers).

        4. If the entire histogram is located to the left of the red line, then for all trial runs, there were more seats than students who scored above the specified cutoff. Conversely, when
        the entire histogram is located to the right of the redline, then there are more students than seats for every run of the n_trials. If the histogram straddles the redline, then there were
        some trials where there were more students (who scored above the cutoff) than seats, and some trials where there were less students (who scored above the cutoff) than there were seats.
        """)
"""
#### When no bonus points are awarded.
"""
#--------------------------------------------------Markdown text that will be displayed in the browser--------------------------------end

fig, ax = plt.subplots(len(df_even_NoBonus_A.columns),4, figsize = (18, 15))
for i, item in enumerate(df_even_NoBonus_A):
    df_even_NoBonus_A[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,0])
    df_skew_NoBonus_A[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,1])
    df_even_NoBonus_Aplus[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,2])
    df_skew_NoBonus_Aplus[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,3])

    ax[i,0].set_ylabel('Tier ' + str(i +1), size = 14)

for item in ax.flatten():
    item.set_xlim(20,300)
    item.axvline(125,0,250, color = 'r')
    item.grid(False)

ax[0,0].set_title('Even Tiers \n N with score 90 and above', size = 16)
ax[0,1].set_title('Skewed Tiers \n N with score 90 and above', size = 16)
ax[0,2].set_title('Even Tiers \n N with score 100 and above', size = 16)
ax[0,3].set_title('Skewed Tiers \n N with score 100 and above', size = 16)
st.pyplot(fig)



"""
#### When bonus points are awarded to 80% of students.
"""
df_skew_bonus_A = simulate_trials(make_data2,tier_skew,90)
df_even_bonus_A = simulate_trials(make_data2, tier_even,90)
df_skew_bonus_Aplus = simulate_trials(make_data2,tier_skew,100)
df_even_bonus_Aplus = simulate_trials(make_data2, tier_even,100)

fig, ax = plt.subplots(len(df_skew_bonus_A.columns),4, figsize = (18, 15))
for i, item in enumerate(df_skew_bonus_A):
  df_even_bonus_A[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,0])
  df_skew_bonus_A[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,1])
  df_even_bonus_Aplus[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,2])
  df_skew_bonus_Aplus[item].hist(histtype = 'step', bins = 10, lw = 2, ax = ax[i,3])
 
  ax[i,0].set_ylabel('Tier ' + str(i +1), size = 14)

for item in ax.flatten():
  item.set_xlim(20,300)
  item.axvline(125,0,300, color = 'r')
  item.grid(False)


ax[0,0].set_title('Even Tiers \n N with score 90 and above', size = 16)
ax[0,1].set_title('Skewed Tiers \n N with score 90 and above', size = 16)
ax[0,2].set_title('Even Tiers \n N with score 100 and above', size = 16)
ax[0,3].set_title('Skewed Tiers \n N with score 100 and above', size = 16)

st.pyplot(fig)

"""
### Percentage of students with perfect scores, but no bonus points, who are rejected.
The results of n trials to determine the percentage of students with perfect scores who will be rejected. As you run more trials (increase n), random noise will disappear.
"""


df_1000_even_reject = A_plus_rejected(tier_even) # Thousand trials, tiers are evenly distrubuted

df_1000_skew_reject = A_plus_rejected(tier_skew) # Thousand trials, tiers are skewed



"""
##### Even distribution of tiers.

"""


st.write(df_1000_even_reject.agg(['mean','std']))


"""
##### Skewed distribution of tiers.
"""


st.write(df_1000_skew_reject.agg(['mean','std']))




