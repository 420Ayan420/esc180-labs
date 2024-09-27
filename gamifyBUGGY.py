######################################################################################
def initialize():
    # Initializes the global variables needed for the simulation.
    global cur_hedons, cur_health
    global cur_time
    global last_activity, last_activity_duration
    global last_finished
    global bored_with_stars
    
    cur_hedons = 0
    cur_health = 0
    cur_star = None
    cur_star_activity = None
    bored_with_stars = False
    last_activity = None
    last_activity_duration = 0
    cur_time = 0
    last_finished = -1000

def star_can_be_taken(activity):
    global cur_time, last_finished, bored_with_stars
    if bored_with_stars:
        return False
    # Determine if a star can be taken based on the activity and timing
    return (cur_time - last_finished) >= 120

def perform_activity(activity, duration):
    global cur_hedons, cur_health
    global cur_time
    global last_activity, last_activity_duration
    global last_finished
    global bored_with_stars

    # Determine if the user is tired
    is_tired = (cur_time - last_finished) < 120

    # Calculate health points
    health_points = estimate_health_delta(activity, duration)
    cur_health += health_points  # Update health points first

    hedons = 0
    star_used = False

    if activity == "running":
        # Determine hedons based on tiredness and stars
        if is_tired:
            hedons = duration * -2
        else:
            if star_can_be_taken(activity) and (cur_time - last_finished) < 120:
                star_used = True
                if duration <= 10:
                    hedons = duration * 2 + (duration * 3)
                else:
                    hedons = (10 * 2) + (duration - 10) * -2 + (3 * 10)
            else:
                if duration <= 10:
                    hedons = duration * 2
                else:
                    hedons = (10 * 2) + (duration - 10) * -2

    elif activity == "textbooks":
        # Determine hedons based on tiredness and stars
        if is_tired:
            hedons = duration * -2
        else:
            if star_can_be_taken(activity) and (cur_time - last_finished) < 120:
                star_used = True
                if duration <= 20:
                    hedons = duration * 1 + (3 * duration)
                else:
                    hedons = (20 * 1) + (duration - 20) * -1 + (3 * 20)
            else:
                if duration <= 20:
                    hedons = duration * 1
                else:
                    hedons = (20 * 1) + (duration - 20) * -1

    # Update cur_hedons with the calculated hedons
    cur_hedons = cur_hedons + hedons

    # Update the last finished timing and activity
    cur_time = cur_time + duration
    last_finished = cur_time
    last_activity = activity
    last_activity_duration = duration 

    # Set bored_with_stars if a star was used
    if star_used:
        bored_with_stars = True

def get_cur_hedons():
    return cur_hedons
    
def get_cur_health():
    return cur_health
    
def offer_star(activity):
    global bored_with_stars
    if not bored_with_stars:
        bored_with_stars = True
        
def most_fun_activity_minute():
    global cur_time, last_finished
    is_tired = (cur_time - last_finished) < 120  # Determine if the user is tired

    # Calculate hedons for resting, running, and textbooks for 1 minute
    resting_hedons = 0  # Resting gives 0 hedons
    running_hedons = estimate_hedons_delta("running", 1)
    textbooks_hedons = estimate_hedons_delta("textbooks", 1)

    # Adjust hedons if the user is tired
    if is_tired:
        running_hedons -= 2  # Penalize for being tired while running
        textbooks_hedons -= 2  # Penalize for being tired while studying

    # Ensure hedons do not drop below 0
    running_hedons = max(running_hedons, -float('inf'))  # Keep it as is; can be negative
    textbooks_hedons = max(textbooks_hedons, -float('inf'))  # Keep it as is; can be negative

    # Find the maximum hedons among the activities
    max_hedons = max(running_hedons, textbooks_hedons, resting_hedons)

    if max_hedons == running_hedons:
        return "running"
    elif max_hedons == textbooks_hedons:
        return "textbooks"
    else:
        return "resting"

######################################################################################
def estimate_hedons_delta(activity, duration):
    # Return the amount of hedons for performing activity for duration minutes.
    if activity == "running":
        if duration <= 10:
            return (duration * 2)
        else:
            return (10 * 2 + (duration - 10) * -2)
    elif activity == "textbooks":
        if duration <= 20:
            return (duration * 1)
        else:
            return (20 * 1 + (duration - 20) * -1)
    return 0

def estimate_health_delta(activity, duration):
    # Return the amount of health points for performing activity for duration minutes.
    if activity == "running":
        if duration <= 180:
            return (duration * 3)
        else:
            return ((180 * 3) + ((duration - 180) * 1))
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
    