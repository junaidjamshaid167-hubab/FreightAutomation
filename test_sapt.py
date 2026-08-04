from terminals.sapt import SAPTTerminal

terminal = SAPTTerminal()

containers = [
    "TIIU4183115",
    "MSDU4275984",
    "MSBU5328633",
    "MEDU7936247",
]

for container in containers:

    print("\n" + "=" * 60)
    print("CONTAINER:", container)
    print("=" * 60)

    try:
        html = terminal.get_container_history(container)

        print("HTTP response received")
        print("HTML length:", len(html))

        # Save every response separately
        filename = f"sapt_{container}_history.html"

        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)

        print("Saved:", filename)

        # Look for important indicators
        print("Contains _jsonArray:", "_jsonArray" in html)
        print("Contains ContainerHistory:", "ContainerHistory" in html)
        print("Contains container number:", container in html)
        print("Contains PID:", '"pid"' in html)
        print("Contains isSuccess:", '"isSuccess"' in html)

    except Exception as e:
        print("ERROR:", type(e).__name__)
        print(e)