METRIC_INFO = {
    'Safety (Low Crime)': {
        'description': 'Measures neighborhood safety based on reported crime incidents over the past year. Higher scores indicate fewer crimes.',
        'score_explanation': 'Score is inverted crime count — higher means safer. A score of 25,000 means very few crimes; a score near 0 means high crime area.',
        'top_meaning': 'These are Chicago\'s safest neighborhoods. Residents here experience significantly fewer reported crimes including theft, assault, and property crime. Ideal for families and those prioritizing security.',
        'bottom_meaning': 'These neighborhoods have the highest crime rates in Chicago. Consider additional safety precautions, research specific blocks, and visit at different times of day before committing.'
    },
    'School Quality (Overall)': {
        'description': 'Comprehensive school quality score combining safety, instruction, environment, teacher quality, leadership, family involvement, and student attendance across all schools.',
        'score_explanation': 'Score out of 100 based on: Safety (15), Instruction (15), Environment (10), Low Misconduct (10), Teachers (10), Leaders (10), Family Involvement (10), Parent Engagement (10), Attendance (10).',
        'top_meaning': 'These neighborhoods have the strongest schools across all metrics. Expect quality instruction, safe environments, engaged parents, and strong leadership. Great for families with children of any age.',
        'bottom_meaning': 'Schools in these areas struggle across multiple dimensions — lower attendance, weaker instruction, and less parent engagement. Consider charter schools, magnet programs, or selective enrollment options if moving here.'
    },
    'Elementary Schools': {
        'description': 'Quality score for elementary schools (ES) only, focusing on early childhood metrics like PK-2 literacy/math and grades 3-5 performance.',
        'score_explanation': 'Score out of ~73 based on: Safety (10), Environment (8), Instruction (10), Teachers (8), Family Involvement (7), PK-2 Literacy (8), PK-2 Math (8), Gr3-5 Math (7), Gr3-5 Reading (7).',
        'top_meaning': 'Best neighborhoods for children ages 5-11. Strong early literacy and math foundations, safe classrooms, and involved parent communities. Kids here start their academic journey on solid footing.',
        'bottom_meaning': 'Elementary schools here show weaker early reading and math outcomes. Early intervention and supplemental tutoring may be needed. Research individual schools — some may outperform the neighborhood average.'
    },
    'High Schools': {
        'description': 'Quality score for high schools (HS) only, emphasizing college readiness metrics like graduation rates, college eligibility, and ACT scores.',
        'score_explanation': 'Score out of ~50 based on: Safety (8), Instruction (8), Graduation Rate (10), College Eligibility (8), College Enrollment (8), ACT Score (8).',
        'top_meaning': 'Teenagers here have the best shot at college success. High graduation rates, competitive ACT scores, and strong college enrollment. These schools open doors to universities and careers.',
        'bottom_meaning': 'High schools in these areas have lower graduation rates and college readiness. Many students don\'t finish or aren\'t prepared for higher education. Look into selective enrollment high schools or alternative pathways.'
    },
    'College Readiness': {
        'description': 'Focused purely on college preparation outcomes — how well do high schools prepare students for higher education?',
        'score_explanation': 'Score out of 100 based on: Graduation Rate (20), College Eligibility (25), College Enrollment (25), ACT Score (20), Freshman on Track (10).',
        'top_meaning': 'Students from these neighborhoods actually go to college. High ACT scores, strong graduation rates, and proven college enrollment. If higher education is your priority, these are your neighborhoods.',
        'bottom_meaning': 'Very few students from these high schools enroll in college. Lower ACT scores and graduation rates create barriers to higher education. Consider this carefully if college is a priority for your family.'
    }
}

# Map settings
MAP_CENTER = {'lat': 41.8781, 'lon': -87.6298}
MAP_ZOOM = 9
MAP_STYLE = 'open-street-map'
COLOR_SCALE = 'RdYlGn'
from pathlib import Path

# Get the project root (parent of dashboard folder)
PROJECT_ROOT = Path(__file__).parent.parent

# Data paths
DATA_PATHS = {
    'crimes': PROJECT_ROOT / 'notebooks/data/raw/Crimes_-_One_year_prior_to_present.csv',
    'education': PROJECT_ROOT / 'notebooks/data/raw/Chicago_Public_Schools_-_Progress_Report_Cards_(2011-2012).csv',
    'socioeconomic': PROJECT_ROOT / 'notebooks/data/raw/Census_Data_-_Selected_socioeconomic_indicators_in_Chicago,_2008_–_2012.csv',
    'geojson': 'https://data.cityofchicago.org/resource/igwz-8jzy.geojson'
}
