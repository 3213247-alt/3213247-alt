
def simulate_funnels():
    print(f"{'Metric':<30} | {'User':<10} | {'Realistic':<10} | {'Univ. Stream':<10}")
    print("-" * 70)
    
    scenarios = [
        {"name": "User", "starters": 12855, "pass": 0.45, "ret": 0.65},
        {"name": "Realistic", "starters": 12855, "pass": 0.45, "ret": 0.85},
        {"name": "Univ", "starters": 5000, "pass": 0.65, "ret": 0.90}, 
    ]
    
    for i in range(1, 5):
        line = [f"Exam {i} Passers"]
        for sc in scenarios:
            # simple simulation
            # pass 1
            if i == 1:
                sc["curr"] = sc["starters"] * sc["pass"]
            else:
                sc["curr"] = sc["curr"] * sc["ret"] * sc["pass"]
            
            line.append(f"{int(sc['curr']):<10}")
        
        print(f"{line[0]:<30} | {line[1]} | {line[2]} | {line[3]}")

    print("-" * 70)
    # Total Qualified (4 exams + 56% skills factor)
    line = ["Qualified (Skills)"]
    for sc in scenarios:
        val = sc["curr"] * 0.56
        line.append(f"{int(val):<10}")
    print(f"{line[0]:<30} | {line[1]} | {line[2]} | {line[3]}")

simulate_funnels()
