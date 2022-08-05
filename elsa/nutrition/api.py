from enum import Enum

from elsa.users.models import CustomUser


class WeightGoals(Enum):
    GAIN = "GAIN"
    LOSE = "LOSE"
    MAINTAIN = "MAINTAIN"


WEIGHT_TO_GAIN_LOSE_PER_MONTH_VALUES = {
    0.5: {WeightGoals.GAIN: 350, WeightGoals.LOSE: -375},
    1: {WeightGoals.GAIN: 400, WeightGoals.LOSE: -500},
    1.5: {WeightGoals.GAIN: 450, WeightGoals.LOSE: -583},
    2: {WeightGoals.GAIN: 500, WeightGoals.LOSE: -666},
    2.5: {WeightGoals.GAIN: 550, WeightGoals.LOSE: -750},
    3: {WeightGoals.GAIN: 600, WeightGoals.LOSE: -833},
    3.5: {WeightGoals.GAIN: 650, WeightGoals.LOSE: -916},
    4: {WeightGoals.GAIN: 700, WeightGoals.LOSE: -1000},
}


def get_weight_change_per_month(user):
    weight_difference = user.weight_goal - user.weight
    abs_weight_diff = abs(weight_difference)
    weigth_change_per_month = (
        abs_weight_diff / 6 if abs_weight_diff > 11 else abs_weight_diff / 3
    )
    return weigth_change_per_month


def get_weight_goal_conclusion(user):
    weight_difference = user.weight_goal - user.weight
    if weight_difference > 0:
        weight_goal_conclusion = WeightGoals.GAIN
    elif weight_difference < 0:
        weight_goal_conclusion = WeightGoals.LOSE
    else:
        weight_goal_conclusion = WeightGoals.MAINTAIN

    return weight_goal_conclusion


def get_weight_to_gain_lose_per_month(
    weigth_change_per_month, weight_goal_conclusion
):
    weight_to_gain_lose_per_month = 0
    if weight_goal_conclusion in [WeightGoals.GAIN, WeightGoals.LOSE]:
        for key, dict in WEIGHT_TO_GAIN_LOSE_PER_MONTH_VALUES.items():
            if weigth_change_per_month <= key:
                weight_to_gain_lose_per_month = dict[weight_goal_conclusion]
                break

    return weight_to_gain_lose_per_month


def get_total_energy_expenditure(user, day, week):
    from elsa.training_plans.api import get_daily_plans

    weigth_change_per_month = get_weight_change_per_month(user)
    weight_goal_conclusion = get_weight_goal_conclusion(user)
    weight_to_gain_lose_per_month = get_weight_to_gain_lose_per_month(
        weigth_change_per_month, weight_goal_conclusion
    )

    cycling_plans, physic_plans = get_daily_plans(user, day, week)

    if len(cycling_plans) == 0:
        cycling_mets = 0
        ctt = 0
    else:
        cycling_mets = cycling_plans[0]["cycling_training_intensity"]
        ctt = cycling_plans[0]["cycling_training_time"]

    if len(physic_plans) == 0:
        physic_mets = 0
        gtt = 0
    else:
        physic_mets = physic_plans[0]["gym_training_intensity"]
        gtt = physic_plans[0]["gym_training_time"]

    # TODO set 'cycling_comp_mets' appropiately
    # whenever the cycling competition data is available.
    cycling_comp_mets = 0  # Placeholder.

    # TODO set 'cct' appropiately whenever the
    # cycling competition data is available.
    cct = 0  # Placeholder.

    # TODO ask what this variable is about.
    # resting_metabolic_unit = cycling_mets * 0.0175 * user.weight
    total_sports_activity_requirement = (
        (ctt * cycling_mets) + (cct * cycling_comp_mets) + (gtt * physic_mets)
    )

    basal_metabolic_rate = {
        CustomUser.Genders.MALE: 66
        + (13.7 * user.weight)
        + (5 * user.height)
        - (6.8 * user.age),
        CustomUser.Genders.FEMALE: 65
        + (9.6 * user.weight)
        + (1.7 * user.height)
        - (4.7 * user.age),
    }
    physical_activity_level = 0.2 * basal_metabolic_rate[user.gender]
    foods_thermic_effects = 0.1 * basal_metabolic_rate[user.gender]
    total_energy_expenditure = (
        basal_metabolic_rate[user.gender]
        + physical_activity_level
        + foods_thermic_effects
        + total_sports_activity_requirement
        + weight_to_gain_lose_per_month
    )

    return total_energy_expenditure, weight_goal_conclusion
