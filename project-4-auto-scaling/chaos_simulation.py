"""Local-only Auto Scaling + chaos-test demonstration. Creates no AWS resources."""
from collections import Counter

AZS = ["ap-south-1a", "ap-south-1b", "ap-south-1c"]
MIN_CAPACITY, MAX_CAPACITY = 3, 8
desired = 4
instances = []
next_id = 0


def healthy():
    return [i for i in instances if i["state"] == "InService" and i["registered"]]


def launch(excluded=None):
    global next_id
    excluded = excluded or set()
    if len(healthy()) >= MAX_CAPACITY:
        return False
    active = healthy()
    ondemand = sum(i["capacity"] == "On-Demand" for i in active)
    target_ondemand = max(1, (desired + 1) // 2)
    capacity = "On-Demand" if ondemand < target_ondemand else "Spot"
    counts = Counter(i["az"] for i in active if i["az"] not in excluded)
    available = [az for az in AZS if az not in excluded]
    if not available:
        return False
    az = min(available, key=lambda x: (counts[x], x))
    next_id += 1
    iid = f"sim-{next_id:03}"
    print(f"Launching {iid}: {capacity}, {az}")
    print("  Lifecycle hook: warm-up / DB migration represented as a simulation.")
    print("  Health check passed; simulated target registered.")
    instances.append({"id": iid, "capacity": capacity, "az": az,
                      "state": "InService", "registered": True})
    return True


def restore(excluded=None):
    while len(healthy()) < desired:
        if not launch(excluded):
            break


def report(label):
    active = healthy()
    print(f"\n{label}: {len(active)} healthy simulated targets")
    print("  Capacity mix:", dict(Counter(i["capacity"] for i in active)))
    print("  AZ distribution:", dict(Counter(i["az"] for i in active)))
    if active:
        print("  Simulated service status: at least one target healthy")
    else:
        print("  WARNING: no healthy targets in simulation")
    return len(active)


def main():
    global desired
    print("PROJECT 4: LOCAL AUTO SCALING & CHAOS SIMULATION")
    print("Local only: no AWS API calls and no AWS resources created.")
    desired = MIN_CAPACITY + 1
    restore()
    assert report("Initial mixed fleet") >= MIN_CAPACITY

    print("\nCPU test: simulated average CPU = 82%; target = 70%")
    desired = min(desired + 1, MAX_CAPACITY)
    restore()
    assert report("After CPU scale-out") >= MIN_CAPACITY

    print("\nALB test: simulated requests per target = 1300; threshold = 1000")
    desired = min(desired + 1, MAX_CAPACITY)
    restore()
    assert report("After request-count scale-out") >= MIN_CAPACITY

    print("\nChaos test 1: manually terminate one instance")
    victim = healthy()[0]
    victim["state"] = "Terminated"
    victim["registered"] = False
    restore()
    assert report("After termination recovery") >= MIN_CAPACITY

    print("\nChaos test 2: simulate ap-south-1b AZ failure")
    for item in healthy():
        if item["az"] == "ap-south-1b":
            item["state"] = "Unavailable"
            item["registered"] = False
    restore(excluded={"ap-south-1b"})
    final_count = report("After simulated AZ recovery")
    assert final_count >= MIN_CAPACITY, "Simulation failed to restore minimum healthy capacity"
    assert all(i["az"] != "ap-south-1b" for i in healthy()), "Failed AZ still has healthy targets"

    print("\nPASS: local logic restored minimum capacity after the simulated failures.")
    print("LIMITATION: does not test actual ALB traffic, AWS lifecycle hooks, real Spot interruptions, or zero downtime.")


if __name__ == "__main__":
    main()
