aircraft_weight = float(input("Enter aircraft weight (kg): "))
thrust = float(input("Enter thrust (N): "))

acceleration = thrust / aircraft_weight

print("Aircraft acceleration is:", acceleration, "m/s^2")

if acceleration > 15:
    print("High performance thrust detected.")
else:
    print("Moderate acceleration.")