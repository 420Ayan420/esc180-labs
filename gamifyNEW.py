######################################################################################
def initialize():
    '''Initializes the global variables needed for the simulation.'''
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
    """Determine if a star can be offered for the given activity."""
    global bored_with_stars, cur_star_activity, cur_star  # Ensure global declaration

    if bored_with_stars:
        return False

    if cur_star_activity == activity:
        return False  # Cannot offer a star for the same activity consecutively

    # If it's a new activity, we can offer a star
    cur_star_activity = activity
    return True

def perform_activity(activity, duration):
    """Perform the specified activity for a given duration."""
    global cur_time

    cur_time += duration  # Increment the current time

    if activity == "running":
        running_health(duration)
        running_hedons(duration)
    elif activity == "textbooks":
        textbooks_health(duration)
        textbooks_hedons(duration)
    elif activity == "resting":
        resting_health(duration)
        resting_hedons(duration)

    last_activity = activity
    last_activity_duration = duration


def get_cur_hedons():
    """Get the current number of hedons."""
    global cur_hedons
    return cur_hedons


def get_cur_health():
    """Get the current health points."""
    global cur_health
    return cur_health


def offer_star(activity):
    """Offer a star for the specified activity."""
    global cur_star, bored_with_stars

    if star_can_be_taken(activity):
        cur_star = activity  # Assign the star to the current activity
        bored_with_stars = True  # Mark that the user is bored with stars
    else:
        print("Cannot offer a star for this activity right now.")


def most_fun_activity_minute():
    """Determine the most fun activity for the last minute."""
    global last_activity_duration, last_activity, cur_hedons, cur_health

    # Assuming "fun" is based on hedons gained; you could also incorporate other metrics
    if last_activity == "running":
        return "running"
    elif last_activity == "textbooks":
        return "textbooks"
    elif last_activity == "resting":
        return "resting"
    else:
        return "no activity performed yet"

def running_health(minutes):
    """Calculate health points gained from running.""" 
    global cur_health

    if last_activity in ['textbooks', 'rest']:
        # Reset health calculation if previous activity was textbooks or resting
        last_activity_duration = 0  

    if minutes <= 180:
        cur_health += minutes * 3
    else:
        cur_health += (180 * 3) + ((minutes - 180) * 1)

def running_hedons(minutes):
    """Calculate hedons gained from running.""" 
    global cur_hedons, last_activity, last_activity_duration, last_finished

    if last_activity in ['textbooks', 'rest']:
        # Reset hedons calculation if previous activity was textbooks or resting
        last_activity_duration = 0  

    if last_activity == 'running' and (cur_time - last_finished <= 60):
        # If running again within the last hour
        if last_activity_duration < 60:
            last_activity_duration += minutes
        else:
            # More than an hour has passed
            last_activity_duration = minutes
    else:
        last_activity_duration = minutes

    if cur_time - last_finished < 60:
        # Running with star conditions
        if cur_star is not None and cur_star_activity == 'running':
            if last_activity_duration < 10:
                cur_hedons += 5 * minutes  # First 10 minutes with star
            else:
                cur_hedons -= 2 * minutes  # Lose hedons after 10 minutes
        else:
            if last_activity_duration < 10:
                cur_hedons += 2 * minutes  # First 10 minutes without star
            else:
                cur_hedons -= 2 * minutes  # Lose hedons after 10 minutes
    else:
        # Reset hedons to base condition
        if last_activity_duration < 10:
            cur_hedons += 2 * minutes
        else:
            cur_hedons -= 2 * minutes

    last_activity = 'running'
    last_finished = cur_time

def textbooks_health(minutes):
    """Calculate health points gained from carrying textbooks.""" 
    global cur_health

    cur_health += minutes * 2

def textbooks_hedons(minutes):
    """Calculate hedons gained/lost from carrying textbooks.""" 
    global cur_hedons, last_activity, last_activity_duration

    if last_activity in ['running', 'rest']:
        # Reset hedons calculation if previous activity was running or resting
        last_activity_duration = 0  

    if last_activity == 'textbooks' and (cur_time - last_finished <= 60):
        # If carrying textbooks again within the last hour
        if last_activity_duration < 20:
            last_activity_duration += minutes
        else:
            # More than an hour has passed
            last_activity_duration = minutes
    else:
        last_activity_duration = minutes

    if cur_star is not None and cur_star_activity == 'textbooks':
        if last_activity_duration < 10:
            cur_hedons += 4 * minutes  # First 10 minutes with star
        elif last_activity_duration < 30:
            cur_hedons += 1 * minutes  # After 10 minutes with star
        else:
            cur_hedons -= 1 * minutes  # Lose hedons after 20 minutes
    else:
        if last_activity_duration < 20:
            cur_hedons += 1 * minutes  # First 20 minutes without star
        else:
            cur_hedons -= 1 * minutes  # Lose hedons after 20 minutes

    last_activity = 'textbooks'
    last_finished = cur_time

def resting_health(minutes):
    """Calculate health points from resting.""" 
    global cur_health

    # Resting gives 0 health points
    cur_health += 0

def resting_hedons(minutes):
    """Calculate hedons from resting.""" 
    global cur_hedons

    # Resting gives 0 hedons
    cur_hedons += 0

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
