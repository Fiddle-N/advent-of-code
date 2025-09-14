from advent_of_code.puzzles.day_21 import process


def test():
    food_str = """\
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""
    allegen_assessment = process.AllergenAssessment.from_string(food_str)
    assert allegen_assessment.non_allergenic_ingredients == {'kfcds', 'nhms', 'sbzzf', 'trh'}
    assert allegen_assessment.non_allergenic_ingredient_occurrence() == 5
    assert allegen_assessment.allergenic_ingredients == {
        'dairy': 'mxmxvkd',
        'fish': 'sqjhc',
        'soy': 'fvjkl',
    }
    assert allegen_assessment.canonical_dangerous_ingredients == 'mxmxvkd,sqjhc,fvjkl'