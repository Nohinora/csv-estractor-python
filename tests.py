import common_data
import re

# ^[0-9]{7}1[0-9]{5}$

mat = "2730421100031"

print(re.search(common_data.models["aroma x"],mat))
