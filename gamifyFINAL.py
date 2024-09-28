######################################################################################
# Initialize all global variables to initial conditions, in the sense they do not impact
# if-type statements.
def initialize():
    # Initializes the global variables needed for the simulation.
    global cur_hedons, cur_health
    global cur_time
    global last_activity, last_activity_duration
    global last_finished
    global bored_with_stars
    global running_star
    global textbook_star
    global star_time_1
    global star_time_2
    global star_time_3
    global cumulative_running_time
    global cumulative_textbooks_time

    running_star = False
    textbook_star = False

    star_time_1 = -200
    star_time_2 = -200
    star_time_3 = -200
    cur_hedons = 0
    cur_health = 0
    cur_star = None
    cur_star_activity = None
    bored_with_stars = False
    last_activity = None
    last_activity_duration = 0
    cur_time = 0
    last_finished = -1000
    cumulative_running_time = 0
    cumulative_textbooks_time = 0

# Check whether star can be taken for a given activity.
def star_can_be_taken(activity):
    global star_time_3, cur_time, running_star, textbook_star
    if cur_time == star_time_3 and not bored_with_stars:
        if (activity == "running" and running_star):
            running_star = False
            return True
        elif (activity == "textbooks" and textbook_star):
            textbook_star = False
            return True
    return False

# Calculate final hedon and health points based on the duration of activity
# and the type of activty.
def perform_activity(activity, duration):
    global cur_hedons, cur_health
    global cur_time
    global last_activity, last_activity_duration
    global last_finished
    global bored_with_stars
    global cumulative_running_time
    global cumulative_textbooks_time

    hedons = 0
    star_used = False

    if activity == "running":
        # ADD CUMULATIVE RUN TIME
        cumulative_running_time += duration
        cumulative_textbooks_time = 0
        hedons = estimate_hedons_delta("running", duration)

    elif activity == "textbooks":
        # ADD CUMULATIVE TEXTBOOK TIME
        cumulative_textbooks_time += duration
        cumulative_running_time = 0
        hedons = estimate_hedons_delta("textbooks", duration)


    elif activity == "resting":
        cumulative_running_time = 0
        cumulative_running_time = 0

    # Update cur_hedons with the calculated hedons
    cur_hedons = cur_hedons + hedons

    # Calculate health points
    health_points = estimate_health_delta(activity, duration)
    cur_health += health_points  # Update health points first

    # Update the last finished timing and activity
    cur_time = cur_time + duration
    if not (activity == "resting"):
        last_finished = cur_time    
    last_activity = activity
    last_activity_duration = duration

# Return the current total hedon count.
def get_cur_hedons():
    global cur_hedons
    return cur_hedons

# Return the total health point count.
def get_cur_health():
    global cur_health
    return cur_health

# Check if bored, if not bored update coressponding activity for star bonus activated.
def offer_star(activity):
    # Update star times, check if less than 120 minutes between most recent, and third
    # most recent star, if so set bored_with_stars to True, set star corresponding to
    # activity to be True
    
    global bored_with_stars
    global star_time_1
    global star_time_2
    global star_time_3
    global running_star
    global textbook_star

    star_time_1 = star_time_2
    star_time_2 = star_time_3
    star_time_3 = cur_time

    if (star_time_3 - star_time_1) < 120:
        bored_with_stars = True

    if(activity == "running"):
        running_star = True
    else:
        textbook_star = True

# Determines the most fun activty in the next 1 minute.
def most_fun_activity_minute():
    global cur_time, last_finished
    # Calculate hedons for resting, running, and textbooks for 1 minute
    resting_hedons = 0  # Resting gives 0 hedons
    running_hedons = estimate_hedons_delta("running", 1)
    textbooks_hedons = estimate_hedons_delta("textbooks", 1)

    # Rubbish, honestly.
    # # Ensure hedons do not drop below 0
    # running_hedons = max(running_hedons, -float('inf'))  # Keep it as is; can be negative
    # textbooks_hedons = max(textbooks_hedons, -float('inf'))  # Keep it as is; can be negative

    # Find the maximum hedons among the activities
    max_hedons = max(running_hedons, textbooks_hedons, resting_hedons)

    if max_hedons == running_hedons:
        return "running"
    elif max_hedons == textbooks_hedons:
        return "textbooks"
    else:
        return "resting"

######################################################################################
# Calculate the hedon count for a given activity over a given duration.
def estimate_hedons_delta(activity, duration):
    # Return the amount of hedons for performing activity for duration minutes.

    # Determines if the user is tired
    is_tired = (cur_time - last_finished) < 120

    if activity == "running":
        # Determine hedons based on tiredness and stars
        if is_tired:
            if star_can_be_taken("running"):
                if duration <= 10:
                    return duration
                else:
                    return 10 + (duration - 10) * -2
            else:
                return duration * -2
        else:
            if star_can_be_taken("running") and (cur_time - last_finished) < 120:
                if duration <= 10:
                    return duration * 2 + (duration * 3)
                else:
                    return 50 + (duration - 10) * -2
            else:
                if duration <= 10:
                    return duration * 2
                else:
                    return 20 + (duration - 10) * -2

    elif activity == "textbooks":
        # Determine hedons based on tiredness and stars
        if is_tired:
            if star_can_be_taken("textbooks"):
                if duration <= 10:
                    return duration
                else:
                    return 10 + (duration - 10) * -2
            else:
                return duration * -2
        else:
            if star_can_be_taken("textbooks") and (cur_time - last_finished) < 120:
                if duration <= 20:
                    return duration * 1 + (3 * duration)
                else:
                    return 50 + (duration - 20) * -1
            else:
                if duration <= 20:
                    return duration
                else:
                    return 20 + (duration - 20) * -1
    return 0

# Calculate the health count for a given activity over a given duration.
def estimate_health_delta(activity, duration):
    # Return the amount of health points for performing activity for duration minutes.
    if activity == "running":
        if cumulative_running_time <= 180:
            return (duration * 3)
        else:
            return (180 - (cumulative_running_time - duration)) * 3 + (cumulative_running_time - 180) * 1
    elif activity == "textbooks":
        return (duration * 2)
    return 0

######################################################################################
if __name__ == '__main__':
    initialize()
    perform_activity("running", 30)
    print(get_cur_hedons())            # -20 = 10 * 2 + 20 * (-2)             # Test 1
    print(get_cur_health())            # 90 = 30 * 3                          # Test 2
    print(most_fun_activity_minute())  # resting                              # Test 3
    perform_activity("resting", 30)
    offer_star("running")
    print(most_fun_activity_minute())  # running                              # Test 4
    perform_activity("textbooks", 30)
    print(get_cur_health())            # 150 = 90 + 30*2                      # Test 5
    print(get_cur_hedons())            # -80 = -20 + 30 * (-2)                # Test 6
    offer_star("running")
    perform_activity("running", 20)
    print(get_cur_health())            # 210 = 150 + 20 * 3                   # Test 7
    print(get_cur_hedons())            # -90 = -80 + 10 * (3-2) + 10 * (-2)   # Test 8
    perform_activity("running", 170)
    print(get_cur_health())            # 700 = 210 + 160 * 3 + 10 * 1         # Test 9
    print(get_cur_hedons())            # -430 = -90 + 170 * (-2)              # Test 10
