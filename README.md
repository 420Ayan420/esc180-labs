  # esc180-labs
  Will fill out as time allows.

  # gamify.py
  ### Activity Rules
  1. Running:
    - Health Points:
      - Less than 180 minutes: Gain 3 health points per minute.
      - More than 180 minutes: Gain 1 health point per minute for every minute after 180.
      - Clock Reset: The running health point calculation resets if the user carries textbooks or rests for even one minute.
    - Hedons:
      - If Tired:
        - If No Star: Lose 2 hedons/min.
        - If Star Available:
          - Fewer than 3 stars used in the last hour:
            - First 10 minutes: Gain 1 hedon/min (−2 + 3).
            - After 10 minutes: Lose 2 hedons/min (star bonus expires).
      - If Not Tired:
        - If No Star:
          - First 10 minutes: Gain 2 hedons/min.
          - After 10 minutes: Lose 2 hedons/min.
        - If Star Available:
          - Fewer than 3 stars used in the last hour:
            - First 10 minutes: Gain 5 hedons/min (2 + 3).
            - After 10 minutes: Lose 2 hedons/min.
          - If 3 stars have been used in the last hour:
            - First 10 minutes: Gain 2 hedons/min.
            - After 10 minutes: Lose 2 hedons/min.

  2. Resting:
    - Health: 0 health points per minute.
    - Hedons: 0 hedons per minute.

  3. Carrying Textbooks:
    - Health: Gain 2 health points per minute.
    - Hedons:
      - If Tired:
        - If No Star: Lose 2 hedons/min.
        - If Star Available:
          - Fewer than 3 stars used in the last hour:
            - First 10 minutes: Gain 1 hedon/min (−2 + 3).
            - After 10 minutes: Lose 1 hedon/min.
      - If Not Tired:
        - If No Star:
          - First 20 minutes: Gain 1 hedon/min.
          - After 20 minutes: Lose 1 hedon/min.
        - If Star Available:
          - Fewer than 3 stars used in the last hour:
            - First 10 minutes: Gain 4 hedons/min (1 + 3).
            - After 10 minutes: Gain 1 hedon/min for the remaining 20-minute period.
          - If 3 stars have been used in the last hour:
            - First 20 minutes: Gain 1 hedon/min.
            - After 20 minutes: Lose 1 hedon/min.

