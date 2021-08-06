intercept = 6.06544681
patient_age = 0.00217305
preoperative_PSA = -0.30855258
preoperative_PSA_Spline_1 = 0.00273133
preoperative_PSA_Spline_2 = -0.00754754
pathologic_Gleason_Grade_Group_2 = -0.85166185
pathologic_Gleason_Grade_Group_3 = -2.04732288
pathologic_Gleason_Grade_Group_4 = -2.69430008
pathologic_Gleason_Grade_Group_5 = -2.730107
extracapsular_Extension = -0.75415866
seminal_Vesicle_Invasion = -0.52491813
lymph_Node_Involvement = -1.1522794
surgical_Margin_Status = -0.87872476
scaling_Parameter = 0.98794906
C_index = 0.83823618
Model_N = 11960

PSAPreopKnot1 = 0.2
PSAPreopKnot2 = 4.7
PSAPreopKnot3 = 7.2
PSAPreopKnot4 = 96.53

# Grade Group 1 = Gleason 6 (or less)
# Grade Group 2 = Gleason 3+4=7
# Grade Group 3 = Gleason 4+3=7
# Grade Group 4 = Gleason 8
# Grade Group 5 = Gleason 9-10

def sp1var(
    psa_value
):
    sp1_variable = max(psa_value - PSAPreopKnot1, 0)**3
    sp1_variable += -(max(psa_value - PSAPreopKnot3, 0)**3)*(PSAPreopKnot4 - PSAPreopKnot1)/(PSAPreopKnot4 - PSAPreopKnot3)
    sp1_variable += (max(psa_value - PSAPreopKnot4, 0)**3)*(PSAPreopKnot3 - PSAPreopKnot1)/(PSAPreopKnot4 - PSAPreopKnot3)

    return sp1_variable

def sp2var(
    psa_value
):
    sp2_variable = max(psa_value - PSAPreopKnot2, 0)**3
    sp2_variable += -(max(psa_value - PSAPreopKnot3, 0)**3)*(PSAPreopKnot4 - PSAPreopKnot2)/(PSAPreopKnot4 - PSAPreopKnot3)
    sp2_variable += (max(psa_value - PSAPreopKnot4, 0)**3)*(PSAPreopKnot3 - PSAPreopKnot2)/(PSAPreopKnot4 - PSAPreopKnot3)

    return sp2_variable

def gleason_value(primary_gleason, secondary_gleason):
    total = primary_gleason + secondary_gleason

    if total == 6:
        return pathologic_Gleason_Grade_Group_2
    elif total == 7:
        return pathologic_Gleason_Grade_Group_3
    elif total == 8:
        return pathologic_Gleason_Grade_Group_4
    else:
        return pathologic_Gleason_Grade_Group_5


def XB(
        psa_value,
        age,
        primary_gleason,
        secondary_gleason,
        surgical_margins,
        extracapsular,
        seminal_vesicles,
        pelvic_lymph_nodes
):
    XB = intercept
    XB += psa_value*preoperative_PSA
    XB += sp1var(psa_value) * preoperative_PSA_Spline_1
    XB += sp2var(psa_value) * preoperative_PSA_Spline_2
    XB += age*patient_age
    XB += gleason_value(primary_gleason, secondary_gleason)

    if surgical_margins:
        XB += surgical_Margin_Status
    if extracapsular:
        XB += extracapsular_Extension
    if seminal_vesicles:
        XB += seminal_Vesicle_Invasion
    if pelvic_lymph_nodes:
        XB += lymph_Node_Involvement

    return XB

def prob(
        study_time,
        time,
        psa_value,
        age,
        primary_gleason,
        secondary_gleason,
        surgical_margins,
        extracapsular,
        seminal_vesicles,
        pelvic_lymph_nodes
):
    xb = XB(
        psa_value, age, primary_gleason, secondary_gleason, surgical_margins, extracapsular,
        seminal_vesicles, pelvic_lymph_nodes
    )
    import numpy as np
    num = 1 + (np.exp(-xb)*time)**(1/scaling_Parameter)
    denum = 1 + (np.exp(-xb)*study_time)**(1/scaling_Parameter)

    return num/denum

proba2 = prob(
    study_time=2,
    time=2,
    psa_value=40,
    age=65,
    primary_gleason=4,
    secondary_gleason=5,
    surgical_margins=True,
    extracapsular=False,
    seminal_vesicles=True,
    pelvic_lymph_nodes=False
)

proba5 = prob(
    study_time=5,
    time=2,
    psa_value=40,
    age=65,
    primary_gleason=4,
    secondary_gleason=5,
    surgical_margins=True,
    extracapsular=False,
    seminal_vesicles=True,
    pelvic_lymph_nodes=False
)

print("2 years : ", proba2)
print("5 years: ", proba5)
