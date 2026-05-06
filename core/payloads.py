def load_payloads(file_path):

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            return [
                line.strip()
                for line in f
                if line.strip()
            ]

    except:
        return []